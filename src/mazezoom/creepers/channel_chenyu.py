# -*- coding:utf-8 -*-

#Author:chenyu
#Date:2014/08/24
#Email:chenyuxxgl@126.com


"""
    渠道下载页面爬虫:
    抓取因子：软件大小，版本，下载次数, 软件
    下载次数抓取策略：
        1.位于detail页面的可以直接抓取
        2.位于搜索结果中的可以保存此app在搜索结果中的名字,
          重新搜索获取下载次数
"""

import re
from base import ChannelSpider

class HiapkChannel(ChannelSpider):
    """
    ***无下载次数***
    url ： http://apk.hiapk.com/appinfo/com.tencent.mm
    作者： 腾讯科技广州分公司
    热度： 2.3亿热度
    大小： 25.12MB
    类别： 社交
    语言： 中文
    固件： 2.2及以上固件版本
    支持屏幕： 适用分辨率
    上架时间： 2014-07-17 
    """

    domain = "apk.hiapk.com"
    fuzzy_xpath = "//div[@class='code_box_border']/div[@class='line_content']"
    lable_xpath = "child::span[1]/text()"
    value_xpath = "child::span[2]/text()"
    down_xpath = "//a[@class='link_btn']/@href"

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                label = item.xpath(self.lable_xpath)[0]
                value = item.xpath(self.value_xpath)[-1]
                print  title, value
                result[label.strip()] = value.strip()

        down_link = etree.xpath(self.down_xpath)[0]
        down_link = self.normalize_url(url, down_link)
        if down_link:
           storage = self.download_app(down_link)
        return result 

class GfanChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://apk.gfan.com/Product/App98660.html
    版 本 号：4.0.0
    开 发 者：网易移动中心
    发布时间：2014-08-08
    文件大小：18.24MB
    支持固件：2.3 及以上版本 
    """

    domain = "apk.gfan.com"
    fuzzy_xpath = "//div[@class='app-infoAintro']/div[@class='app-info']/p[position()<5]/text()"
    down_xpath = "//a[@id='computerLoad']/@href"
    seperator = u'：' 

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                content = item.strip()
                label, value = content.split(self.seperator)
                print label, value
                result[label] = value

        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

class Apk91Channel(ChannelSpider):
    """
    url: http://apk.91.com/Soft/Android/com.tencent.mm-462-5.3.1.67_r745169.html
    版本：5.3.1.67_r745169
    下载次数：25380万
    文件大小：25.12MB
    适用固件：Android2.2及以上
    分享日期：2014-07-17 15:37
    分享者：Wechat我要上传
    联系电话：-
    联系邮箱：-
    开发商：腾讯科技广州分公司
    热门标签： 聊天工具 、 娱乐 、 通讯 、 网络语音 、 聊天社交 、 我想恋爱
    """

    domain = "apk.91.com"
    fuzzy_xpath = "//ul[@class='s_info']/li/text()[1]"
    down_xpath = "//a[@class='s_btn s_btn4']/@href"
    tag = u'热门标签'
    tag_xpath = "//ul[@class='s_info']/li[last()]/a//text()"
    seperator = u'：'
    label = u'下载次数'

    def run(self, url):
        result = {}
        down_link = None
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                content = item.strip()
                label, value = content.split(self.seperator)
                print label, value
                result[label] = value
        tags = etree.xpath(self.tag_xpath)
        tags = u'、'.join([x.strip() for x in tags])
        if tags:
            result[self.tag] = tags

        times = result.get(self.label)
        biaoqian = result.get(self.tag)
        try:
            down_link = etree.xpath(self.down_xpath)[0]
            down_link = self.normalize_url(url, down_link)
        except:
            pass

        print down_link
        if down_link:
           storage = self.download_app(down_link)

        return result

class AngeeksChannel(ChannelSpider):
    """
    url：http://apk.angeeks.com/soft/10069485.html
    软件大小： 3.4MB 
    更新时间：2012-03-20
    下载次数：3774
    """
    domain = "www.angeeks.com"
    down_xpath = "//div[@class='rgmainsrimg']/a/@href"
    seperator = u'：'
    version_xpath = "//dl[@class='clear_div hr']/dd/span[@class='ko']/text()"
    fuzzy_xpath = "//div[@class='rgmainslx']/span/text()"
    label = u'下载次数'


    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)

        version = etree.xpath(self.version_xpath)
        if version:
            version = version[0].split(self.seperator)[-1]

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()
        times = result.get(self.label)
        print times

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return result

class It168Channel(ChannelSpider):
    """
    url: http://down.it168.com/315/321/130157/index.shtml
    软件大小: 24MB
    软件作者: 腾讯
    语言界面: 简体中文
    软件授权: 免费软件
    下载次数: 614285
    更新时间: 2014-2-11
    """
    domain = "down.it168.com"
    seperator = u'：'
    fuzzy_xpath = "//div[@class='right_con1_2 mt8 border1']/ul/li"
    label_xpath = "child::span[1]/text()"
    value_xpath = "child::a/text()|child::span[2]/text()|child::text()"
    down_xpath = "//li[@class='sign11 four_li1']/a/@href"
    label = u'下载次数:'

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            label = item.xpath(self.label_xpath)[0].strip()
            value = item.xpath(self.value_xpath)[-1].strip()
            result[label] = value

        times = result.get(self.label)
        print times

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)

        return result

class PcHomeChannel(ChannelSpider):
    """
    url: http://download.pchome.net/mobile/System/files/down-26039-1.html
    更新时间：2014-05-27
    软件大小：10.12MB
    软件分类：文件管理
    开发商：微信电话本
    软件性质：[免费软件]
    支持系统：Android
    """
    domain = "download.pchome.net"
    seperator = u'：'
    fuzzy_xpath = "//div[@class='dl-info-con']/ul/li[@style='width:100%;']/preceding-sibling::li"
    label_xpath = "child::span[1]/text()"
    value_xpath = "child::text()|child::a/text()"
    pagedown_xpath = "//div[@class='dl-con-left']//div[@class='dl-info-btn']/a/@href"
    down_xpath = "//dl[@class='clearfix']/dd[last()]/a/@onclick"
    times_xpath = "//div[@class='dl-download clearfix']/div[@class='dl-info-btn']/a/span[@class='i2']/text()"

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)

        times = etree.xpath(self.times_xpath)[0]
        print times

        pagedown_link = etree.xpath(self.pagedown_xpath)[0]
        print pagedown_link
        downdetail = self.send_request(pagedown_link)
        onclick = downdetail.xpath(self.down_xpath)[0]
        r = re.compile("windowOpen\('([^']+)'\);")
        onclick_content = r.search(onclick)
        down_link = onclick_content.group(1)
        print down_link
        if down_link:
            storage = self.download_app(down_link)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            label = item.xpath(self.label_xpath)[0].strip()
            value = item.xpath(self.value_xpath)[0].strip()
            print label, value
            result[label] = value

        return result

class QQChannel(ChannelSpider):
    """
    url: http://sj.qq.com/myapp/detail.htm?apkName=com.tencent.mm
    版本号：V5.3.1.67_r745169
    更新时间：2014年7月11日
    开发商：腾讯
    """
    domain = "sj.qq.com"
    seperator = u'：'
    fuzzy_xpath = "//div[@class='det-othinfo-container J_Mod']"
    label_xpath = "child::div[@class='det-othinfo-tit']/text()"
    value_xpath = "child::div[@class='det-othinfo-data']/text()"
    down_xpath = "//div[@class='det-ins-btn-box']/a[@class='det-down-btn']/@href"
    times_xpath = "//div[@class='det-ins-num']/text()"

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)

        times = etree.xpath(self.times_xpath)[0]
        print times

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            print down_link
            storage = self.download_app(down_link)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            label = item.xpath(self.label_xpath)[0].strip()
            value = item.xpath(self.value_xpath)[-1].strip()
            print label, value
            result[label] = value

        return result

class MumayiChannel(ChannelSpider):
    """
    url: http://www.mumayi.com/android-28640.html
    软件类型：免费软件
    所属类别：新闻资讯
    更新时间：18 小时前
    程序大小：18.62MB
    """
    domain = "sj.qq.com"
    seperator = u'：'
    fuzzy_xpath = "//ul[@class='istyle fl']/li[@class='isli gray']|//ul[@class='istyle fl']/li[@class='isli']"
    label_xpath = "child::span[@class='iname']/text()"
    value_xpath = "child::text()|child::font/text()"
    down_xpath = "//a[@class='download fl']/@href"

    def download_times(self, title):
        """
        下载次数：1620472次
        """
        from searchposition import MumayiPosition
        position = MumayiPosition()
        times = position.download_times(title)
        return times

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            print down_link
            storage = self.download_app(down_link)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            label = item.xpath(self.label_xpath)[0].strip()
            value = item.xpath(self.value_xpath)[0].strip()
            print label, value
            result[label] = value

        return result

class SkycnChannel(ChannelSpider):
    """
    url: http://shouji.baidu.com/soft/item?docid=6722314&from=as&f=software%40indexrecommend%401
    大小: 6.9MB 
    版本: 5.0.1.11 
    下载次数: 9646万
    """
    domain = "www.skycn.com"
    fuzzy_xpath = "//div[@class='content-right']/div[@class='detail']/span/text()"
    down_xpath = "//div[@class='area-download']/a[@class='apk']/@href"
    label = u'下载次数'
    

    def run(self, url):
        seperator = u':'
        result = {}
        storage = None
        etree = self.send_request(url)

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            print down_link
            storage = self.download_app(down_link)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(seperator)
            print label, value
            result[label] = value

        times = result.get(self.label) 
        print times
        return result

class ZolChannel(ChannelSpider):
    """
    url: http://sj.zol.com.cn/mkey/
    下载次数： 93,866次 
    """
    domain = "sj.zol.com.cn"
    down_xpath = "//ul[@class='download-items']/li[@class='item'][1]/a[@class='downLoad-button androidDown-button']/@onclick"
    fuzzy_xpath = "//ul[@class='summary-text clearfix']/li[@class='item-3']/span/text()"
    label = u'下载次数：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)

        onclick = etree.xpath(self.down_xpath)[0]
        r = re.compile("corpsoft\('([^']+)','1'\)")
        onclick_content = r.search(onclick)
        down_link = onclick_content.group(1)
        down_link = self.normalize_url(url, down_link)
        print down_link

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}
        storage = self.download_app(down_link, headers=headers)

        items = etree.xpath(self.fuzzy_xpath)
        label, value = items
        print label
        print value
        result[label] = value

        times = result.get(self.label)
        print times
        return result

class NduoaChannel(ChannelSpider):
    """
    url: http://www.nduoa.com/apk/detail/808577
    version: (4.0.1)
    下载次数：8,740,875次下载
    版本：5.0.1.11 
    大小：18.62 MB 
    作者：网易
    更新：发布于4天前
    """
    domain = "www.nduoa.com"
    fuzzy_xpath = "//div[@class='apkinfo']"
    version_xpath = "child::div[@class='head']/div[@class='name']/span[@class='version']/text()"
    times_xpath = "child::div[@class='head']/div[@class='levelCount']/span[@class='count']/text()"
    size_xpath = "child::div[@class='size row']/text()"
    author_xpath = "child::div[@class='author row']/text()"
    authorvalue_xpath = "child::div[@class='author row']/span/a/text()"
    updatetime_xpath = "child::div[@class='updateTime row']/text()"    
    updatetimevalue_xpath = "child::div[@class='updateTime row']/em/text()"
    down_xpath = "//a[@id='BDTJDownload']/@href"
    label = u'下载次数'


    def run(self, url):
        seperator = u'：'
        result = {}
        storage = None
        etree = self.send_request(url)

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            down_link = self.normalize_url(url, down_link)
            print down_link
            storage = self.download_app(down_link)

        item = etree.xpath(self.fuzzy_xpath)[0]
        version = item.xpath(self.version_xpath)[0]
        r_version = re.compile('\((.+)\)')
        version = r_version.search(version).group(1)
        result['version'] = version
        times = item.xpath(self.times_xpath)[0]
        r_times = re.compile('([0-9,]+)')
        times = r_times.search(times).group(0)
        times = re.sub(',','',times)
        result[self.label] = times
        size = item.xpath(self.size_xpath)[0]
        size_label, size_value = size.split(seperator)
        result[size_label] = size_value
        author = item.xpath(self.author_xpath)[0]
        author = re.sub(u'：','',author)
        authorvalue = item.xpath(self.authorvalue_xpath)[0]
        result[author] = authorvalue
        updatetime = item.xpath(self.updatetime_xpath)[0]
        updatetime = re.sub(u'：','',updatetime)
        updatetimevalue = item.xpath(self.updatetimevalue_xpath)[0]
        result[updatetime] = updatetimevalue

        times = result.get(self.label)
        print times
        return result

class Android115Channel(ChannelSpider):
    """
    url: http://android.155.cn/soft/10198.html
    生活实用
    中文
    完全免费
    3M
    5756
    开发商：互联网
    2014-08-22
    """
    domain = "www.155.cn"
    fuzzy_xpath = "//div[@class='content-right']/div[@class='detail']/span/text()"
    down_xpath = "//div[@class='c1_bot']/a[@class='down']/@href"
    time_xpath = "//div[@class='c1_xxi']/span[font]/text()"
    label = u'下载次数'


    def run(self, url):
        seperator = u':'
        result = {}
        storage = None
        etree = self.send_request(url)

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            print down_link
            storage = self.download_app(down_link)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(seperator)
            print label, value
            result[label] = value

        #times = result.get(self.label)
        times = etree.xpath(self.time_xpath)[0].strip()
        print times
        return result

class LiqucnChannel(ChannelSpider):
    """
    url: http://os-android.liqucn.com/rj/12910.shtml
    下载次数：2950444次
    大小：13.62MB
    更新时间：2014-08-26
    标签： 来电归属地,隐私保护,体检,防骚扰,杀毒,拦截,来电防火墙
    """

    domain = "www.liqucn.com"
    fuzzy_xpath = "//table[@class='lineheight_0913']/tr/td"
    info_xpath = "child::text()|child::*/text()"
    down_xpath = "//a[@id='content_mobile_href']/@href"
    seperator = u'：'
    label = u'下载次数'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                content = ''.join(info)
                label, value = content.split(self.seperator)
                label = label.strip()
                value = value.strip()
                print label, value
                result[label] = value

        times = result.get(self.label)
        print times
        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

if __name__ == '__main__':
    #url = "http://apk.hiapk.com/appinfo/com.tencent.mm"
    #hiapk = HiapkChannel()
    #print hiapk.run(url)

    #url = "http://apk.gfan.com/Product/App98660.html"
    #gfan = GfanChannel()
    #print gfan.run(url)

    #url = "http://apk.91.com/Soft/Android/com.tencent.mm-462-5.3.1.67_r745169.html"
    #apk91 = Apk91Channel()
    #print apk91.run(url)

    #url = "http://apk.angeeks.com/soft/10069485.html"
    #angeeks = AngeeksChannel()
    #print angeeks.run(url)

    #url = "http://down.it168.com/315/321/130157/index.shtml"
    #it168 = It168Channel()
    #print it168.run(url)

    #url = "http://download.pchome.net/mobile/System/files/detail-26039.html"
    #pchome = PcHomeChannel()
    #print pchome.run(url)

    #url = "http://sj.qq.com/myapp/detail.htm?apkName=com.tencent.mm"
    #qq = QQChannel()
    #print qq.run(url)

    #url = "http://www.mumayi.com/android-28640.html"
    #mumayi = MumayiChannel()
    #print mumayi.run(url)
    #print mumayi.download_times(u'网易新闻 V4.0.1')

    #url = "http://shouji.baidu.com/soft/item?docid=6722314&from=as&f=software%40indexrecommend%401"
    #skycn = SkycnChannel()
    #print skycn.run(url)

    #url = "http://sj.zol.com.cn/mkey/"
    #zol = ZolChannel()
    #print zol.run(url)

    #url = "http://www.nduoa.com/apk/detail/11990"
    #nduoa = NduoaChannel()
    #print nduoa.run(url)

    #url = "http://android.155.cn/soft/10198.html"
    #android115 = Android115Channel()
    #print android115.run(url)

    #url = "http://os-android.liqucn.com/rj/12910.shtml"
    #liqucn = LiqucnChannel()
    #print liqucn.run(url)
