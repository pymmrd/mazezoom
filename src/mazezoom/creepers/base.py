# -*- coding:utf-8 -*-

#StdLib imports
import os
import time
import random
import urllib
import requests
import shortuuid
import urlparse
from datetime import datetime
from lxml.html import fromstring

#From Projects
from constants import (USER_AGENTS, MAX_RETRY_TIMES, DEFAULT_CHARSET,
                       POSITION_APP_DIR, CHANNAL_APP_DIR)


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

    __metaclass__ = RegisterSubClass

    def __init__(self):
        self.session = requests.session()
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

    def get_content(self, url, data=None, headers=None):
        """
        给请求加载USER-AGENT, 获取页面内容，
        """
        content = ''
        if headers:
            self.session.headers.update(headers)
        if data is not None:
            ack = self.session.post(url, data)
        else:
            ack = self.session.get(url)
        content = ack.content
        return content

    def normalize_url(self, source, url):
        """
        >>> urlparse.urljoin('http://www.baidu.com/?a=1', '/page/1?query=a')
            http://www.baidu.com/page/1?query=a
        >>> urlparse.urljoin('http://www.baidu.com/?a=1', 'http://www.baidu.com/page/1?query=a')
            http://www.baidu.com/page/1?query=a
        """
        return urlparse.urljoin(source, url)

    def get_elemtree(self, url, data=None, headers=None):
        """
        生成dom树方便xpath分析
        """
        etree = None
        content = self.get_content(url, data, headers)
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

    def download_app(self, url, headers=None, session=None):
        downloader = DownloadAppSpider(session)
        storage = downloader.run(url, headers=headers)
        return storage

    def run(self):
        """
        接口子类实现
        """
        pass

    def update_request_headers(self, headers):
        self.session.headers.update(headers)


    def delete_request_headers(self, keys):
        for key in keys:
            try:
                del self.session.headers[key]
            except KeyError:
                pass

    def __del__(self):
        self.session.close()


class PositionSpider(CreeperBase):
    charset = DEFAULT_CHARSET

    def send_request(self, appname=None, url=None,
                     data=None, headers=None, tree=True):
        url = self.search_url if url is None else url
        if data is None and appname:
            quote_app = self.quote_args(appname)
            url = url % quote_app

        if tree:
            #获取页面dom树
            etree = self.get_elemtree(url, data, headers)
        else:
            #获取response的 raw string
            etree = self.get_content(url, data, headers)
        return etree

    def verify_app(self, url=None, down_link=None, chksum=None):
        """
        url: detail页面链接
        down_link: 下载链接
        chsksum: 校验和
        """
        #如果没有传入down_link,就需要向detail页面发送请求
        if not down_link and url:
            etree = self.send_request(url=url)
            down_link = etree.xpath(self.down_xpath)[0]
        storage = self.download_app(down_link)
        return storage


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

    def run(self, url, headers=None):
        storage = self.get_storage()
        content = self.get_content(url, headers=headers)
        with open(storage, 'a') as f:
            f.write(content)
            f.flush()
        return storage


class ChannelSpider(CreeperBase):

    def send_request(self, url, headers=None, tree=True):
        if tree:
            #获取页面dom树
            etree = self.get_elemtree(url, headers)
        else:
            #获取response的 raw string
            etree = self.get_content(url, headers)
        return etree


if __name__ == "__main__":
    #url = "http://apps.wandoujia.com/apps/net.myvst.v2/download"
    url = "http://pc1.gamedog.cn/big/online/juese/233490/tiantianaixiyouyxdog_an.apk"
    domain = "apps.wandoujia.com"
    referer = "www.oyksoft.com/soft/32456.html"
    downloader = DownloadAppSpider()
    print downloader.run(url)
