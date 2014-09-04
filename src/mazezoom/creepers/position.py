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
    修订记录：
        2014/08/23 增加verify_app渠道通过md5验证功能
"""
import re
from base import PositionSpider


class OyksoftPosition(PositionSpider):
    """
    >>>oyk = OyksoftPosition()
    >>>oyk.run(u'腾讯手机管家')
    """
    android_token = 'Android'
    domain = "www.oyksoft.com"
    charset = 'gbk'  # 对传入的appname以此字符集进行编码
    search_url = (
        "http://www.oyksoft.com/search.asp?"
        "action=s&sType=ResName&keyword=%s"
    )
    link_xpath = "child::a/strong"
    down_xpath = "//a[@class='normal']/@href"  # detail
    base_xpath = "//div[@class='searched']/div[@class='title']"
    times_xpath = "//div[@class='softjj']/a[@class='listdbt']/text()"

    def download_times(self, title):
        """
        总下载次数：2444
        """
        seperator = "："
        etree = self.send_request(title)
        item = etree.xpath(self.times_xpath)
        times = None
        if item:
            item = item[0]
            try:
                times = item.split(seperator)[-1]
            except (TypeError, IndexError, ValueError):
                pass
        return times

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            strong = item.xpath(
                self.link_xpath
            )[0]
            parent = strong.getparent()
            link = self.normalize_url(
                self.search_url,
                parent.attrib['href']
            )
            title = item.text_content()
            if self.android_token in title:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class GameDogPosition(PositionSpider):
    """
    >>>gd = GameDogPosition()
    >>>gd.run(u'刀塔传奇')
    """

    quanlity = 10
    android = u'安卓版'
    domain = "www.gamedog.cn"
    search_url = ("http://zhannei.gamedog.cn/cse/search"
                  "?s=10392184185092281050&entry=1&q=%s")
    xpath = "//a[@class='result-game-item-title-link']"
    down_xpath = "//dd[@id='downs_box']/span[1]/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.android in title:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results


class Mm10086Position(PositionSpider):
    """
    >>>mm10086 = Mm10086Position()
    >>>mm10086.run(u'街头足球')
    """
    quanlity = 10
    domain = "mm.10086.cn"
    search_url = "http://mm.10086.cn/searchapp?dt=android&advanced=0&st=3&q=%s"
    base_xpath = "//dd[@class='sr_searchListConTt']"
    xpath = "child::h2/a"
    down_xpath = "child::a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.base_xpath)
        for item in items:
            dom = item.xpath(self.xpath)
            link = self.normalize_url(
                self.search_url,
                dom.attrib['href']
            )
            title = dom.text_content()
            if appname in title:
                down_link = item.xpath(self.down_xpath)[0]
                down_link = self.normalize_url(
                    self.search_url,
                    down_link
                )
                if is_accurate:
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results


class Position520Apk(PositionSpider):
    """
    >>>p520apk = Position520Apk()
    >>>p520apk.run(u'QQ部落')
    """
    quanlity = 7
    domain = "www.520apk.com"
    search_url = ("http://search.520apk.com/cse/search"
                  "?s=17910776473296434043&q=%s")
    xpath = "//h3[@class='c-title']/a"
    url_token = '/android/'  # 通过url token进一步准确定位
    down_xpath = "//a[@class='icon_downbd']/@href"
        #"//a[@class='icon_downdx']/@href",
        #"//a[@class='icon_downlt']/@href",

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if appname in title:
                if self.url_token in link:
                    if is_accurate:
                        match = self.verify_app(link, chksum=chksum)
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results


class Apk3Position(PositionSpider):
    """
    >>>apk3 = Apk3Position()
    >>>apk3.run(u'刷机精灵')
    """
    quanlity = 10
    charset = 'gb2312'
    domain = "www.apk3.com"
    search_url = "http://www.apk3.com/search.asp?m=2&s=0&word=%s&x=0&y=0"
    xpath = "//div[@class='searchTopic']/a"
    down_xpath = "//ul[@class='downlistbox']/li/a/@href"  # Detail

    def verify_app(self, url, chksum):
        etree = self.send_request(url)
        down_link = etree.xpath(self.down_xpath)[0]
        down_link = self.normalize_url(url, down_link)
        storage = self.download_app(down_link)
        return storage

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if appname in title:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(link, chksum)
                    if match:
                        results.append((link, title))
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class DownzaPosition(PositionSpider):
    """
    >>>dza = DownzaPosition()
    >>>dza.run(u'快投')
    """
    quanlity = 10
    charset = 'gb2312'
    domain = "www.downza.cn"
    android_token = "Android"
    andorid_xpath = "//div[@class='bread f_mirco']/a[2]/text()"
    search_url = "http://www.downza.cn/search?k=%s"
    xpath = "//div[@class='soft_list mb_20 clearfix']/dl/dd/h2/a"
    down_xpath = "//div[@class='down_view_down_list fl']/ul/li/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            detail = self.send_request(link)
            android = detail.xpath(self.andorid_xpath)
            if android and android[0].strip() == self.android_token:

                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]

                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results


class AnZhiPosition(PositionSpider):
    """
    >>>anzhi = AnZhiPosition()
    >>>anzhi.run(u'去哪儿')
    """
    quanlity = 10
    domain = "www.anzhi.com"
    search_url = "http://www.anzhi.com/search.php?keyword=%s&x=0&y=0"
    base_xpath = "//div[@class='app_list border_three']/ul/li"
    link_xpath = (
        "child::div[@class='app_info']/"
        "span[@class='app_name']/a/@href"
    )
    title_xpath = (
        "child::div[@class='app_info']/"
        "span[@class='app_name']/a/text()"
    )
    down_xpath = "child::div[@class='app_down']/a/@onclick"
    down_url = "http://www.anzhi.com/dl_app.php?s=%s&n=7"

    def download_link(self, etree):
        #opendown(1322730);
        down_link = ''
        down_text = etree.xpath(self.down_xpath)
        if down_text:
            down_text = down_text[0]
            regx = re.compile('opendown\((?P<pk>\d+)\).+')
            match = regx.match(down_text)
            if match is not None:
                pk = match.group('pk')
                down_link = self.down_url % pk
        return down_link

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.xpath(self.link_xpath)[0]
            )
            title = item.xpath(self.title_xpath)[0]
            down_link = self.download_lin(item)
            if is_accurate:
                match = self.verify_app(
                    down_link=down_link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results


class AngeeksPosition(PositionSpider):
    """
    >>>angeek = AngeeksPosition()
    >>>angeek.run(u'飞机')
    """
    #验证下载个数
    charset = 'gbk'
    quanlity = 10
    domain = "www.angeeks.com"
    search_url = "http://apk.angeeks.com/search?keywords=%s&x=29&y=15"
    base_xpath = "//ul[@id='mybou']/li/dl/dd"
    link_xpath = "child::div[@class='info']/a/@href"
    title_xpath = "child::div[@class='info']/a/text()"
    down_xpath = "child::div[@class='dowl']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.base_xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.xpath(self.link_xpath)[0]
            )
            title = item.xpath(self.title_xpath)[0]
            down_link = item.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
            if is_accurate:  # 精确匹配
                match = self.verify_app(
                    down_link=down_link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results


class JiQiMaoPosition(PositionSpider):
    """
    >>>jiqimao = JiQiMaoPosition()
    >>>jiqimao.run(u'金银岛')
    """
    quanlity = 10
    domain = "jiqimao.com"
    search_url = "http://jiqimao.com/search/index?a=game&w=%s"
    search_url2 = "http://jiqimao.com/search/index?a=soft&w=%s"
    xpath = "//div[@class='applist']/ul/li/a"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url2)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if is_accurate:
                match = self.verify_app(link, chksum=chksum)
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results


class SjapkPosition(PositionSpider):
    """
    >>>sjapk = SjapkPosition()
    >>>sjapk.run(u'喜羊羊之灰太狼闯关')
    """
    quanlity = 10
    charset = 'gb2312'
    domain = "www.sjapk.com"
    search_url = "http://www.sjapk.com/Search.asp"
    xpath = "//li/span/h1/a"
    down_xpath = "//div[@class='main_r_xiazai5']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        data = {'Key': appname.encode(self.charset)}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if is_accurate:
                match = self.verify_app(url=link, chksum=chksum)
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results


class CoolApkPosition(PositionSpider):
    """
    >>>coolapk = CoolApkPosition()
    >>>coolapk.run(u'刀塔传奇')
    """
    quanlity = 10
    domain = "www.coolapk.com"
    search_url = "http://www.coolapk.com/search?q=%s"
    xpath = ("//ul[@class='media-list ex-card-app-list']"
             "/li[@class='media']/div[@class='media-body']/h4/a")
    down_xpath = "//div[@class='ex-page-header']/following::script[1]/text()"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if is_accurate:
                match = self.verify_app(url=link, chksum=chksum)
                if match:
                    results.append((link, title))
            else:
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
    abstract = True

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if appname in title:
                results.append((link, title))
        return results


class CrossmoPosition(PositionSpider):
    """
    >>>cs = CrossmoPosition()
    >>>cs.run(u'LT来电报号')
    """
    quanlity = 10
    domain = "www.crossmo.com"
    search_url = ("http://soft.crossmo.com/soft_default.php"
                  "?act=search&searchkey=%s")
    xpath = "//div[@class='infor_centerb1']/div/dl/dt/a"

    def verify_app(self, url):
        from channel import CrossmoChannel
        cross = CrossmoChannel(url)
        etree = cross.send_request(url)
        appkey = cross.get_appkey(etree)
        appid = cross.get_appid(url)
        donw_link = cross.download_link(appkey, appid)
        if down_link:
            storage = cross.download_app(donwlink,session=self.sesion)
        return storage

    def run(self, appname):
        results = []
        headers = {'Host': 'soft.crossmo.com', 'Referer': 'soft.crossmo.com'}
        etree = self.send_request(appname, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if appname in title:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class ShoujiBaiduSpider(PositionSpider):
    """
    >>>shouji = ShoujiBaiduSpider()
    >>>shouji.run(u'HOT市场')
    """
    quanlity = 10
    domain = "shouji.baidu.com"
    search_url = ("http://shouji.baidu.com/s"
                  "?wd=%s&data_type=app&"
                  "f=header_software@input@btn_search"
                  "&from=web_alad_5")
    xpath = "//div[@class='top']/a[@class='app-name']"
    down_xpath = "//div[@class='area-download']/a[@class='apk']/@href"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if appname in title:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class Position7xz(PositionSpider):
    """
    >>>p7xz = Position7xz()
    >>>p7xz.run(u'极品飞车13')
    """
    quanlity = 10
    domain = "www.7xz.com"
    search_url = "http://www.7xz.com/search?q=%s"
    xpath = "//div[@class='caption']/ul/li/a[@class='a2']"
    down_xpath = "//div[@class='diannao']/a[@class='d_pc_normal_dn']/@href"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                #模糊匹配
                results.append((link, title))
        return results


class PC6Position(PositionSpider):
    """
    >>>pc6 = PC6Position()
    >>>pc6.run(u'弹跳忍者')
    """
    quanlity = 10
    charset = "gb2312"
    domain = "www.pc6.com"
    search_url = "http://www.pc6.com/search2.asp?keyword=%s&searchType=down&rootID=465%2C466"
    xpath = "//div[@class='baseinfo']/h3/a"
    down_xpath = "//div[@class='left2']/a[@class='wdj']/@href"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                #模糊匹配
                results.append((link, title))
        return results


class Position3533(PositionSpider):
    """
    >>>p3533 = Position3533()
    >>>p3533.run(u'功夫西游')
    """
    quanlity = 10
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
            if is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                #模糊匹配
                results.append((link, title))
        return results


class Apk8Position(PositionSpider):
    """
    >>>apk8 = Apk8Position()
    >>>apk8.run(u'天天跑酷')
    """
    quanlity = 10
    domain = "www.apk8.com"
    search_url = "http://www.apk8.com/search.php"
    xpath = "//div[@class='main_search_pic']/ul/li/strong/a"
    down_xpath = "//div[@class='downnew']/a[@class='bt_bd']/@href"

    def run(self, appname):
        results = []
        data = {'key': appname.encode(self.charset)}
        headers = {'Host': self.domain, 'Referer': self.search_url}
        etree = self.send_request(data=data, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                #模糊匹配
                results.append((link, title))
        return results


class XiaZaiZhiJiaPosition(PositionSpider):
    """
    >>>xzzj = XiaZaiZhiJiaPosition()
    >>>xzzj.run(u'微信')
    """

    quanlity = 10
    charset = 'gb2312'
    domain = "www.xiazaizhijia.com"
    search_url = ("http://www.xiazaizhijia.com/search.php"
                  "?kwtype=0&keyword=%s&channel=0")
    xpath = "//div[@class='th-name']/a[@class='green-ico']"
    down_xpath = "//a[@class='AMIC_downStylea']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                #模糊匹配
                results.append((link, title))
        return results


class CngbaPosition(PositionSpider):
    """
    >>>cngba = CngbaPosition()
    >>>cngba.run(u'名将决')
    """
    quanlity = 5 #无下载资源
    charset = "gb2312"
    domain = "www.cngba.com"
    search_url = "http://down.cngba.com/script/search.php?keyword=%s"
    xpath = "//div[@class='game_Ljj']/strong/a"

    def download_times(self):
        pass

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
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
    base_xpath = "//div[@class='li']"
    link_xpath = "child::ul/li/a[@class='tit']" 
    down_xpath = "child::div[@class='dl']/a[class='down']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(link_xpath)
            link = elem.attrib['href']
            title = elem.text_content().strip()
            down_link = elem.xpath(self.down_xpath)  
            if appname in title:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link = down_link[0],
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    #模糊匹配
                    results.append((link, title))
            results.append((link, title))
        return results


class PcHomePosition(PositionSpider):
    """
    >>>pchome = PcHomePosition()
    >>>pchome.run(u'微信')
    下载次数：9604
    """
    charset = 'gbk'
    domain = "www.pchome.net"
    search_url = ("http://search.pchome.net/download.php"
                  "?wd=%s&submit=%CB%D1+%CB%F7")
    #xpath = "//div[@class='tit']/a"
    base_xpath = "//dd[@class='clearfix']"
    seperator = "："
    times_xpath = "child::div[@class='dw']/span/text()"
    link_xpath = "child::div[@class='tit']/a"
    down_xpath = "//div[@class='dl-download-links mg-btm20']/dl/dd/a/@onclick"
    andorid_token = 'mobile-Internet-im'

    def download_times(self, appname):
        etree = self.send_request(appname)
        items = etree.xpath(self.base_xpath)
        times = 0
        for item in items:
            elem = item.xpath(self.link_xpath)
            link = elem.attrib['href']
            title = elem.text_content()
            if title == appname:
                times_dom = item.xpath(self.times_xpath)
                if times_dom:
                    times_raw = times_dom[0]
                    try:
                        times = int(times_raw.split(self.seperator)[-1])
                    except (TypeError, IndexError):
                        pass
                    break
        return times

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)
            link = elem.attrib['href']
            title = elem.text_content()
            if self.android_token in link:
                if is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    #模糊匹配
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
    Symbian
    >>>wap = WapMyPosition()
    >>>wap.run(u'360手机卫士')
    """

    domain = "www.wapmy.cn"
    search_url = "http://www.wapmy.cn/wapmys/webmy/search.jsp"
    xpath = "//p[@class='listname']/b/a"
    abstract = True

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
    PC客户端
    >>>downbank = DownBankPosition()
    >>>downbank.run(u'金山毒霸')
    """
    charset = 'gb2312'
    domain = "www.downbank.cn"
    search_url = "http://www.downbank.cn/search.asp?keyword=%s&x=38&y=10"
    xpath = "//div[@class='searchTopic']/a"
    abstract = True

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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.attrib['title']
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

    def download_times(self):
        pass

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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
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
    abstract = True

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

if __name__ == "__main__":
    oyk = OyksoftPosition()
    print oyk.run(u'腾讯手机管家')

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

    #ruan8 = Ruan8Position()
    #print ruan8.run(u'360')

    #gd = GameDogPosition()
    #print gd.run(u'刀塔传奇')

    #mm10086 = Mm10086Position()
    #print mm10086.run(u'街头足球')

    #p520apk = Position520Apk()
    #print p520apk.run(u'QQ部落')

    #apk3 = Apk3Position()
    #print apk3.run(u'刷机精灵')

    #dza = DownzaPosition()
    #print dza.run(u'快投')

    #anzhi = AnZhiPosition()
    #print anzhi.run(u'去哪儿')

    #angeek = AngeeksPosition()
    #print angeek.run(u'飞机')

    #jiqimao = JiQiMaoPosition()
    #print jiqimao.run(u'金银岛')

    #p365 = Position365()
    #print p365.run(u'金蝶KIS')

    #sjapk = SjapkPosition()
    #print sjapk.run(u'喜羊羊')

    #nokia365 = Position365Nokia()
    #nokia365.run(u'水果忍者')

    #myfiles = MyFilesPosition()
    #myfiles.run(u'驱动精灵')

    #coolapk = CoolApkPosition()
    #print coolapk.run(u'刀塔传奇')

    #downbank = DownBankPosition()
    #print downbank.run(u'金山毒霸')

    #cs = CrossmoPosition()
    #print cs.run(u'LT来电报号')

    #shouji = ShoujiBaiduSpider()
    #print shouji.run(u'HOT市场')

    #p7xz = Position7xz()
    #print p7xz.run(u'刀塔传奇')

    pchome = PcHomePosition()
    prchome.run(u'微信 for Android')
