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

    def tryAgain(self, req, retries=0):
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
        return urlparse.urljoin(source, url)

    def get_elemtree(self, url):
        etree = None
        content = self.get_content(url)
        if content:
            try:
                etree = fromstring(content)
            except:
                pass
        return etree

    def quote_args(self, appname):
        return urllib.quote(appname.encode(self.charset))

    def run(self):
        pass
