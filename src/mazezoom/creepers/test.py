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

url = "http://www.oyksoft.com/GoogleSearch.html?q=%D1%B6%C0%D7"
base_xpath = "//table[@class='gsc-table-result']/tbody/tr/td[@class='gsc-table-cell-snippet-close']"
title_xpath = "child::div[@class='gs-title gsc-table-cell-thumbnail gsc-thumbnail-left']/a[@class='gs-title']"
link_xpath = "child::div[@class='gs-title gsc-table-cell-thumbnail gsc-thumbnail-left']/a[@class='gs-title']/@href"
ua = random.choice(USER_AGENTS)
print ua

req = urllib2.Request(url, headers={'User-Agent':ua})

content = urllib2.urlopen(req).read()
dom = fromstring(content)
items = dom.xpath(base_xpath)
for item in items:
    print item.xpath(link_xpath)[0], item.xpath(title_xpath)[0].text_content()
