# -*- coding:utf-8 -*-

from base import PositionSpider

class HaipkPosition(PositionSpider):
    domain = "apk.haipk.com"
    search_url = "http://apk.hiapk.com/search?key=%s"
    xpath = "//span[@class='list_title font12']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class GfanPosition(PositionSpider):
    domain = "apk.gfan.com"
    search_url = "http://apk.gfan.com/search?q=%s"
    xpath = "//span[@class='apphot-tit']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class Apk91Position(PositionSpider):
    domain = "apk.gfan.com"
    search_url = "http://apk.91.com/soft/android/search/1_5_0_0_%s"
    xpath = "//div[@class='zoom']/h4/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

#error
class AngeeksPosition(PositionSpider):
    domain = "apk.angeeks.com"
    #charset = 'gb2312'
    search_url = "http://apk.angeeks.com/search?keywords=%s&x=0&y=0"
    xpath = "//div[@class='info']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class It168Position(PositionSpider):
    domain = "down.it168.com"
    charset = 'gb2312'
    search_url = "http://down.it168.com/soft_search.html?keyword=%s"
    xpath = "//div[@class='r3']/ul/li/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class PcHomePosition(PositionSpider):
    domain = "download.pchome.net"
    #charset = 'gbk'
    search_url = "http://download.pchome.net/search-%s---0-1.html"
    xpath = "//div[@class='tit']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

#error
class QQPosition(PositionSpider):
    domain = "sj.qq.com"
    search_url = "http://sj.qq.com/myapp/search.htm?kw=%s"
    xpath = "//a[@class='appName']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class MumayiPosition(PositionSpider):
    domain = "android.mumayi.com"
    search_url = "http://s.mumayi.com/index.php?q=%s"
    xpath = "//ul[@class='applist']//h3[@class='hidden']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class SkycnPosition(PositionSpider):
    domain = "www.skycn.com"
    search_url = "http://shouji.baidu.com/s?wd=%s&data_type=app&from=as"
    xpath = "//a[@class='app-name']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class ZolPosition(PositionSpider):
    domain = "sj.zol.com.cn"
    charset = 'gbk'
    search_url = "http://xiazai.zol.com.cn/search?wd=%s&type=1"
    xpath = "//ul[@class='results-text']/li[@class='item']/div[@class='item-header clearfix']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class SinaPosition(PositionSpider):
    domain = "tech.sina.com.cn"
    charset = 'gb2312'
    search_url = "http://down.tech.sina.com.cn/3gsoft/iframelist.php?classid=0&keyword=%s&tag=&osid=4"
    xpath = "//div[@class='b_txt']/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class DuotePosition(PositionSpider):
    domain = "www.duote.com"
    charset = 'gb2312'
    search_url = "http://www.duote.com/searchPhone.php?searchType=&so=%s"
    xpath = "//div[@class='list_item']/div[@class='tit_area']/span[@class='name']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class ImobilePosition(PositionSpider):
    domain = "www.imobile.com.cn"
    search_url = "http://app.imobile.com.cn/android/search/%s.html"
    xpath = "//ul[@class='ranking_list']/li/div[@class='ico']/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class ApkzuPosition(PositionSpider):
    domain = "www.apkzu.com"
    charset = 'gb2312'
    search_url = "http://www.apkzu.com/search.asp?k=%s&c=1"
    xpath = "//div[@class='recList']/div[@class='recSinW btmLine1']/dl/dt/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class NduoaPosition(PositionSpider):
    domain = "www.nduoa.com"
    search_url = "http://www.nduoa.com/search?q=%s"
    xpath = "//ul[@class='apklist clearfix']//div[@class='name']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class Android115Position(PositionSpider):
    domain = "www.155.cn"
    charset = 'gb2312'
    search_url = "http://android.155.cn/search.php?kw=%s&index=soft"
    xpath = "//ul[@class='gmc-c']/li/strong/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class Shop985Position(PositionSpider):
    """
    搜索结果没有区分平台
    """
    domain = "d.958shop.com"
    charset = 'gb2312'
    search_url = "http://d.958shop.com/search/?keywords=%s&cn=soft"
    xpath = "//span[@class='t_name01']/a[@class='b_f']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class LiqucnPosition(PositionSpider):
    """
    根据Cookie或者referer来区别用户手机系统
    """
    domain = "www.liqucn.com"
    android_referer = 'http://os-android.liqucn.com/'
    search_url = "http://search.liqucn.com/download/%s"
    xpath = "//li[@class='appli_info']/a"

    def run(self, appname):
        results = []
        headers = {'Referer': self.android_referer}
        etree = self.send_request(appname, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

#erro英文有结果，中文没有结果
class CrskyPosition(PositionSpider):
    domain = "www.crsky.com"
    charset = 'gb2312'
    search_url = "http://sj.crsky.com/query.aspx?keyword=%s&type=android"
    #xpath = "//div[@class='list_block app_wrap']//div[@class='right']//a"
    xpath = "//a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class DPosition(PositionSpider):
    domain = "www.d.cn"
    search_url = "http://android.d.cn/search/app/?keyword=%s"
    xpath = "//p[@class='g-name']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

if __name__ == "__main__":
    #haipk = HaipkPosition()
    #print haipk.run(u'微信')

    #gfan = GfanPosition()
    #print gfan.run(u'微信')

    #apk91 = Apk91Position()
    #print apk91.run(u'微信')

    #angeeks = AngeeksPosition()
    #print angeeks.run(u'微信')
    
    #it168 = It168Position()
    #print it168.run(u'微信')

    #pchome = PcHomePosition()
    #print pchome.run(u'微信')

    #qq = QQPosition()
    #print qq.run(u'网易')

    #mumayi = MumayiPosition()
    #print mumayi.run(u'微信')

    #skycn = SkycnPosition()
    #print skycn.run(u'微信')
  
    #zol = ZolPosition()
    #print zol.run(u'网易')

    #sina = SinaPosition()
    #print sina.run(u'新浪')

    #duote = DuotePosition()
    #print duote.run(u'网易')

    #imobile = ImobilePosition()
    #print imobile.run(u'微信')

    #apkzu = ApkzuPosition()
    #print apkzu.run(u'网易')

    #nduoa = NduoaPosition()
    #print nduoa.run(u'资讯')

    #android115 = Android115Position()
    #print android115.run(u'网易')

    #shop985 = Shop985Position()
    #print shop985.run(u'网易')

    #liqucn = LiqucnPosition()
    #print liqucn.run(u'腾讯')

    #crsky = CrskyPosition()
    #print crsky.run(u'网易')
 
    d = DPosition()
    print d.run(u'网易')
