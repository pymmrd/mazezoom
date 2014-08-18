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
        etree = self.send_request(appname)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        return [(item.xpath(self.link_xpath)[0], item.xpath(self.title_xpath)[0].text_content()) for item in items]


class GameDogPosition(PositionSpider):
    domain = "www.gamedog.cn"
    search_url = "http://zhannei.gamedog.cn/cse/search?s=10392184185092281050&entry=1&q=%s"
    xpath = "//a[@class='result-game-item-title-link']"

    def run(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        return [(item.attrb('href'), item.text_content()) for item in items]


class Positon365(PositionSpider):
    charset = 'gbk'
    domain = "www.365xz8.cn"
    search_url = "http://www.365xz8.cn/soft/search.asp?act=topic&keyword=%s"
    xpath = "//div[@class='searchTopic']/a"

    def run(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        return [(item.attrb('href'), item.text_content()) for item in items]


class Mm10086Position(PositionSpider):
    domain = "mm.10086.cn"
    search_url = "http://mm.10086.cn/searchapp?dt=android&advanced=0&st=3&q=%s"
    xpath = "//dd[@class='sr_searchListConTt']/h2/a"

    def run(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        return [(item.attrb('href'), item.text_content()) for item in items]


class Hack50Positon(PositionSpider):
    domain = "www.hack50.com"
    charset = 'gbk'
    search_url = "http://so.hack50.com/cse/search?s=1849264326530945843&ie=gbk&q=%s&m=2&x=20&y=12"
    xpath = "//h3[@class='c-title']/a"

    def run(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        return [(item.attrb('href'), item.text_content()) for item in items]


class Position520Apk(PositionSpider):
    domain = "www.520apk.com"
    search_url = "http://search.520apk.com/cse/search?s=17910776473296434043&q=%s"
    xpath = "//h3[@class='c-title']/a"

    def run(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        return [(item.attrb('href'), item.text_content()) for item in items]


class Apk3Position(PositionSpider):
    domain = "www.apk3.com"
    search_url = "http://www.apk3.com/search.asp?m=2&s=0&word=%s&x=0&y=0"
    xpath = "//div[@class='searchTopic']/a"

    def run(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        return [(item.attrb('href'), item.text_content()) for item in items]
    

if __name__ == "__main__":
    oyk = OyksoftPosition()
    print oyk.run(u'迅雷')
