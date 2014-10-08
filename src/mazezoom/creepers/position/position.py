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


class OyksoftPosition(PositionSpider):
    """
    >>>oyk = OyksoftPosition()
    >>>oyk.run(u'腾讯手机管家')
    """
    seperator = u'：'
    name = u'快乐无极'
    android_token = 'Android'
    domain = "www.oyksoft.com"
    charset = 'gbk'  # 对传入的appname以此字符集进行编码
    search_url = (
        "http://www.oyksoft.com/search.asp?"
        "action=s&sType=ResName&keyword=%s"
    )
    base = "//div[@class='searched']"
    link_xpath = "child::div[@class='title']/a/strong"
    down_xpath = "//a[@class='normal']/@href"  # detail
    base_xpath = "//div[@class='searched']"
    times_xpath = "child::div[@class='softjj']/a[@class='listdbt']/text()"

    def download_times(self):
        """
        总下载次数：2444
        """
        times = 0
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            strong = item.xpath(
                self.link_xpath
            )[0]
            title = strong.text_content().strip()
            if self.app_name == title:
                times_dom = item.xpath(self.times_xpath)
                if times_dom:
                    times_raw = times_dom[0]
                    try:
                        times = int(
                            times_raw.split(self.seperator)[-1].strip()
                        )
                    except (TypeError, IndexError, ValueError):
                        pass
                    break
        return times

    def download_token(self):
        token = ''
        url = "http://bd.oyksoft.com/a.aspx"
        content = self.send_request(url=url, tree=False)
        regx = re.compile("for_download='(?P<token>.+)';")
        match = regx.search(content)
        if match is not None:
            token = match.group('token')
        return token

    def verify_app(self, url=None, down_link=None):
        """
        url: detail页面链接
        down_link: 下载链接
        chsksum: 校验和
        """
        is_right = False
        #如果没有传入down_link,就需要向detail页面发送请求
        if not down_link and url:
            etree = self.send_request(url=url)
            down_link = etree.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                if down_link.find('.oyksoft.com') > 0:
                    token = self.download_token()
                    down_link = '%s?oyksoft=%s' % (down_link, token)
        if down_link:
            storage = self.download_app(down_link)
            md5sum = fchksum.fmd5t(storage)
            if md5sum == self.chksum:
                is_right = True
                os.unlink(storage)
        return is_right

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
            title = item.text_content().strip()
            if self.android_token in title:
                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class GameDogPosition(PositionSpider):
    """
    >>>gd = GameDogPosition()
    >>>gd.run(u'刀塔传奇')
    """

    name = u'游戏狗'
    quanlity = 10
    iphone = u'iphone'
    ipad = u'ipad'
    domain = "www.gamedog.cn"
    search_url = ("http://zhannei.gamedog.cn/cse/search"
                  "?s=10392184185092281050&entry=1&q=%s")
    xpath = "//a[@class='result-game-item-title-link']"
    down_xpath = "//dd[@id='downs_box']/span[1]/a/@href"
    detail_links = "//ul[@id='div_android']/li/h3/a"

    def mixin(self, link, title):
        results = []
        detail = '/detail/'
        if detail in link:
            dtree = self.send_request(url=link)
            dlinks = dtree.xpath(self.detail_links)
            for item in dlinks:
                dlink = item.attrib['href']
                dtitle = item.text_content()
                match = self.verify_app(
                    url=dlink
                )
                if match:
                    results.append((dlink, dtitle))
                    break  # 匹配一个就可以
        else:
            match = self.verify_app(
                url=link,
            )
            if match:
                results.append((link, title))
        return results

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            low_title = title.lower()
            if self.iphone not in low_title or self.ipad not in low_title:
                if self.is_accurate:  # 精确匹配
                    links = self.mixin(link, title)
                    if links:
                        results.extend(links)
                else:
                    results.append((link, title))
        return results


class Mm10086Position(PositionSpider):
    quanlity = 10
    name = u'移动应用商店'
    domain = "mm.10086.cn"
    search_url = "http://mm.10086.cn/searchapp?dt=android&advanced=0&st=3&q=%s"
    base_xpath = "//dd[@class='sr_searchListConTt']"
    xpath = "child::h2/a"
    down_xpath = "child::a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            dom = item.xpath(self.xpath)
            if dom:
                dom = dom[0]
                link = self.normalize_url(
                    self.search_url,
                    dom.attrib['href']
                )
                title = dom.text_content()
                if self.app_name in title:
                    down_link = item.xpath(self.down_xpath)[0]
                    down_link = self.normalize_url(
                        self.search_url,
                        down_link
                    )
                    if self.is_accurate:
                        match = self.verify_app(
                            down_link=down_link
                        )
                        if match:
                            results.extend((link, title))
                            break
                    else:
                        results.append((link, title))
        return results


class Position520Apk(PositionSpider):
    """
    >>>p520apk = Position520Apk()
    >>>p520apk.run(u'QQ部落')
    """
    quanlity = 7
    name = u'安卓乐园'
    domain = "www.520apk.com"
    search_url = ("http://search.520apk.com/cse/search"
                  "?s=17910776473296434043&q=%s")
    xpath = "//h3[@class='c-title']/a"
    url_token = '/android/'  # 通过url token进一步准确定位
    down_xpath = "//a[@class='icon downbd']/@href"
        #"//a[@class='icon_downdx']/@href",
        #"//a[@class='icon_downlt']/@href",

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.app_name in title:
                if self.url_token in link:
                    if self.is_accurate:
                        match = self.verify_app(
                            url=link
                        )
                        if match:
                            results.append((link, title))
                            break
                    else:
                        results.append((link, title))
        return results


class Apk3Position(PositionSpider):
    """
    >>>apk3 = Apk3Position()
    >>>apk3.run(u'刷机精灵')
    """
    name = u'Apk3安卓网'
    quanlity = 10
    charset = 'gb2312'
    domain = "www.apk3.com"
    search_url = "http://www.apk3.com/search.asp?m=2&s=0&word=%s&x=0&y=0"
    xpath = "//div[@class='searchTopic']/a"
    down_xpath = "//ul[@class='downlistbox']/li/a/@href"  # Detail

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(url=link)
                    if match:
                        results.append((link, title))
                        break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class DownzaPosition(PositionSpider):
    """
    >>>dza = DownzaPosition()
    >>>dza.run(u'快投')
    """
    name = u'下载之家'
    quanlity = 10
    charset = 'gb2312'
    domain = "www.downza.cn"
    android_token = "Android"
    andorid_xpath = "//div[@class='bread f_mirco']/a[2]/text()"
    search_url = "http://www.downza.cn/search?k=%s"
    xpath = "//div[@class='soft_list mb_20 clearfix']/dl/dd/h2/a"
    down_xpath = "//div[@class='down_view_down_list fl']/ul/li/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            detail = self.send_request(url=link)
            android = detail.xpath(self.andorid_xpath)
            if android and android[0].strip() == self.android_token:

                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]

                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    results.append((link, title))
        return results


