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

class AngeeksPosition(PositionSpider):
    domain = "apk.angeeks.com"
    charset = 'gb2312'
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
            print link, title
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
    """
    Ajax
    """
    domain = "sj.qq.com"
    #search_url = "http://sj.qq.com/myapp/search.htm?kw=%s"
    search_url = "http://sj.qq.com/myapp/searchAjax.htm?kw=%E7%BD%91%E6%98%93&pns=&sid="
    xpath = "//a"

    def run(self, appname):
        results = []
	etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
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

class CrskyPosition(PositionSpider):
    """
    搜索结果比页面展示条目要少
    """
    domain = "www.crsky.com"
    charset = 'gb2312'
    search_url = "http://sj.crsky.com/query.aspx?keyword=%s&type=android"
    xpath = "//div[@class='right']//a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
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

class AndroidcnPosition(PositionSpider):
    """
    应用、游戏、资讯、壁纸、主题使用不同二级域名
    列表页与结果页下载次数不一致
    """
    domain = "www.androidcn.com"
    search_url = "http://down.androidcn.com/search/q/%s"
    xpath = "//div[@class='app-info']/h2/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class ApkcnPosition(PositionSpider):
    domain = "www.apkcn.com"
    search_url = "http://www.apkcn.com/search/"
    xpath = "//div[@class='box']/div[@class='post indexpost']/h3/a"

    def run(self, appname):
        results = []
        data = {'keyword': appname.encode(self.charset), 'select': 'all'}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class SohoPosition(PositionSpider):
    domain = "download.sohu.com"
    search_url = "http://download.sohu.com/search?words=%s"
    xpath = "//div[@class='yylb_box']/div[@class='yylb_main']/p[@class='yylb_title']/strong/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class ShoujiPosition(PositionSpider):
    """
    应用和游戏分类搜索，域名不同，无下载次数
    """
    domain = "soft.shouji.com.cn"
    domain1 = "game.shouji.com.cn"
    search_url = (
        "http://soft.shouji.com.cn/sort/search.jsp"
        "?html=soft"
        "&phone=100060" #100060代表安卓平台
        "&inputname=soft"
        "&softname=%s"
        "&thsubmit=搜索"
    )
    search_url1 = (
        "http://game.shouji.com.cn/gamelist/list.jsp"
        "?html=soft"
        "&phone=100060"
        "&inputname=game"
        "&gname=%s"
        "&thsubmit=搜索"
    )
    xpath = "//div[@id='bklist']//li[@class='bname']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        #items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        for item in items2:
            link = self.normalize_url(self.search_url1, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

#error
class Mobile1Position(PositionSpider):
    """
    json
    """
    domain = "www.1mobile.tw"
    #search_url = "http://www.1mobile.tw/index.php?c=search.index&keywords=%s"
    search_url = "http://www.1mobile.tw/index.php?c=search.json&keywords=%s&page=1"
    xpath = "//div[@class='list_item']//a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class OnlineDownPosition(PositionSpider):
    """
    排行列表页有下载量，搜索列表页无，结果页无
    """
    domain = "www.onlinedown.net"
    search_url = (
        "http://search.newhua.com/search_list.php"
        "?searchname=%s"
        "&searchsid=6"
        "&app=search"
        "&controller=index"
        "&action=search"
        "&type=news"
    )
    xpath = "//div[@class='title']/strong/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class EoemarketPosition(PositionSpider):
    domain = "www.eoemarket.com"
    search_url = "http://www.eoemarket.com/search_.html?keyword=%s&pageNum=1"
    xpath = "//ol[@class='RlistName']/li[1]/span/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class ApkolPosition(PositionSpider):
    """
    结果页打开慢，安装次数
    """
    domain = "www.apkol.com"
    search_url = "http://www.apkol.com/search?keyword=%s"
    xpath = "//div[@class='listbox ty']/div[@class='yl_pic']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.attrib['title']
            results.append((link, title))
            print link, title
        return results

class BkillPosition(PositionSpider):
    domain = "www.bkill.com"
    charset = 'gb2312'
    search_url = "http://www.bkill.com/d/search.php?mod=do&n=1"
    xpath = "//div[@class='clsList']/dl/dt/a"

    def run(self, appname):
        results = []
        data = {
            'keyword': appname.encode(self.charset),
            'area': 'name',
            'category': '0',
            'field[condition]': 'Android',
            'order': 'downcount', #updatetime
            'submit': '搜 索',
            'way': 'DESC'
        }
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

if __name__ == "__main__":
    #haipk = HaipkPosition()
    #print haipk.run(u'微信')

    #gfan = GfanPosition()
    #print gfan.run(u'微信')

    #apk91 = Apk91Position()
    #print apk91.run(u'微信')

    #angeeks = AngeeksPosition()
    #print angeeks.run(u'刀塔')
    
    #it168 = It168Position()
    #print it168.run(u'微信')

    #pchome = PcHomePosition()
    #print pchome.run(u'微信')

    #qq = QQPosition()
    #print qq.run(u'qq')

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
    #print crsky.run(u'腾讯')
 
    #d = DPosition()
    #print d.run(u'网易')

    #androidcn = AndroidcnPosition()
    #print androidcn.run(u'腾讯')

    #apkcn = ApkcnPosition()
    #print apkcn.run(u'腾讯')

    #soho = SohoPosition()
    #print soho.run(u'捕鱼')

    #shouji = ShoujiPosition()
    #print shouji.run(u'腾讯')

    #mobile1 = Mobile1Position()
    #print mobile1.run(u'qq')

    #onlinedown = OnlineDownPosition()
    #print onlinedown.run(u'腾讯')

    #eoemarket = EoemarketPosition()
    #print eoemarket.run(u'腾讯')

    #borpor = BorPorPosition()
    #print borpor.run(u'网易')

    #apkol = ApkolPosition()
    #print apkol.run(u'腾讯')

    #bkill = BkillPosition()
    #print bkill.run(u'网易')
