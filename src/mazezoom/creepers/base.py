# -*- coding:utf-8 -*-

#StdLib imports
import os
import sys
import time
import random
import urllib
import urllib2
import fchksum
import requests
import binascii
import shortuuid
import urlparse
from datetime import datetime
from lxml.html import fromstring

#From Projects
from constants import (USER_AGENTS, MAX_RETRY_TIMES, DEFAULT_CHARSET,
                       POSITION_APP_DIR, CHANNAL_APP_DIR)

current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.abspath(os.path.dirname(current_path))
sys.path.append(project_path)
project_settings = 'settings'
os.environ['DJANGO_SETTINGS_MODULE'] = project_settings

from django.conf import settings
from orm import ORMManager


class RegisterSubClass(type):
    def __init__(cls, name, bases, attrs):
        try:
            if PositionSpider in bases:
                if not hasattr(cls, 'abstract'):
                    if not hasattr(PositionSpider, 'subclass'):
                        PositionSpider.subclass = {}
                    PositionSpider.subclass[cls.domain] = cls

            if ChannelSpider in bases:
                if not hasattr(ChannelSpider, 'subclass'):
                    ChannelSpider.subclass = {}
                ChannelSpider.subclass[cls.domain] = cls
        except NameError:
            pass


class CreeperBase(object):

    charset = DEFAULT_CHARSET
    __metaclass__ = RegisterSubClass

    def __init__(self):
        self.session = requests.session()
        self.objects = ORMManager()
        self.session.headers['User-Agent'] = random.choice(USER_AGENTS)

    def tryAgain(self, req, retries=0):
        """
         尝试最大次数(MAX_RETRY_TIMES)后请求退出
        """
        content = ''
        if retries < MAX_RETRY_TIMES:
            try:
                time.sleep(5)
                content = urllib2.urlopen(req).read()
            except:
                retries += 1
                content = self.tryAgain(req, retries)
        return content

    def get_content(self, url, data=None):
        """
        给请求加载USER-AGENT, 获取页面内容，
        """
        content = ''
        try:
            if data is not None:
                ack = self.session.post(url, data)
            else:
                ack = self.session.get(url)
            content = ack.content
        except:
            pass
        return content

    def normalize_url(self, source, url):
        """
        >>> urlparse.urljoin('http://www.baidu.com/?a=1', '/page/1?query=a')
            http://www.baidu.com/page/1?query=a
        >>> urlparse.urljoin('http://www.baidu.com/?a=1', 'http://www.baidu.com/page/1?query=a')
            http://www.baidu.com/page/1?query=a
        """
        return urlparse.urljoin(source, url)

    def get_elemtree(self, url, data=None, ignore=False, charset=False):
        """
        生成dom树方便xpath分析
        """
        etree = None
        content = self.get_content(url, data)
        if charset:
            content = content.decode(self.charset)
        if ignore:  # 针对页面存在错误编码和多编码现象处理
            content = content.decode(self.charset, 'ignore')
        if content:
            try:
                etree = fromstring(content)
            except:
                pass
        return etree

    def quote_args(self, appname):
        """
        对传入的参数,按照对应网站charset编码
        """
        return urllib.quote(appname.encode(self.charset))

    def unquote(self, v):
        return urllib.unquote(v)

    def download_app(self, url):
        downloader = DownloadAppSpider(self.session)
        if isinstance(self, PositionSpider):
            storage = downloader.run(url, is_position=True)
        else:
            storage = downloader.run(url)
        return storage

    def run(self):
        """
        接口子类实现
        """
        pass

    def update_request_headers(self, headers):
        """
        添加HTTP请求头
        """
        self.session.headers.update(headers)

    def delete_request_headers(self, keys):
        """
        删除不需要的请求头
        """
        for key in keys:
            try:
                del self.session.headers[key]
            except KeyError:
                pass

    def __del__(self):
        self.session.close()