class AnZhiPosition(PositionSpider):
    """
    >>>anzhi = AnZhiPosition()
    >>>anzhi.run(u'去哪儿')
    """
    name = u'安智'
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

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.xpath(self.link_xpath)[0]
            )
            title = item.xpath(self.title_xpath)[0]
            if self.app_name in title:
                if self.is_accurate:
                    down_link = self.download_link(item)
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    results.append((link, title))
        return results


class AngeeksPosition(PositionSpider):
    """
    >>>angeek = AngeeksPosition()
    >>>angeek.run(u'飞机')
    """
    #验证下载个数
    name = u'安极网'
    charset = 'gbk'
    quanlity = 10
    domain = "www.angeeks.com"
    search_url = "http://apk.angeeks.com/search?keywords=%s&x=29&y=15"
    base_xpath = "//ul[@id='mybou']/li/dl/dd"
    link_xpath = "child::div[@class='info']/a/@href"
    title_xpath = "child::div[@class='info']/a/text()"
    down_xpath = "child::div[@class='dowl']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                down_link = self.normalize_url(
                    self.search_url,
                    down_link
                )
            if self.is_accurate:  # 精确匹配
                match = self.verify_app(
                    down_link=down_link,
                )
                if match:
                    results.append((link, title))
                    break
            else:
                results.append((link, title))
        return results


class JiQiMaoPosition(PositionSpider):
    """
    >>>jiqimao = JiQiMaoPosition()
    >>>jiqimao.run(u'金银岛')
    """
    name = u'机器猫'
    quanlity = 10
    domain = "jiqimao.com"
    search_url = "http://jiqimao.com/search/index?a=game&w=%s"
    search_url2 = "http://jiqimao.com/search/index?a=soft&w=%s"
    xpath = "//div[@class='applist']/ul/li/a"
    down_xpath = (
        "//img[@src='/Templates/foreapps/images/downloadbtn.jpg']"
        "/parent::a/@href"
    )

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url2)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.is_accurate:
                match = self.verify_app(link)
                if match:
                    results.append((link, title))
                    break
            else:
                results.append((link, title))
        return results


class SjapkPosition(PositionSpider):
    """
    >>>sjapk = SjapkPosition()
    >>>sjapk.run(u'喜羊羊之灰太狼闯关')
    """
    name = u'卓乐网'
    quanlity = 10
    charset = 'gb2312'
    domain = "www.sjapk.com"
    search_url = "http://www.sjapk.com/Search.asp"
    xpath = "//li/span/h1/a"
    down_xpath = "//div[@class='main_r_xiazai5']/a/@href"

    def position(self):
        results = []
        data = {'Key': self.app_name.encode(self.charset)}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.is_accurate:
                match = self.verify_app(url=link)
                if match:
                    results.append((link, title))
                    break
            else:
                results.append((link, title))
        return results


class CoolApkPosition(PositionSpider):
    """
    >>>coolapk = CoolApkPosition()
    >>>coolapk.run(u'刀塔传奇')
    """
    name = u'酷安网'
    quanlity = 10
    domain = "www.coolapk.com"
    search_url = "http://www.coolapk.com/search?q=%s"
    xpath = ("//ul[@class='media-list ex-card-app-list']"
             "/li[@class='media']/div[@class='media-body']/h4/a")
    down_xpath = "//div[@class='ex-page-header']/following::script[1]/text()"

    def download_link(self, url):
        etree = self.send_request(url=url)

        def extra_param():
            extra = ''
            extra_regx = re.compile('.+\((?P<extra>\d+)\).+')
            extra_xpath = (
                "//div[@class='media-btns"
                " ex-apk-view-btns']/a/@onclick"
            )
            extra_raw = etree.xpath(extra_xpath)
            #onDownloadApk(0);
            if extra_raw:
                extra_raw = extra_raw[0]
                match = extra_regx.match(extra_raw)
                if match is not None:
                    token = match.group('extra')
                    if token != '0':
                        extra = "&extra=%s" % token
            return extra

        down_link = None
        down_regx = re.compile(r'.+apkDownloadUrl\s=\s"(?P<url>.+)";')
        item = etree.xpath(self.down_xpath)
        if item:
            item = item[0]
            content = item.strip().split('\n')[0]
            down_match = down_regx.match(content)
            if down_match is not None:
                extra = extra_param()
                down_link = 'http://%s%s%s' % (
                    self.domain,
                    down_match.group('url'),
                    extra
                )
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.is_accurate:
                down_link = self.download_link(link)
                if down_link:
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
            else:
                results.append((link, title))
        return results


class CrossmoPosition(PositionSpider):
    """
    >>>cs = CrossmoPosition()
    >>>cs.run(u'LT来电报号')
    """
    name = u'十字猫'
    quanlity = 10
    domain = "www.crossmo.com"
    search_url = ("http://soft.crossmo.com/soft_default.php"
                  "?act=search&searchkey=%s")
    xpath = "//div[@class='infor_centerb1']/div/dl/dt/a"
    head_xpath = "//head"

    def get_appkey(self, etree):
        appkey = None
        head = etree.xpath(self.head_xpath)[0].text_content()
        regx = re.compile("var\sone_Key='(?P<key>.+)';")
        match = regx.search(head)
        if match is not None:
            appkey = match.group('key')
        return appkey

    def get_appid(self, url):
        """
        url: http://soft.crossmo.com/softinfo_505012.html
        """
        return url.split('_')[-1].split('.')[0]

    def _download_link(self, url, appkey, appid):
        check_app = (
            "http://soft.crossmo.com/softdown_topc_v5.php?"
            "crossmo=%s&downloadtype=checkapks&appid=%s"
        ) % (appkey, appid)
        down_app = (
            "http://soft.crossmo.com/softdown_topc_v5.php?"
            "crossmo=%s&downloadtype=local&appid=%s"
        ) % (appkey, appid)
        self.set_header(url)
        self.send_request(url=check_app, tree=False)
        return down_app

    def download_link(self, url):
        etree = self.send_request(url=url)
        appkey = self.get_appkey(etree)
        appid = self.get_appid(url)
        dlink = self._download_link(url, appkey, appid)
        down_link = dlink
        return down_link

    def position(self):
        results = []
        headers = {'Host': 'soft.crossmo.com', 'Referer': 'soft.crossmo.com'}
        self.update_request_headers(headers)
        etree = self.send_request(self.app_name)
        self.flush_header(('Host', 'Referer'))
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    down_link = self.download_link(link)
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    self.flush_header(('X-Requested-With', 'Referer'))
                    if match:
                        results.append((link, title))
                        break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results

    def set_header(self, url):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': url
        }
        self.update_request_headers(headers)

    def flush_header(self, fields=None):
        if fields:
            for field in fields:
                del self.session.headers[field]


