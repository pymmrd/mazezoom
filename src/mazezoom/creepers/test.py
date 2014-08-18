# -*-coding:utf-8 -*-

import random
import urllib2
from lxml.html import fromstring


USER_AGENTS = [
    ("Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) "
     "Gecko/20071127 Firefox/2.0.0.11"),
    ("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) "
     "Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"),
    'Opera/9.25 (Windows NT 5.1; U; en)',
]

name = u'一个都不能死'
name = name.encode('utf-8')
url = "http://mm.10086.cn/searchapp?dt=android&advanced=0&st=3&q=%s" % name 
ua = random.choice(USER_AGENTS)

link_xpath = "//dd[@class='sr_searchListConTt']/h2/a"

req = urllib2.Request(url, headers={'User-Agent':ua})

content = urllib2.urlopen(req).read()
dom = fromstring(content)
items = dom.xpath(link_xpath)
for item in items:
    link = item.attrib['href']
    title = item.text_content()
    print link, title

