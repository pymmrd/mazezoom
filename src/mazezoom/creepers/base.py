# -*- coding:utf-8 -*-

#StdLib imports
import os
import time
import random
import urllib
import urllib2
import shortuuid
import urlparse
from datetime import datetime
from lxml.html import fromstring

#From Projects
from constants import (USER_AGENTS, MAX_RETRY_TIMES, DEFAULT_CHARSET,
                       POSITION_APP_DIR, CHANNAL_APP_DIR)


class CreeperBase(object):
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
        ua = random.choice(USER_AGENTS)
        if headers:
            headers['User-Agent'] = ua
        else:
            headers = {'User-Agent': ua}
        req = urllib2.Request(url=url, data=data, headers=headers)
        try:
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            print e
            if e.code == 503:
                time.sleep(0.1)
                content = self.tryAgain(req, 0)
        except:
            time.sleep(0.1)
            content = self.tryAgain(req, 0)
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

    def run(self):
        """
        接口子类实现
        """
        pass


class PositionSpider(CreeperBase):
    charset = DEFAULT_CHARSET

    def send_request(self, appname=None, url=None, data=None, headers=None):
        #按照网站charset编码参数
        url = self.search_url if url is None else url
        if data is None:
            #GET 请求
           # if self.charset == DEFAULT_CHARSET:
           #      quote_app = appname.encode(self.charset)
           #else:
            quote_app = self.quote_args(appname)
            url = url % quote_app
        else:
            data = urllib.urlencode(data)
        #获取页面dom树
        etree = self.get_elemtree(url, data, headers)
        return etree


class DownloadAppSpider(CreeperBase):

    def get_storage(self, is_position=False):
        today = datetime.today()
        unique_dir = self.unique_name()
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


    def run(self, url, domain=None, referer=None, headers=None):
        storage = self.get_storage()
        content = self.get_content(url, headers=headers)
        with open(storage, 'a') as f:
            f.write(content)
            f.flush()
        return storage


class ChannelSpider(CreeperBase):

    def send_request(self, url, headers=None):

        if headers is None:
            headers = {}
        if 'Host' not in headers:
            headers['Host'] = self.domain
        if 'Referer' not in headers:
            headers['Referer'] = self.domain

        etree = self.get_elemtree(url, headers=headers)
        return etree


if __name__ == "__main__":
    url = "http://apps.wandoujia.com/apps/net.myvst.v2/download"
    domain = "apps.wandoujia.com"
    referer = "www.oyksoft.com/soft/32456.html"
    downloader = DownloadAppSpider()
    print downloader.run(url, domain, referer)