class ShoujiBaiduSpider(PositionSpider):
    """
    >>>shouji = ShoujiBaiduSpider()
    >>>shouji.run(u'HOT市场')
    """
    name = u'百度手机助手'
    quanlity = 10
    domain = "shouji.baidu.com"
    search_url = ("http://shouji.baidu.com/s"
                  "?wd=%s&data_type=app&"
                  "f=header_software@input@btn_search"
                  "&from=web_alad_5")
    xpath = "//div[@class='top']/a[@class='app-name']"
    down_xpath = "//div[@class='area-download']/a[@class='apk']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class Position7xz(PositionSpider):
    """
    >>>p7xz = Position7xz()
    >>>p7xz.run(u'极品飞车13')
    """
    name = u'七匣子'
    quanlity = 10
    domain = "www.7xz.com"
    search_url = "http://www.7xz.com/search?q=%s"
    xpath = "//div[@class='caption']/ul/li/a[@class='a2']"
    down_xpath = "//div[@class='diannao']/a[@class='d_pc_normal_dn']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                )
                if match:
                    results.append((link, title))
                    break
            else:
                #模糊匹配
                results.append((link, title))
        return results


class PC6Position(PositionSpider):
    """
    >>>pc6 = PC6Position()
    >>>pc6.run(u'弹跳忍者')
    """
    name = u'PC6'
    quanlity = 10
    charset = "gb2312"
    domain = "www.pc6.com"
    search_url = (
        "http://www.pc6.com/search2.asp?"
        "keyword=%s&searchType=down&rootID=465,466"
    )
    xpath = "//div[@class='baseinfo']/h3/a"
    down_xpath = "//div[@class='left2']/a[@class='wdj']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.is_accurate:  # 精确匹配
                link = self.normalize_url(self.search_url, link)
                match = self.verify_app(
                    url=link,
                )
                if match:
                    results.append((link, title))
                    break
            else:
                #模糊匹配
                results.append((link, title))
        return results


class Position3533(PositionSpider):
    """
    >>>p3533 = Position3533()
    >>>p3533.run(u'功夫西游')
    """
    name = u'手机世界'
    quanlity = 10
    domain = "www.3533.com"
    search_url = "http://search.3533.com/software?keyword=%s"
    search_url1 = "http://search.3533.com/game?keyword=%s"
    xpath = "//div[@class='appinfo']/a[@class='apptit']"
    down_xpath = "//div[@class='andorid']/dl/dt/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                )
                if match:
                    results.append((link, title))
                    break
            else:
                #模糊匹配
                results.append((link, title))
        return results


class Apk8Position(PositionSpider):
    """
    ajax
    >>>apk8 = Apk8Position()
    >>>apk8.run(u'天天跑酷')
    """
    name = u'APK8安卓网'
    quanlity = 10
    domain = "www.apk8.com"
    search_url = "http://www.apk8.com/search.php"
    xpath = "//div[@class='main_search_pic']/ul/li/strong/a"
    down_xpath = "//div[@class='downnew']/a[@class='bt_bd']/@href"

    def position(self):
        results = []
        data = {'key': self.app_name.encode(self.charset)}
        headers = {'Host': self.domain, 'Referer': self.search_url}
        self.update_request_headers(headers)
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.is_accurate:  # 精确匹配
                match = self.verify_app(
                    url=link,
                )
                if match:
                    results.append((link, title))
                    break
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
    name = u'下载之家'
    charset = 'gb2312'
    domain = "www.xiazaizhijia.com"
    search_url = ("http://www.xiazaizhijia.com/search.php"
                  "?kwtype=0&keyword=%s&channel=0")
    xpath = "//div[@class='th-name']/a[@class='green-ico']"
    down_xpath = "//a[@class='AMIC_downStylea']/@href"
    andorid_token = 'andorid'

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.app_name in title and self.andorid_token in title.lower():
                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        url=link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class AnRuanPosition(PositionSpider):
    name = u'安软市场'
    charset = 'gbk'
    domain = "soft.anruan.com"
    search_url = "http://www.anruan.com/search.php?t=all&keyword=%s"
    base_xpath = "//div[@class='li']"
    link_xpath = "child::ul/li/a[@class='tit']"
    down_xpath = "child::div[@class='dl']/a[@class='down']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.text_content().strip()
            down_link = item.xpath(self.down_xpath)
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                            break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class PcHomePosition(PositionSpider):
    #charset = 'gbk'
    domain = "www.pchome.net"
    #search_url = ("http://search.pchome.net/download.php"
    #              "?wd=%s&submit=%CB%D1+%CB%F7")
    search_url = "http://download.pchome.net/search-%s---0-1.html"
    #xpath = "//div[@class='tit']/a"
    base_xpath = "//dd[@class='clearfix']"
    seperator = u"："
    times_xpath = "child::div[@class='dw']/span/text()"
    link_xpath = "child::div[@class='tit']/a"
    down_xpath = "//div[@class='dl-download-links mg-btm20']/dl/dd/a/@onclick"
    android_title_token = 'android'
    android_url_token = '/mobile/'
    fuzzy_xpath = "//div[@class='dl-info-con']/ul/li"

    def download_times(self):
        times = 0
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content()
            if title == self.app_name:
                times_dom = item.xpath(self.times_xpath)
                if times_dom:
                    times_raw = times_dom[0]
                    try:
                        times = int(
                            times_raw.split(self.seperator)[-1].strip()
                        )
                    except (TypeError, IndexError, ValueError):
                        pass
                    break
        return times

    def download_link(self, etree):
        down_link = None
        href = None
        down_label = u'下载地址'
        regx = re.compile(".+\('(?P<link>.+)'\).+")
        xpath = "//ul[@class='dl-tab-6 clearfix']/li/a"
        links = etree.xpath(xpath)
        for link in links:
            text = link.text.strip()
            if text == down_label:
                href = link.attrib.get('href', '')
                etree = self.send_request(url=href)
                items = etree.xpath(self.down_xpath)
                if items:
                    item = items[0]
                    match = regx.search(item)
                    if match is not None:
                        down_link = match.group('link')
        return down_link, href

    def tell_android(self, title, link):
        etree = None
        referer = None
        down_link = None
        is_android = False
        if self.android_title_token in title.lower():
            is_android = True
        elif self.android_url_token in link and 'iphone' not in title.lower():
            etree = self.send_request(url=link)
            items = etree.xpath(self.fuzzy_xpath)
            for item in items:
                content = item.text_content().strip()
                label, value = content.split(self.seperator)
                if label == u'支持系统' and value == 'Android':
                    is_android = True
                    break
        if etree is None:
            etree = self.send_request(url=link)
            down_link, referer = self.download_link(etree)
        return is_android, down_link, referer

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.text_content()
            is_android, down_link, referer = self.tell_android(title, link)
            if is_android:
                if self.is_accurate:  # 精确匹配
                    headers = {
                        'Host': 'dl-sh-ctc-2.pchome.net',
                        'Referer': referer
                    }
                    self.update_request_headers(headers)
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    #模糊匹配
                    results.append((link, title))
        return results