class PositionSpider(CreeperBase):


    def __init__(self, app_name, app_uuid=None,
                 version=None, chksum=None,
                 is_accurate=True, has_orm=True):
        """
        app_uuid: app唯一主键ID
        version: app版本， 如：3.5
        chksum: app md5校验和
        is_accurate: 标识爬虫精确抓取或者模糊抓取
        has_orm: 是否加载orm操作，设置为False不进行存数据库操作
        """
        super(PositionSpider, self).__init__()
        self.app_uuid = app_uuid
        self.version = version
        self.chksum = chksum
        self.app_name = app_name
        self.has_orm = has_orm
        self.is_accurate = is_accurate
        if settings.DEBUG and has_orm:
            self.objects.create_debug_app(
                app_uuid,
                chksum,
                app_name,
                version,
            )

    def send_request(self, appname=None, url=None,
                     data=None, tree=True,
                     charset=False, ignore=False):
        url = self.search_url if url is None else url
        if data is None and appname:
            quote_app = self.quote_args(appname)
            url = url % quote_app
        print 'url--->', url
        if tree:
            #获取页面dom树
            etree = self.get_elemtree(url, data, ignore, charset)
        else:
            #获取response的 raw string
            etree = self.get_content(url, data)
        return etree

    def verify_app(self, url=None, down_link=None):
        """
        url: detail页面链接
        down_link: 下载链接
        chsksum: 校验和
        """
        is_right = False
        #如果没有传入down_link,就需要向detail页面发送请求
        if not down_link and url:
            etree = self.send_request(url=url)
            down_link = etree.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                down_link = self.normalize_url(url, down_link)
        if down_link:
            storage = self.download_app(down_link)
            md5sum = fchksum.fmd5t(storage)[0]
            if md5sum == self.chksum:
                is_right = True
                os.unlink(storage)
        return is_right

    def record_channellink(self, result):
        """
        result: [(link, title)]
        """
        app = self.objects.get_app(self.app_uuid)
        app_version, is_created = self.objects.get_or_create_appversion(
            app,
            self.version,
            self.chksum
        )
        channel, is_created = self.objects.get_or_create_channel(
            self.name,
            self.domain
        )
        if result:
            self.objects.populate_channel_for_app(app_version, channel)
        for item in result:
            link = item[0]
            title = item[1]
            checksum = binascii.crc32(link)
            self.objects.get_or_create_channellink(
                app,
                app_version,
                checksum,
                title=title,
                url=link,
                channel=channel
            )

    def position(self):
        pass

    def run(self):
        result = self.position()
        self.record_channellink(result)


class DownloadAppSpider(CreeperBase):
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = requests.session()

    def get_storage(self, is_position=False):
        today = datetime.today()
        if is_position:
            sub_path = os.path.join(
                POSITION_APP_DIR,
                today.strftime('%Y'),
                today.strftime('%m'),
                today.strftime('%d'),
                #unique_dir
            )
        else:
            sub_path = os.path.join(
                CHANNAL_APP_DIR,
                today.strftime('%Y'),
                today.strftime('%m'),
                today.strftime('%d'),
                #unique_dir
            )
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)
        filename = self.unique_name()
        storage = os.path.join(sub_path, filename)
        return storage

    def unique_name(self):
        return shortuuid.uuid()

    def run(self, url, is_position=False):
        storage = self.get_storage(is_position)
        content = self.get_content(url)
        with open(storage, 'a') as f:
            f.write(content)
            f.flush()
        return storage


class ChannelSpider(CreeperBase):
    def __init__(self, channellink, app_uuid,
                 app_version, channel, url, title):
        super(ChannelSpider, self).__init__()
        self.channellink = channellink
        self.app_uuid = app_uuid
        self.app_version = app_version
        self.channel = channel
        self.url = url
        self.title = title

    def record_appdetail(self, result):
        detail, is_created = self.objects.get_or_create_appdetail(
            self.app_uuid,
            self.app_version,
            **result
        )
        return detail, is_created

    def record_dailydownload(self, download_times):
        self.objects.create_or_update_dailydownload(
            self.channellink,
            download_times,
            app_uuid=self.app_uuid,
            app_version=self.app_version,
            channel = self.channel
        )

    def send_request(self, url, tree=True, ignore=False):
        if tree:
            #获取页面dom树
            etree = self.get_elemtree(url, ignore=ignore)
        else:
            #获取response的 raw string
            etree = self.get_content(url)
        return etree

    def parser(self):
        pass

    def run(self):
        result= self.parser()
        download_times = result.pop('download_times', 0)
        detail, is_created = self.record_appdetail(result)
        if download_times:
            self.record_dailydownload(download_times)
