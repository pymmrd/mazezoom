# -*- coding:utf-8 -*-

from base import PositionSpider


class OyksoftPosition(PositionSpider):
    domain = "www.oyksoft.com"
    charset = 'gbk'
    search_url = "http://www.oyksoft.com/GoogleSearch.html?q=%s"
    base_xpath = "//table[@class='gsc-table-result']/tbody/tr/td[@class='gsc-table-cell-snippet-close']"
    title_xpath = "child::div[@class='gs-title gsc-table-cell-thumbnail gsc-thumbnail-left']/a[@class='gs-title']"
    link_xpath = "child::div[@class='gs-title gsc-table-cell-thumbnail gsc-thumbnail-left']/a[@class='gs-title']/@href"

    def run(self, appname):
        quote_app = self.quote_args(appname)
        url = self.search_url % quote_app
        etree = self.get_elemtree(url)
        items = etree.xpath(self.base_xpath)
        return [(item.xpath(self.link_xpath)[0], item.xpath(self.title_xpath)[0].text_content()) for item in items]


if __name__ == "__main__":
    oyk = OyksoftPosition()
    print oyk.run(u'迅雷')
    