class HiapkPosition(PositionSpider):
    """
    下载次数：否(搜索页面3.92千万热度)
    备选：    热度/评分次数
    位置：    信息页
    """
    name = u'安卓市场'
    domain = "apk.hiapk.com"
    search_url = "http://apk.hiapk.com/search?key=%s"
    xpath = "//span[@class='list_title font12']/a"
    down_xpath = "//a[@class='link_btn']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            detail = self.get_elemtree(link)
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(link, down_link)
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class GfanPosition(PositionSpider):
    """
    下载次数：否
    备选：    评分次数
    位置：    信息页
    """
    name = u'机锋市场'
    domain = "apk.gfan.com"
    search_url = "http://apk.gfan.com/search?q=%s"
    xpath = "//span[@class='apphot-tit']/a"
    down_xpath = "//a[@id='computerLoad']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            detail = self.get_elemtree(link)
            if self.app_name in title:
                if self.is_accurate:    # 精确匹配
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class Apk91Position(PositionSpider):
    """
    下载次数：是（文字）
    位置：    信息页
    搜索：    分类搜索
    极少数detail页里没有down_link
    """
    name = u'安卓下载'
    domain = "apk.91.com"
    search_url = "http://apk.91.com/soft/android/search/1_5_0_0_%s"
    search_url1 = "http://apk.91.com/game/android/search/1_5_%s"
    xpath = "//div[@class='zoom']/h4/a"
    down_xpath = "//a[@class='s_btn s_btn4']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(
            self.app_name,
            url=self.search_url1
        )
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.attrib['href']
            )
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:    # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(
                            self.search_url,
                            down_link
                        )

                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class It168Position(PositionSpider):
    """
    下载次数：是(d)
    位置：    信息页
    搜索：    结果不区分平台
    """
    name = u'IT168软件下载'
    domain = "down.it168.com"
    charset = 'gb2312'
    suffix = u'.apk'
    search_url = "http://down.it168.com/soft_search.html?keyword=%s"
    xpath = "//div[@class='r3']/ul/li/h3/a"
    down_xpath = "//li[@class='sign11 four_li1']/a/@href"
    android_tokens = ['android', u'安卓版']
    ios_tokens = ['iphone', 'ipad']

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            low_title = title.lower()

            #准确验证andorid
            isbreak = False
            for token in self.ios_tokens:
                if token in low_title:
                    isbreak = True
                    break

            if isbreak:
                continue

            is_android = False
            for token in self.android_tokens:
                if token in low_title:
                    is_android = True
                    break

            if is_android:
                if self.is_accurate:  # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class QQPosition(PositionSpider):
    """
    下载次数：是(d, s)
    位置：    信息页
    搜索：    Json,Ajax,目前搜索结果只能取到前10个
    """
    name = u'应用宝'
    domain = "sj.qq.com"
    search_url = (
        "http://sj.qq.com/myapp/"
        "searchAjax.htm?kw=%s&pns=&sid="
    )
    detail_url = (
        "http://sj.qq.com/myapp/"
        "detail.htm?apkName=%s"
    )
    down_xpath = (
        "//div[@class='det-ins-btn-box']/"
        "a[@class='det-down-btn']/@data-apkurl"
    )

    def position(self):
        results = []
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % quote_app
        content = self.get_content(url)
        output = json.loads(content)
        appList = output.get('obj', {}).get('appDetails', [])
        for app in appList:
            link = self.detail_url % app.get('pkgName', '')
            title = app.get('appName', '').strip()
            #downcount = app['appDownCount']
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results


