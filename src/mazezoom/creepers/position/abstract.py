# -*- coding:utf-8 -*-
#Author: zoug
#Email: b.zougang@gmail.com
#Date: 2014/08/18

"""
渠道搜索爬虫：
    1. 以各渠道的搜索作为入口,输入应用程序名称进行搜索，
       支持GET和POST请求,对特定渠道需要伪装headers.
    2. 各渠道搜索质量不一，可以加入各种特征进行准确定位.
    3. 获取软件的下载地址.
    4. 下载软件进行md5值匹配.
    5. 注意搜索页面的下载次数和detail页面的下载次数
    修订记录：
        2014/08/23 增加verify_app渠道通过md5验证功能
"""
import re
import json
import fchksum

if __name__ == '__main__':
    import os
    import sys
    current_path = os.path.abspath(os.path.dirname(__file__))
    creepers_path = os.path.abspath(os.path.dirname(current_path))
    sys.path.append(creepers_path)
from base import PositionSpider


class Position365Nokia(PositionSpider):
    """
    >>>nokia365 = Position365Nokia()
    >>>nokia365.run(u'HTC')
    """
    domain = "www.365nokia.cn"
    search_url = "http://www.365nokia.cn/search.asp?q=%s"
    xpath = "//div[@class='list-r']/ur/li/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.app_name in title:
                results.append((link, title))
        return results

class MyFilesPosition(PositionSpider):

    """
    pc渠道
    >>>myfiles = MyFilesPosition()
    >>>myfiles.run(u'驱动精灵')
    """

    domain = "www.myfiles.com.cn"
    search_url = "http://so.myfiles.com.cn/soft.aspx?q=%s&Submit2="
    xpath = ("//div[@class='rj-list']/div[@class='list1']"
             "/ul/li[@class='rjbt']/a")
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class WapMyPosition(PositionSpider):
    """
    Symbian
    >>>wap = WapMyPosition()
    >>>wap.run(u'360手机卫士')
    """

    domain = "www.wapmy.cn"
    search_url = "http://www.wapmy.cn/wapmys/webmy/search.jsp"
    xpath = "//p[@class='listname']/b/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.attrib['title']
            results.append((link, title))
        return results


class DownBankPosition(PositionSpider):
    """
    PC客户端
    >>>downbank = DownBankPosition()
    >>>downbank.run(u'金山毒霸')
    """
    charset = 'gb2312'
    domain = "www.downbank.cn"
    search_url = "http://www.downbank.cn/search.asp?keyword=%s&x=38&y=10"
    xpath = "//div[@class='searchTopic']/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class AndroidZonePosition(PositionSpider):
    """
    回复后下载
    >>>az = AndroidZonePosition()
    >>>az.run(u'手机QQ')
    """
    charset = "gbk"
    domain = "andorid.zone.it.sohu.com"
    search_url = ("http://android.zone.it.sohu.com/search.php"
                  "?mod=forum&searchid=204468&orderby=lastpost"
                  "&ascdesc=desc&searchsubmit=yes&kw=%s")
    search_url1 = ("http://android.zone.it.sohu.com/search.php"
                   "?mod=forum&searchid=204469&orderby=lastpost"
                   "&ascdesc=desc&searchsubmit=yes&kw=%s")
    xpath = "//li[@class='pbw']/h3[@class='xs3']/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpatH(self.xpath)
        for item in items.extend(items2):
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class App111Position(PositionSpider):
    """
    ios
    >>>app = App111Position()
    >>>app.run(u'K歌达人')
    """

    domain = "www.app111.com"
    search_url = "http://www.app111.com/search?k=%s"
    xpath = "//div[@class='Apper_contain3_1']/ul/li/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.attrib['title']
            results.append((link, title))
        return results




class MaoRen8Position2(PositionSpider):
    """
    >>>maoren8 = MaoRen8Position()
    >>>maoren8.run(u'全名水浒')
    """
    charset = 'gb2312'
    domain = "www.maoren8.com"
    search_url = "http://www.maoren8.com/game/"
    link_xpath = "//div[@class='game-list-hidden animat-out']/a"
    title_xpath = "child::h2/text()"
    abstract = True

    def position(self):
        results = []
        data = {
            'monder': '1',
            'orderview': '3',
            'search_subject': self.app_name.encode(self.charset)
        }
        headers = {
            'Host': self.domain,
            'Referer': 'http://www.maoren8.com/game-3-0-0-0-0-0-3-0-1-0/',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept': ('text/html,application/xhtml+xml'
                       ',application/xml;q=0.9,*/*;q=0.8'),
            'Accept-Language': ('zh-cn,es-ar;q=0.8,fr-be;'
                                'q=0.6,en-us;q=0.4,en;q=0.2'),
        }
        etree = self.send_request(data=data, headers=headers)
        items = etree.xpath(self.link_xpath)
        for item in items:
            link = item.attrib['href']
            title = item.xapth(self.title_xpath)[0]
            results.append((link, title))
        return results


