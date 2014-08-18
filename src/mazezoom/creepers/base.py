# -*- coding:utf-8 -*-

#StdLib imports
import time
import random
import urllib
import urllib2
import urlparse
from lxml.html import fromstring

#From Projects
from constants import USER_AGENTS, MAX_RETRY_TIMES


class PositionSpider(object):
    chartset = DEFAULT_CHARSET

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

    def get_content(self, url):
        """
        给请求加载USER-AGENT, 获取页面内容，
        """
        ua = random.choice(USER_AGENTS)
        headers = {'User-Agent': ua}
        req = urllib2.Request(url=url, headers=headers)
        try:
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            if e.code == 503:
                time.sleep(30)
                content = self.tryAgain(req, 0)
        except:
            time.sleep(30)
            content = self.tryAgain(req, 0)
        return content

    def normalize_url(source, url):
        """
        >>> urlparse.urljoin('http://www.baidu.com/?a=1', '/page/1?query=a')
            http://www.baidu.com/page/1?query=a
        >>> urlparse.urljoin('http://www.baidu.com/?a=1', 'http://www.baidu.com/page/1?query=a')
            http://www.baidu.com/page/1?query=a
        """
        return urlparse.urljoin(source, url)

    def get_elemtree(self, url):
        """
        生成dom树方便xpath分析
        """
        etree = None
        content = self.get_content(url)
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

    def send_request(self, appname):
        #按照网站charset编码参数
        quote_app = self.quote_args(appname)
        url = self.search_url % quote_app

        #获取页面dom树
        etree = self.get_elemtree(url)
        return etree

    def run(self):
        """
        接口子类实现
        """
        pass