class MumayiPosition(PositionSpider):
    """
    下载次数：是(S)
    位置：    列表页
    """
    name = u'木蚂蚁应用市场'
    domain = "andorid.mumayi.com"
    search_url = "http://s.mumayi.com/index.php?q=%s"
    base_xpath = "//ul[@class='applist']/li"
    link_xpath = "child::h3[@class='hidden']/a"
    times_xpath = "descendant::li[@class='num']/text()"
    down_xpath = "//a[@class='download fl']/@href"

    def download_times(self):
        """
        下载次数：1620467次
        """
        times = 0
        seperator = u'：'
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            rawtitle = elem.attrib.get('title', '').strip()
            if rawtitle == self.app_name:
                times_dom = item.xpath(self.times_xpath)
                if times_dom:
                    rawtimes = times_dom[0]
                    try:
                        times = int(rawtimes.split(seperator)[-1][:-1])
                    except (TypeError, IndexError, ValueError):
                        pass
                    else:
                        break
        return times

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.attrib.get('title', '').strip()
            if self.app_name in title.lower():
                if self.is_accurate:    # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class ZolPosition(PositionSpider):
    """
    多版本现象
    下载次数：(D)
    位置：    信息页
    """
    name = u'ZOL手机应用'
    domain = "sj.zol.com.cn"
    charset = 'gbk'
    search_url = "http://xiazai.zol.com.cn/search?wd=%s&type=1"
    xpath = (
        "//ul[@class='results-text']/li[@class='item']/"
        "div[@class='item-header clearfix']/a"
    )
    down_xpath = (
        #"//ul[@class='download-items']/li[@class='item'][1]"
        "//a[@class='downLoad-button androidDown-button']/@href"
    )
    token = 'sj.zol.com.cn'
    iphone_token = ['iphone', 'ipad']

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            low_title = title.lower()
            if self.token in link and self.app_name in title:
                is_continue = False
                for itoken in self.iphone_token:
                    if itoken in low_title:
                        is_continue = True
                        break
                if is_continue:
                    continue
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    #onclick = detail.xpath(self.down_xpath)[0]
                    #r = re.compile("corpsoft\('([^']+)','\d+'\)")
                    #onclick_content = r.search(onclick)
                    #down_link = onclick_content.group(1)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(link, down_link)
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class PcOnlinePosition(PositionSpider):
    """
    下载次数：是(s,d)
    位置：    信息页
    """
    name = u'太平洋电脑网'
    domain = "dl.pconline.com.cn"
    charset = 'gb2312'
    search_url = (
        "http://ks.pconline.com.cn/download.shtml"
        "?q=%s"
        "&downloadType=Android%%CF%%C2%%D4%%D8"
    )  # %%表示%
    xpath = "//a[@class='aTitle']"
    down_xpath = "//a[@class='btn sbDownload']/@tempurl"

    def get_pid(self, url):
        pid_url = url.rsplit('/', 1)
        pid = pid_url[-1].split('.')[0]
        return pid

    def get_token(self, url):
        token = None
        token_url = "http://dlc2.pconline.com.cn/dltoken/%s_genLink.js"
        pid = self.get_pid(url)
        token_url = token_url % pid
        content = self.send_request(url=token_url, tree=False)
        regx = re.compile('\((?P<token>.+)\)')
        match = regx.search(content.strip())
        if match is not None:
            token = match.group('token')
        return token

    def download_link(self, url):
        down_link = None
        token = self.get_token(url)
        if token is not None:
            detail = self.get_elemtree(url)
            dlink = detail.xpath(self.down_xpath)
            if dlink:
                dlink = dlink[0]
                items = dlink.rsplit('/', 1)
                down_link = '%s/%s/%s' % (items[0], token, items[1])
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    headers = {'Host': self.domain, 'Referer': link}
                    self.update_request_headers(headers)
                    down_link = self.download_link(link)
                    if down_link:
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class SinaPosition(PositionSpider):
    """
    下载次数：(S, D)
    位置：    信息页
    """
    name = u'新浪科技'
    domain = "tech.sina.com.cn"
    charset = 'gb2312'
    search_url = (
        "http://down.tech.sina.com.cn/3gsoft/"
        "iframelist.php?classid=0&keyword=%s&tag=&osid=4"
    )
    xpath = "//div[@class='b_txt']/h3/a"
    down_xpath = "//a[@id='downurl_link']/@href"

    def download_ip(self):
        token = None
        ip_url = "http://sinastorage.com/?extra&op=selfip.js&cb=downWithIp"
        content = self.send_request(url=ip_url, tree=False)
        regx = re.compile("\('(?P<token>.+)'\)")
        match = regx.search(content.strip())
        if match is not None:
            token = match.group('token')
        return token

    def download_link(self, url):
        down_link = None
        detail = self.get_elemtree(url, ignore=True)
        dlink = detail.xpath(self.down_xpath)
        if dlink:
            dlink = dlink[0]
            ip = self.download_ip()
            dlink = '%s&ip=%s' % (dlink, ip)
            down_link = self.normalize_url(
                self.search_url,
                dlink
            )
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if self.is_accurate:  # 精确匹配
                down_link = self.download_link(link)
                if down_link:
                    headers = {'Referer': link}
                    self.update_request_headers(headers)
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
            else:
                results.append((link, title))
        return results


class DuotePosition(PositionSpider):
    """
    下载次数：是(人气S, D)
    位置：    信息页
    """
    name = u'2345软件大全'
    domain = "www.duote.com"
    charset = 'gb2312'
    search_url = "http://www.duote.com/searchPhone.php?searchType=&so=%s"
    xpath = (
        "//div[@class='list_item']/"
        "div[@class='tit_area']/span[@class='name']/a"
    )

    def download_link(self, link):
        down_link = None
        regx = re.compile("var sPubdown = '(?P<down_link>.+?)';")
        content = self.send_request(url=link, tree=False)
        match = regx.search(content)
        if match is not None:
            down_link = match.group('down_link')
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.attrib['href']
            )
            title = item.text_content().strip()
            if self.is_accurate:  # 精确匹配
                down_link = self.download_link(link)
                if down_link:
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
            else:
                results.append((link, title))
        return results


class ImobilePosition(PositionSpider):
    """
    下载次数：是(S, D)
    位置：    信息页
    """
    name = u'手机之家'
    domain = "www.imobile.com.cn"
    search_url = "http://app.imobile.com.cn/android/search/%s.html"
    xpath = "//ul[@class='ranking_list']/li/div[@class='ico']/h3/a"
    down_xpath = "//div[@class='download_install']/a[@class='download']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.attrib['href']
            )
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class NduoaPosition(PositionSpider):
    """
    下载次数：是S,D
    位置：    信息页
    """
    name = u'N多网'
    domain = "www.nduoa.com"
    search_url = "http://www.nduoa.com/search?q=%s"
    base_xpath = "//ul[@class='apklist clearfix']/li"
    link_xpath = "child::div[@class='name']/a/@href"
    title_xpath = "child::div[@class='name']/a/span[@class='title']/text()"
    down_xpath = "child::div[@class='btn']/a[@class='dataEle']/@data-dlurl"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            link = item.xpath(self.link_xpath)[0]
            link = self.normalize_url(self.search_url, link)
            title = item.xpath(self.title_xpath)[0].strip()
            if self.app_name in title:
                if self.is_accurate:
                    down_link = item.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(
                            self.search_url,
                            down_link
                        )
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class Android155Position(PositionSpider):
    """
    下载次数：是(S,D)
    位置：    信息页
    """
    name = u'手游天下'
    domain = "www.155.cn"
    charset = 'gb2312'
    search_url = "http://android.155.cn/search.php?kw=%s&index=soft"
    xpath = "//ul[@class='gmc-c']/li/strong/a"
    down_xpath = "//a[@class='down']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.attrib['href']
            )
            title = item.text_content().strip()
            if self.is_accurate:
                detail = self.get_elemtree(link)
                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]
                    down_link = self.normalize_url(
                        self.search_url,
                        down_link
                    )
                    if down_link:
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class Shop958Position(PositionSpider):
    """
    下载次数：是(S, D)
    位置：    信息页
    搜索：    分类搜索，搜索结果没有区分平台
    """
    seperator = u'：'
    os_token = 'android'
    name = u'百信手机下载中心'
    domain = "d.958shop.com"
    charset = 'gb2312'
    search_url = "http://d.958shop.com/search/?keywords=%s&cn=soft"
    # 游戏下载页面跳转3次
    search_url1 = "http://d.958shop.com/search/?keywords=%s&cn=game"
    base_xpath = "//div[@class='soft_img']/dl[@class='game_word']"
    link_xpath = "child::dd/span[@class='t_name01']/a[@class='b_f']"
    down_xpath = "//div[@class='todown1']/a[1]/@href"
    fuzzy_xpath = "child::dd[@class='zx_word']/span"

    def platform_token(self, etree):
        platform = u'运行平台'
        fuzzy_items = etree.xpath(self.fuzzy_xpath)
        is_android = False
        for item in fuzzy_items:
            text = item.text_content().strip()
            items = text.split(self.seperator)
            if platform == items[0] and items[1].lower() == self.os_token:
                is_android = True
                break
        return is_android

    def download_link(self, link):
        down_link = None
        detail = self.get_elemtree(link)
        dlink = detail.xpath(self.down_xpath)
        if dlink:
            down_link = dlink[0]
            if down_link == '#goto_download':
                down_url = link+down_link
                down_page = self.get_elemtree(down_url)
                down_xpath = "//dd[@class='down_u']/a/@href"
                ddlink = down_page.xpath(down_xpath)
                if ddlink:
                    down_link = ddlink[0]
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name, charset=True)
        etree2 = self.send_request(
            self.app_name,
            url=self.search_url1,
            charset=True
        )
        items = etree.xpath(self.base_xpath)
        items2 = etree2.xpath(self.base_xpath)
        items.extend(items2)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.text_content().strip()
            if self.app_name in title:
                is_android = self.platform_token(item)
                if is_android:
                    if self.is_accurate:
                        down_link = self.download_link(link)
                        if down_link:
                            match = self.verify_app(
                                down_link=down_link,
                            )
                            if match:
                                results.append((link, title))
                    else:
                        results.append((link, title))
        return results


