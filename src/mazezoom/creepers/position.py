# -*- coding:utf-8 -*-

from base import PositionSpider


class OyksoftPosition(PositionSpider):
    domain = "www.oyksoft.com"
    charset = 'gbk'
    search_url = "http://www.oyksoft.com/GoogleSearch.html?q=%s"
    base_xpath = ("//table[@class='gsc-table-result']/tbody/"
                  "tr/td[@class='gsc-table-cell-snippet-close']")
    title_xpath = ("child::div[@class='gs-title gsc-table-cell-thumbnail"
                   " gsc-thumbnail-left']/a[@class='gs-title']")
    link_xpath = ("child::div[@class='gs-title gsc-table-cell-thumbnail"
                  " gsc-thumbnail-left']/a[@class='gs-title']/@href")

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            link = item.xpath(self.link_xpath)[0]
            title = item.xpath(self.title_xpath)[0].text_content()
            results.append((link, title))
        return results


class GameDogPosition(PositionSpider):
    domain = "www.gamedog.cn"
    search_url = ("http://zhannei.gamedog.cn/cse/search"
                  "?s=10392184185092281050&entry=1&q=%s")
    xpath = "//a[@class='result-game-item-title-link']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Positon365(PositionSpider):
    charset = 'gbk'
    domain = "www.365xz8.cn"
    search_url = "http://www.365xz8.cn/soft/search.asp?act=topic&keyword=%s"
    xpath = "//div[@class='searchTopic']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Mm10086Position(PositionSpider):
    domain = "mm.10086.cn"
    search_url = "http://mm.10086.cn/searchapp?dt=android&advanced=0&st=3&q=%s"
    xpath = "//dd[@class='sr_searchListConTt']/h2/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Hack50Positon(PositionSpider):
    domain = "www.hack50.com"
    charset = 'gbk'
    search_url = ("http://so.hack50.com/cse/search"
                  "?s=1849264326530945843&ie=gbk&q=%s&m=2&x=20&y=12")
    xpath = "//h3[@class='c-title']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Position520Apk(PositionSpider):
    domain = "www.520apk.com"
    search_url = ("http://search.520apk.com/cse/search"
                  "?s=17910776473296434043&q=%s")
    xpath = "//h3[@class='c-title']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Apk3Position(PositionSpider):
    domain = "www.apk3.com"
    search_url = "http://www.apk3.com/search.asp?m=2&s=0&word=%s&x=0&y=0"
    xpath = "//div[@class='searchTopic']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class DownzaPosition(PositionSpider):
    charset = 'gb2312'
    domain = "www.downza.cn"
    search_url = "http://www.downza.cn/search?k=%s"
    xpath = "//div[@class='soft_list mb_20 clearfix']/dl/dd/h2/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class AnZhiPosition(PositionSpider):
    domain = "www.anzhi.com"
    search_url = "http://www.anzhi.com/search.php?keyword=%s&x=0&y=0"
    xpath = "//span[@class='app_name']/a"

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
    domain = "www.angeeks.com"
    search_url = "http://apk.angeeks.com/search?keywords=%s&x=29&y=15"
    xpath = "//dd/div[@class='info']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class JiQiMaoPosition(PositionSpider):
    domain = "jiqimao.com"
    search_url = "http://jiqimao.com/search/index?a=game&w=%s"
    search_url2 = "http://jiqimao.com/search/index?a=soft&w=%s"
    xpath = "//div[@class='applist']/li/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url2)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        for item in items.extend(items2):
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class IappsPosition(PositionSpider):
    domain = "www.iapps.com"
    search_url = "http://www.iapps.im/search/%s"
    xpath = "//h2[@class='entry-title']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
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

    def run(self, appname):
        results = []
        data = {'search_subject': self.quote_args(appname)}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class SjapkPosition(PositionSpider):
    charset = 'gb2312'
    domain = "www.sjapk.com"
    search_url = "http://www.sjapk.com/Search.asp"
    xpath = "//li/span/h1/a"

    def run(self, appname):
        results = []
        data = {'Key': self.quote_args(appname)}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class CoolApkPosition(PositionSpider):
    domain = "www.cookapk.com"
    search_url = "http://www.coolapk.com/search?q=%s"
    xpath = "//li[@class='media']/div[@class='media-body']/h4/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class Position365Nokia(PositionSpider):
    """
    >>>nokia365 = Position365Nokia()
    >>>nokia365.run(u'HTC')
    """
    domain = "www.365nokia.cn"
    search_url = "http://www.365nokia.cn/search.asp?q=%s"
    xpath = "//div[@class='list-r']/ur/li/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class MyFilesPosition(PositionSpider):

    """
    >>>myfiles = MyFilesPosition()
    >>>myfiles.run(u'驱动精灵')
    """

    domain = "www.myfiles.com.cn"
    search_url = "http://so.myfiles.com.cn/soft.aspx?q=%s&Submit2="
    xpath = ("//div[@class='rj-list']/div[@class='list1']"
             "/ul/li[@class='rjbt']/a")

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class WapMyPosition(PositionSpider):

    """
    >>>wap = WapMyPosition()
    >>>wap.run(u'360手机卫士')
    """

    domain = "www.wapmy.cn"
    search_url = "http://www.wapmy.cn/wapmys/webmy/search.jsp"
    xpath = "//p[@class='listname']/b/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.attrib['title']
            results.append((link, title))
        return results