class Wei2008Position(PositionSpider):
    """
    """
    abstract = True
    domain = "www.wei2008.com"


class Zx181Position(PositionSpider):
    """
    搜索不可用，可能需要深度定制
    """
    abstract = True
    domain = "www.zx181.cn"

    def position(self):
        pass


class BBSLidroidPosition(PositionSpider):
    """
    """
    abstract = True
    domain = "bbs.lidroid.com"


class Position189Store(PositionSpider):
    """
    搜索不可用
    """
    abstract = True
    domain = "www.189store.com"


class ShouYouPosition(PositionSpider):
    domain = "shouyou.178.com"
    url = "http://shouyou.178.com/list/android.html"
    abstract = True

    def position(self):
        pass


class Position07cn(PositionSpider):
    domain = "www.07cn.com"
    abstract = True

    def position(self):
        pass


class Position52SamSung(PositionSpider):
    domain = "bbs.52samsung.com"
    search_url = ""
    abstract = True

    def position(self):
        pass


class SjrjyPosition(PositionSpider):
    domain = "www.sjrjy.com"
    search_url = ""
    abstract = True

    def position(self):
        pass


class Postion92Apk(PositionSpider):
    """
    搜索不可用，需深度定制
    """
    charset = "gbk"
    domain = "www.92apk.com"
    search_url = ""
    abstract = True


class AndroidtgbusPosition(PositionSpider):
    """
    无搜索，需要深度定制
    """
    charset = ""
    domain = "android.tgbus.com"
    abstract = True


class AnDuoWanPosition(PositionSpider):
    """
    搜索质量不高
    """
    abstract = True
    domain = "an.duowan.com"


class SoYingYongPosition(PositionSpider):
    """
    搜索栏无法使用，可能需要深度定制
    """
    domain = "www.soyingyong.com"
    search_url = "http://www.soyingyong.com/apps/search/%s.html"
    abstract = True

    def position(self):
        pass


class Android265gPosition(PositionSpider):
    """
    深度定制
    """
    abstract = True
    domain = "http://android.265g.com/soft/"

    def position(self):
        pass


class ImmikepPosition(PositionSpider):
    """
    深度定制
    """
    domain = "www.immikep.com"
    abstract = True

    def position(self):
        pass


class XtzhongdaPosition(PositionSpider):
    """
    深度定制
    """
    domain = "www.xtzhongda.com"
    abstract = True

    def position(self):
        pass


class DreamsDownPosition(PositionSpider):
    domain = "www.dreamsdown.com"
    charset = 'gbk'
    search_url = (
        "http://search.discuz.qq.com/f/discuz"
        "?mod=curforum&formhash=096d51fb"
        "&srchtype=title&srhfid=170"
        "&srhlocality=forum%3A%3Aforumdisplay&sId=19235686"
        "&ts=1408356224&cuId=0&cuName="
        "&gId=7&agId=0&egIds=&fmSign=&ugSign7="
        "&sign=7e9565583d199fecff9503b381840530"
        "&charset=gbk&source=discuz"
        "&fId=170&q=%s&srchtxt=%s&searchsubmit=true"
    )
    xpath = "//h3[@class='title']/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Hack50Positon(PositionSpider):
    """
    pc端下载包
    >>>hack50 = Hack50Positon()
    >>>hack50.run(u'qq')
    """
    quanlity = 4
    domain = "www.hack50.com"
    charset = 'gbk'
    search_url = ("http://so.hack50.com/cse/search"
                  "?s=1849264326530945843&ie=gbk&q=%s&m=2&x=20&y=12")
    xpath = "//h3[@class='c-title']/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Position365(PositionSpider):
    """
    pc端下载资源
    >>>p365 = Position365()
    >>>p365.run(u'金蝶KIS')
    """
    quanlity = 4
    charset = 'gbk'
    domain = "www.365xz8.cn"
    search_url = "http://www.365xz8.cn/soft/search.asp?act=topic&keyword=%s"
    xpath = "//div[@class='searchTopic']/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class IappsPosition(PositionSpider):
    """
    IOS渠道
    >>>iapps = IappsPosition()
    >>>iapps.run(u'没有刹车')
    """
    domain = "www.iapps.com"
    search_url = "http://www.iapps.im/search/%s"
    xpath = "//h2[@class='entry-title']/a"
    abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class MaoRen8Position(PositionSpider):
    charset = 'gb2312'
    domain = "www.maoren8.com"
    search_url = "http://www.maoren8.com/searcher/"
    xpath = "//div[@id='card_box_list']/ul/li/div[@class='card_title']/a"
    abstract = True

    def position(self):
        results = []
        data = {'search_subject': self.quote_args(self.app_name)}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