class LiqucnPosition(PositionSpider):
    """
    下载次数：(D)
    位置：    信息页
    搜索：    根据Cookie或者referer来区别用户手机系统
    """
    name = u'历趣'
    domain = "www.liqucn.com"
    android_referer = 'http://os-android.liqucn.com/'
    search_url = "http://search.liqucn.com/download/%s"
    base_xpath = "//div[@id='search_result']/ul"
    link_xpath = "child::li[@class='appli_info']/a"
    #down_xpath = "//a[@id='content_mobile_href']/@href"
    down_xpath = "child::li[@class='appli_dwn']/div[@class='down_btn']/a/@href"
    os_token = 'os-android'

    def position(self):
        results = []
        headers = {'Referer': self.android_referer}
        self.update_request_headers(headers)
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib.get('href', '')
            title = elem.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    down_link = item.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class CnmoPosition(PositionSpider):
    """
    TODO:channel
    下载次数：否
    备选：    赞次数
    位置：    信息页
    """
    name = u'手机中国'
    domain = "www.cnmo.com"
    charset = 'gb2312'
    search_url = "http://app.cnmo.com/search/c=a&s=%s&p=2&f=1"
    xpath = "//ul[@class='ResList']/li/div[@class='Righttitle'][1]/a"
    down_xpath = "//input[@id='downloadInfo']/@applocaldownloadurl"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
            results.append((link, title))
        return results


class CrskyPosition(PositionSpider):
    """
    下载比较慢
    下载次数：否
    备选：    访问量
    位置：    信息页
    搜索：    搜索结果比浏览器展示条目要少
    """
    name = u'非凡软件站'
    domain = "www.crsky.com"
    charset = 'gb2312'
    search_url = "http://sj.crsky.com/query.aspx?keyword=%s&type=android"
    xpath = "//div[@class='right']//a"
    down_xpath = "//div[@class='btns']/ul/li/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class DPosition(PositionSpider):
    """
    下载次数：(S, D)
    位置：    列表页
    """
    name = u'当乐网'
    domain = "www.d.cn"
    search_url = "http://android.d.cn/search/app/?keyword=%s"
    base_xpath = "//ul[@class='app-list clearfix']/li"
    link_xpath = "child::div/div[@class='list-right']/p[@class='g-name']/a"
    down_xpath = (
        "child::div/div[@class='list-left']"
        "/div[@class='app-h']/a/@onclick"
    )

    def set_header(self):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.update_request_headers(headers)

    def flush_header(self, fields=None):
        if fields:
            for field in fields:
                del self.session.headers[field]

    def download_link(self, etree):
        down_link = None
        post_url = "http://android.d.cn/rm/red/%s/%s"
        regx = re.compile('\((?P<params>.+)\)')
        onclick = etree.xpath(self.down_xpath)
        if onclick:
            onclick = onclick[0]
            match = regx.search(onclick)
            if match:
                params = match.group('params')
                params = params.split(',')
                down_url = post_url % (params[1], params[2])
                self.set_header()
                content = self.send_request(
                    url=down_url,
                    data={'brand': '', 'model': ''},
                    tree=False
                )
                try:
                    loaddata = json.loads(content)
                except:
                    pass
                else:
                    pkgs = loaddata.get('pkgs')
                    if pkgs:
                        down_link = pkgs[0].get('pkgUrl', None)
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name, ignore=True)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib.get('href', '')
            title = elem.attrib.get('title', '').strip()
            if self.app_name in title:
                if self.is_accurate:
                    down_link = self.download_link(item)
                    if down_link:
                        match = self.verify_app(down_link=down_link)
                        if match is not None:
                            results.append((link, title))
                        self.flush_header(('X-Requested-With',))
                else:
                    results.append((link, title))
        return results


class SjwyxPosition(PositionSpider):
    """
    >>>sjwyx = SjwyxPosition()
    >>>sjwyx.run(u'龙印')
    """
    name = u"手游之家"
    domain = "www.sjwyx.com"
    search_url = "http://www.sjwyx.com/so.aspx?keyword=%s"
    base_xpath = "//li[@class='brdr brdb']"
    link_xpath = "child::a[@class='n']"
    down_xpath = "//a[@class='android_ico']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(down_link=down_link)
                        if match is not None:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class WandoujiaPosition(PositionSpider):
    """
    下载次数：(S, D)
    备选：    安装量
    位置：    信息页
    """
    name = u'豌豆荚'
    domain = "www.wandoujia.com"
    search_url = "http://www.wandoujia.com/search?key=%s"
    base_xpath = "//ul[@id='j-search-list']/li[@class='card']"
    link_xpath = "child::div[@class='app-desc']/a"
    down_xpath = "child::a[@class='install-btn ']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    down_link = item.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class AnzowPosition(PositionSpider):
    """
    下载次数：有
    """
    name = u'安卓软件园'
    domain = "www.anzow.com"
    search_url = "http://www.anzow.com/Search.shtml?stype=anzow&q=%s"
    xpath = "//div[@class='box boxsbg']//dd[@class='down_title']/h2/a"
    down_xpath = "//div[@class='contentdbtn']/a[@class='commentbtn']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
            else:
                results.append((link, title))
        return results