class DownBankPosition(PositionSpider):
    """
    >>>downbank = DownBankPosition()
    >>>downbank.run(u'金山毒霸')
    """
    charset = 'gb2312'
    domain = "www.downbank.cn"
    search_url = "http://www.downbank.cn/search.asp?keyword=%s&x=38&y=10"
    xpath = "//div[@class='searchTopic']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class AndroidZonePosition(PositionSpider):
    """
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpatH(self.xpath)
        for item in items.extend(items2):
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class CrossmoPosition(PositionSpider):
    """
    >>>cs = CrossmoPosition()
    >>>cs.run(u'疯狂的麦咭')
    """
    domain = "www.crossmo.com"
    search_url = ("http://soft.crossmo.com/soft_default.php"
                  "?act=search&searchkey=%s")
    xpath = "//div[@class='infor_centerb1']/div/dl/dt/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.attrib['title']
            results.append((link, title))
        return results


class ShoujiBaiduSpider(PositionSpider):
    """
    >>>shouji = ShoujiBaiduSpider()
    >>>shouji.run(u'HOT市场')
    """
    domain = "shouji.baidu.com"
    search_url = ("http://shouji.baidu.com/s"
                  "?wd=%s&data_type=app&"
                  "f=header_software%40input%40btn_search"
                  "&from=web_alad_5")
    xpath = "//div[@class='top']/a[@class='app-name']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Position7xz(PositionSpider):
    """
    >>>p7xz = Position7xz()
    >>>p7xz.run(u'极品飞车13')
    """
    domain = "www.7xz.com"
    search_url = "http://www.7xz.com/search?q=%s"
    xpath = "//div[@class='caption']/ul/li/a[@class='a2']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class PC6Position(PositionSpider):
    """
    >>>pc6 = PC6Position()
    >>>pc6.run(u'弹跳忍者')
    """
    charset = "gb2312"
    domain = "www.pc6.com"
    search_url = "http://so.pc6.com/?keyword=%s"
    xpath = "//div[@class='baseinfo']/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Position3533(PositionSpider):
    """
    >>>p3533 = Position3533()
    >>>p3533.run(u'功夫西游')
    """
    domain = "www.3533.com"
    search_url = "http://search.3533.com/software?keyword=%s"
    search_url1 = "http://search.3533.com/game?keyword=%s"
    xpath = "//div[@class='appinfo']/a[@class='apptit']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class Apk8Position(PositionSpider):
    """
    >>>apk8 = Apk8Position()
    >>>apk8.run(u'天天跑酷')
    """
    domain = "www.apk8.com"
    search_url = "http://www.apk8.com/search.php"
    xpath = "//div[@class='main_search_pic']/ul/li/strong/a"

    def run(self, appname):
        results = []
        data = {'key': appname.encode(self.charset)}
        headers = {'Host': self.domain, 'Referer': self.search_url}
        etree = self.send_request(data=data, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class XiaZaiZhiJiaPosition(PositionSpider):
    """
    >>>xzzj = XiaZaiZhiJiaPosition()
    >>>xzzj.run(u'微信')
    """

    charset = 'gb2312'
    domain = "www.xiazaizhijia.com"
    search_url = ("http://www.xiazaizhijia.com/search.php"
                  "?kwtype=0&keyword=%s&channel=0")
    xpath = "//div[@class='th-name']/a[@class='green-ico']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class CngbaPosition(PositionSpider):
    """
    >>>cngba = CngbaPosition()
    >>>cngba.run(u'名将决')
    """
    charset = "gb2312"
    domain = "www.cngba.com"
    search_url = "http://down.cngba.com/script/search.php?keyword=%s"
    xpath = "//div[@class='game_Ljj']/strong/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results


class SjwyxPosition(PositionSpider):
    """
    >>>sjwyx = SjwyxPosition()
    >>>sjwyx.run(u'龙印')
    """
    charset = "gb2312"
    domain = "www.sjwyx.com"
    search_url = "http://www.sjwyx.com/so.aspx?keyword=%s"
    base_xpath = "//li[@class='brdr brdb']"
    title_xpath = "child::a[@class='n']/text()"
    other_link = "child::a"
    down_link_token = u'下载'
    abstract = True

    def run(self, appname):
        results = []
        data = {'searchtext': self.quote_args(appname)}
        etree = self.send_request(data=data)
        items = etree.xpath(self.base_xpath)
        for item in items:
            title = item.xpath(self.title_xpath)
            links = item.xpath(self.other_link)
            for link in links:
                if link.text() == self.down_link_token:
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

    def run(self, appname):
        results = []
        data = {
            'monder': '1',
            'orderview': '3',
            'search_subject': appname.encode(self.charset)
        }
        headers = {
            'Host': self.domain,
            'Referer': 'http://www.maoren8.com/game-3-0-0-0-0-0-3-0-1-0/',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-cn,es-ar;q=0.8,fr-be;q=0.6,en-us;q=0.4,en;q=0.2',
        }
        etree = self.send_request(data=data, headers=headers)
        items = etree.xpath(self.link_xpath)
        for item in items:
            link = item.attrib['href']
            title = item.xapth(self.title_xpath)[0]
            results.append((link, title))
        return results


class Ruan8Position(PositionSpider):
    """
    >>>ruan8 = Ruan8Position()
    >>>ruan8.run(u'360')
    """
    charset = 'gbk'
    domain = "soft.anruan.com"
    search_url = "http://www.anruan.com/search.php?t=all&keyword=%s"
    xpath = "//div[@class='li']/ul/li/a[@class='tit']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results


class PcHomePosition(PositionSpider):
    """
    >>>pchome = PcHomePosition()
    >>>pchome.run(u'微信')
    """
    charset = 'gbk'
    domain = "www.pchome.com"
    search_url = ("http://search.pchome.net/download.php"
                  "?wd=%s&submit=%CB%D1+%CB%F7")
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

    def run(self, appname):
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

    def run(self, appname):
        pass


class Position07cn(PositionSpider):
    domain = "www.07cn.com"
    abstract = True

    def run(self, appname):
        pass


class Position52SamSung(PositionSpider):
    domain = "bbs.52samsung.com"
    search_url = ""
    abstract = True

    def run(self, appname):
        pass


class SjrjyPosition(PositionSpider):
    domain = "www.sjrjy.com"
    search_url = ""
    abstract = True

    def run(self, appname):
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

    def run(self, appname):
        pass


class Android265gPosition(PositionSpider):
    """
    深度定制
    """
    abstract = True
    domain = "http://android.265g.com/soft/"

    def run(self):
        pass


class ImmikepPosition(PositionSpider):
    """
    深度定制
    """
    domain = "www.immikep.com"
    abstract = True

    def run(self, appname):
        pass


class XtzhongdaPosition(PositionSpider):
    """
    深度定制
    """
    domain = "www.xtzhongda.com"
    abstract = True

    def run(self, appname):
        pass


if __name__ == "__main__":
    #oyk = OyksoftPosition()
    #print oyk.run(u'迅雷')

    #p7xz = Position7xz()
    #print p7xz.run(u'极品飞车13')

    #pc6 = PC6Position()
    #print pc6.run(u'弹跳忍者')

    #p3533 = Position3533()
    #print p3533.run(u'功夫西游')

    #apk8 = Apk8Position()
    #print apk8.run(u'天天跑酷')

    #xzzj = XiaZaiZhiJiaPosition()
    #print xzzj.run(u'微信')

    #cngba = CngbaPosition()
    #print cngba.run(u'名将决')
    #sjwyx = SjwyxPosition()
    #print sjwyx.run(u'龙印')

    #maoren8 = MaoRen8Position()
    #print maoren8.run(u'全民水浒')

    ruan8 = Ruan8Position()
    print ruan8.run(u'360')