class BkillPosition(PositionSpider):
    """
    下载次数：否
    备选：    人气
    位置：    信息页
    搜索：    高级搜索
    """
    name = u'比克尔下载'
    domain = "www.bkill.com"
    charset = 'gb2312'
    search_url = "http://www.bkill.com/d/search.php?mod=do&n=1"
    xpath = "//div[@class='clsList']/dl/dt/a"
    down_xpath = "//div[@class='down_link_main']/ul/li/a/@href"

    def position(self):
        results = []
        data = {
            'keyword': self.app_name.encode(self.charset),
            'area': 'name',
            'category': '0',
            'field[condition]': 'Android',
            'order': 'downcount',
            'submit': '搜 索',
            'way': 'DESC'
        }
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[-1]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class AndroidcnPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    应用、游戏、资讯、壁纸、主题使用不同二级域名
    列表页与结果页下载次数不一致
    """
    name = u'安卓中国'
    domain = "www.androidcn.com"
    search_url = "http://down.androidcn.com/search/q/%s"
    search_url1 = "http://game.androidcn.com/search/q/%s"
    xpath = "//h2/a"
    down_xpath = "//p[@class='dl-add-3']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
            return results


class SohuPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    同 app.sohu.com
    """
    name = u'搜狐应用中心'
    domain = "download.sohu.com"
    search_url = "http://download.sohu.com/search?words=%s"
    xpath = (
        "//div[@class='yylb_box']/div[@class='yylb_main']"
        "/p[@class='yylb_title']/strong/a"
    )
    down_xpath = "//div[@class='gy_03 clear']/div[2]/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class OnlineDownPosition(PositionSpider):
    """
    下载次数：否
    备选：    人气数
    位置：    信息页
    排行列表页有下载量，搜索列表页无，结果页无
    """
    #abstract = True
    name = u'华军软件园'
    domain = "www.onlinedown.net"
    search_url = (
        "http://search.newhua.com/search_list.php"
        "?searchname=%s"
        "&searchsid=1"
        "&button.x=0"
        "&button.y=0"
    )
    base_xpath = "//div[@class='title']"
    link_xpath = "child::strong/a"
    version_xpath = "child::strong/a/text()"
    token_xpath = (
        "following::h4[@class='left']/"
        "span[@class='f11 farial']/text()"
    )
    pagedown_xpath = "//a[@class='btn_page']/@href"
    down_xpath = "//div[@class='info']/div[@class='down-menu']/a/@href"
    android_token = "android"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.xpath("child::i/text()")[0].strip()
            platform = item.xpath(self.token_xpath)[0].strip().lower()
            if self.app_name in title and platform == self.android_token:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    pagedown_link = detail.xpath(self.pagedown_xpath)
                    if pagedown_link:
                        pagedown_link = pagedown_link[0]
                        pagedown_link = self.normalize_url(link, pagedown_link)
                        downdetail = self.get_elemtree(pagedown_link)
                        down_link = downdetail.xpath(self.down_xpath)
                        if down_link:
                            down_link = down_link[0]
                            match = self.verify_app(
                                down_link=down_link,
                            )
                            if match:
                                results.append((link, title))
                else:
                    results.append((link, title))
        return results


class ZhuodownPosition(PositionSpider):
    """
    下载次数：是
    位置:     信息页
    搜索：    高级搜索
    """
    name = u'捉蛋网'
    domain = "www.zhuodown.com"
    charset = 'gb2312'
    search_url = (
        "http://www.zhuodown.com/plus/search.php?domains=www.zhuodown.com"
        "&kwtype=0&q=%s&searchtype=titlekeyword&client=pub-9280232748837488"
        "&forid=1&ie=GB2312&oe=GB2312&safe=active&cof=GALT:#008000;GL:1;DIV:"
        "#336699;VLC:663399;AH:center;BGC:FFFFFF;LBGC:336699;"
        "ALC:0000FF;LC:0000FF;"
        "T:000000;GFNT:0000FF;GIMP:0000FF;FORID:1&hl=zh-CN"
    )
    xpath = "//div[@class='listbox']/ul[@class='e2']/li/a[2]"
    pagedown_xpath = "//ul[@class='downurllist']/a/@href"
    down_xpath = "//div[@class='advancedsearch']/table/tr[2]/td/li[1]/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    pagedown_link = detail.xpath(self.pagedown_xpath)
                    if pagedown_link:
                        pagedown_link = pagedown_link[0]
                        downdetail = self.get_elemtree(pagedown_link)
                        down_link = downdetail.xpath(self.down_xpath)
                        if down_link:
                            down_link = down_link[0]
                            match = self.verify_app(
                                down_link=down_link,
                            )
                            if match:
                                results.append((link, title))
                else:
                    results.append((link, title))
        return results


class Android159Position(PositionSpider):
    """
    下载次数：是
    位置:     信息页
    搜索：    应用和游戏分类搜索
    机客网安卓市场
    """
    name = u'机客网安卓市场'
    domain = "android.159.com"
    charset = 'gb2312'
    search_url = (
        "http://2013.159.com/appshop/appsoftSearch.aspx?"
        "keyword=%s&MobleBrandTypeId=3170&submit=搜索"
    )
    search_url1 = (
        "http://2013.159.com/appshop/appgameSearch.aspx?"
        "keyword=%s&MobleBrandTypeId=3170&submit=搜索"
    )
    xpath = "//div[@class='typecontent_title f14 appzp6 flod']/a"
    down_xpath = "//div[@class='appinfo_main_2_1_3_1_1']/a/@href"

    def position(self):
        results = []
        regx = re.compile('\(\'(?P<link>.+)\'\)')
        etree = self.send_request(self.app_name, ignore=True)
        etree2 = self.send_request(
            self.app_name,
            url=self.search_url1,
            ignore=True
        )
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = regx.search(down_link)
                        if match is not None:
                            dlink = match.group('link')
                            dlink = self.normalize_url(link, dlink)
                            match = self.verify_app(
                                down_link=dlink,
                            )
                            if match:
                                results.append((link, title))
                else:
                    results.append((link, title))
        return results


class AibalaPosition(PositionSpider):
    """
    下载次数：否
    备选：    关注数
    位置：    信息页
    搜索：    列表页与结果页不一致
    """
    name = u'android软件分享社区'
    domain = "www.aibala.com"
    search_url = "http://www.aibala.com/android-search-1-0-0-%s-1-1"
    xpath = "//ul[@class='block']/li//div[@class='tabRightTL']/a"
    down_xpath = (
        "//div[@class='listMainRightBottomL']/"
        "div[@class='RightB1']/a[1]/@onclick"
    )

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)[0]
                    r = re.compile("window.location.href='(.+)';return false;")
                    down_link = r.search(down_link)
                    down_link = down_link.group(1)
                    if down_link:
                        down_link = self.normalize_url(link, down_link)
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class EoemarketPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    name = u'优亿市场'
    domain = "www.eoemarket.com"
    search_url = "http://www.eoemarket.com/search_.html?keyword=%s&pageNum=1"
    xpath = "//ol[@class='RlistName']/li[1]/span/a"
    down_xpath = "//div[@class='detailsright']/ol/li[1]/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name, ignore=True)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            if self.app_name in title:
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class VmallPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    华为开发者联盟-->华为应用市场
    """
    name = u'华为应用市场'
    domain = "app.vmall.com"
    search_url = "http://app.vmall.com/search/%s"
    base_xpath = (
        "//div[@class='list-game-app dotline-btn nofloat']/"
        "div[@class='game-info  whole']"
    )
    down_xpath = "child::div[@class='app-btn']/a/@onclick"
    link_xpath = "child::h4/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name, ignore=True)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = elem.text.strip()
            if self.app_name in title:
                if self.is_accurate:
                    down_link_raw = item.xpath(self.down_xpath)[0]
                    if down_link_raw:
                        down_link = down_link_raw.split(',')[5][1:-1]
                        if down_link:
                            match = self.verify_app(
                                down_link=down_link,
                            )
                            if match:
                                results.append((link, title))
                else:
                    results.append((link, title))
        return results


class ApkolPosition(PositionSpider):
    """
    下载次数：否
    备选：    安装次数
    搜索：    信息页打开慢
    """
    name = u'安卓在线'
    domain = "www.apkol.com"
    search_url = "http://www.apkol.com/search?keyword=%s"
    base_xpath = "//div[@class='listbox ty']/div[@class='yl_ybwz']"
    link_xpath = "child::h3/a"
    down_xpath = "child::div[@class='yl_btn']/a/@href"
    #down_xpath = "//div[@content]/div[@class='cn_btn']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = self.normalize_url(self.search_url, elem.attrib['href'])
            title = elem.attrib['title'].strip()
            if self.app_name in title:
                if self.is_accurate:
                    down_link = item.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class YruanPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索:     搜索结果不区分平台
    """
    name = u'亿软网'
    domain = "www.yruan.com"
    search_url = "http://www.yruan.com/search.php?keyword=%s"
    xpath = "//span[@class='item_name']/a"
    token = 'Android'
    down_xpath = "//li[@class='downimg']/div[@class='down_link']/a/@href"

    def position(self):
        results = []
        regx = re.compile('\((?P<platform>.+)\)')
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        android_list = []
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.attrib.get('title', '').strip()
            text = item.text.strip()
            match = regx.search(text)
            platform = None
            if match:
                platform = match.group('platform').strip()
            if platform:
                if self.token == platform and self.app_name in title:
                    android_list.append((link, title))
            else:
                if self.app_name in title:
                    android_list.append((link, title))
        if self.is_accurate:
            for item in android_list:
                link = item[0]
                title = item[1]
                detail = self.get_elemtree(link)
                pagedown_link = detail.xpath(self.down_xpath)
                if pagedown_link:
                    pagedown_link = pagedown_link[0]
                    r = re.compile("id=([0-9]+)&")
                    soft_id = r.search(pagedown_link)
                    soft_id = soft_id.group(1)
                    down_link = "http://www.yruan.com/down.php?id=%s" % soft_id
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, item))
        else:
            results = android_list
        return results

if __name__ == "__main__":
    yruan = YruanPosition(
        u'手机QQ',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    yruan.run()

    apkol = ApkolPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #apkol.run()

    vmall = VmallPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #vmall.run()

    eoemarket = EoemarketPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #eoemarket.run()

    aibala = AibalaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #aibala.run()

    android159 = Android159Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #android159.run()

    zhuodown = ZhuodownPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #zhuodown.run()

    onlinedown = OnlineDownPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #onlinedown.run()

    #shouji = ShoujiPosition(
    #    u'水果忍者',
    #    app_uuid=1,
    #    version='1.9.5',
    #    chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    #)
    #shouji.run()

    sohu = SohuPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #sohu.run()

    andoridcn = AndroidcnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #andoridcn.run()

    anzow = AnzowPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #anzow.run()

    wandoujia = WandoujiaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #wandoujia.run()

    oyk = OyksoftPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #oyk.run()

    gd = GameDogPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #gd.run()

    mm10086 = Mm10086Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #mm10086.run()

    p520apk = Position520Apk(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #p520apk.run()

    apk3 = Apk3Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #apk3.run()

    dza = DownzaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #dza.run()

    anzhi = AnZhiPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #anzhi.run()

    angeek = AngeeksPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #angeek.run()

    jiqimao = JiQiMaoPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #jiqimao.run()

    sjapk = SjapkPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )

    coolapk = CoolApkPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )

    cs = CrossmoPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #cs.run()

    shouji = ShoujiBaiduSpider(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #shouji.run()

    p7xz = Position7xz(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #p7xz.run()

    pc6 = PC6Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #pc6.run()

    p3533 = Position3533(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #p3533.run()

    apk8 = Apk8Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #apk8.run()

    xzzj = XiaZaiZhiJiaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #xzzj.run()

    pchome = PcHomePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #pchome.run()

    hiapk = HiapkPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #hiapk.run()

    gfan = GfanPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #gfan.run()

    apk91 = Apk91Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #apk91.run()

    it168 = It168Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #it168.run()

    qq = QQPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #qq.run()

    mumayi = MumayiPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #mumayi.run()
    zol = ZolPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #zol.run()

    pconline = PcOnlinePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #pconline.run()

    sina = SinaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #sina.run()

    duote = DuotePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #duote.run()

    imobile = ImobilePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #imobile.run()

    nduoa = NduoaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #nduoa.run()

    shop958 = Shop958Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
   # shop958.run()

    liqucn = LiqucnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #liqucn.run()

    cnmo = CnmoPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #cnmo.run()

    crsky = CrskyPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #crsky.run()

    d = DPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #d.run()

    sjwyx = SjwyxPosition(
        u'时空',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #sjwyx.run()
