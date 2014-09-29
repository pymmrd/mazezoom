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

if __name__ != '__main__':
    import os
    import sys
    current_path = os.path.abspath(os.path.dirname(__file__))
    creepers_path = os.path.abspath(os.path.dirname(current_path))
    sys.path.append(creepers_path)

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

#error js生成下载链接
class PcOnlineChannel(ChannelSpider):
    """
    url: http://dl.pconline.com.cn/download/172907.html
    提供商：百度无线 软件大小：7.59M
    软件授权：免费 更新：2014-8-22
    软件评级： 语言：简体中文
    """
    domain = "dl.pconline.com.cn"
    fuzzy_xpath = "//div[@class='megR']//i[@class='item']"
    info_xpath = "child::*/text()"
    times_xpath = "//a[@id='linkPage']/em[@id='span_dl_count']/text()"
    label = u'下载次数'
    seperator = u'：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                content = ''.join(info).strip()
                if self.seperator in content:
                    label, value = [x.strip() for x in content.split(self.seperator)]
                    print label, value
                    result[label] = value

        times = etree.xpath(self.times_xpath)[-1].strip()
        print times
        result[self.label] = times

        return result

#error onclick动态生成下载链接 获得不了etree
class SinaChannel(ChannelSpider):
    """
    url: http://down.tech.sina.com.cn/3gsoft/download.php?id=296
    """
    domain = "dl.pconline.com.cn"
    fuzzy_xpath = "//li/span"
    info_xpath = "child::text()|child::p/text()"
    label = u'下载次数'
    seperator = u'：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.get_elemtree(url)

        items = etree.xpath(self.fuzzy_xpath)
        print items
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                print info
                #content = ''.join(info).strip()
                #if self.seperator in content:
                #    label, value = [x.strip() for x in content.split(self.seperator)]
                #    print label, value
                #    result[label] = value

        #times = etree.xpath(self.times_xpath)[-1].strip()
        #print times
        #result[self.label] = times

        return result

class DuoteChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://www.duote.com/soft/32673.html
    版本：3.8.2
    人气：2776
    更新：2014-05-04
    大小：9.5MB
    授权：免费软件
    语言：简体中文
    系统要求：Android 2.2 以上
    """
    domain = "www.duote.com"
    fuzzy_xpath = "//ul[@class='prop_area']/li/text()"
    label = u'人气'
    seperator = u'：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.get_elemtree(url)

        items = etree.xpath(self.fuzzy_xpath)
        print items
        for item in items:
            if item is not None:
                content = item.strip()
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        times = result.get(self.label)
        print times

        return result

class ImobileChannel(ChannelSpider):
    """
    url: http://app.imobile.com.cn/android/app/8025.html
    版 本 号：3.5.0
    所属类型：软件 / 新闻阅读
    更新时间：2013-07-01
    文件大小：6.39 MB
    下载次数：648万
    支持固件：Android 2.0以上
    开 发 者：网易
    """
    domain = "www.imobile.com.cn"
    fuzzy_xpath = "//ul[@class='app_params']/li/text()"
    label = u'下载次数'
    seperator = u'：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.get_elemtree(url)

        items = etree.xpath(self.fuzzy_xpath)
        print items
        for item in items:
            if item is not None:
                content = item.strip()
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        times = result.get(self.label)
        print times

        return result

class ApkzuChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://www.apkzu.com/soft/5206.shtml
    类别：新闻资讯
    时间：2014-1-3 14:46:45
    大小：9 M
    系统：Android 2.1及以上
    授权：免费
    评分：7 分
    语言：简体中文
    人气：1326
    """
    domain = "www.apkzu.com"
    fuzzy_xpath = "//div[@class='appInfo']/li"
    info_xpath = "child::text()|child::*/text()"
    label = u'人气'
    seperator = u'：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.get_elemtree(url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                content = ''.join(info).strip()
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

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

#error 汉字乱码
class Shop958Channel(ChannelSpider):
    """
    url: http://d.958shop.com/soft/196F4351-CCB4-46B3-9A6F-DB705CB88A75.html
    分类：实用工具
    格式：apk
    大小：27168KB
    运行平台：Android
    软件性质：免费软件
    TAG：电子词典 
    上传时间：2014-08-11
    浏览/下载次数：149224/120863次
    """
    domain = "d.958shop.com"
    fuzzy_xpath = "//table[@class='m_word']/tr[position()>2 and position()<11]/td"
    info_xpath = "child::text()|child::*/text()"
    label = u'人气'
    seperator = u'：'


    def run(self, url):
        result = {}
        storage = None
        etree = self.get_elemtree(url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                print info
                content = ''.join(info).strip()
                print content
                #label, value = [x.strip() for x in content.split(self.seperator)]
                #print label, value
                #result[label] = value

        return result


class CrskyChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://android.crsky.com/soft/25385.html
    软件名称：网易邮箱 v3.3.2 安卓版
    开发厂商：网易邮箱手机版
    软件大小：3.31 MB
    支持语言：简体中文
    所属分类：聊天通讯
    访问次数：1457
    上架时间：2014/8/22 16:34:14
    系统要求：Android 2.3,Android 3.0,Android 4.0,Android 4.1,Android 4.2
    """

    domain = "android.crsky.com"
    fuzzy_xpath = "//div[@class='left']/div[@class='s_line']/p"
    info_xpath = "child::text()|child::*//text()"
    down_xpath = "//div[@class='btns']/ul/li/a/@href"
    seperator = u'：'
    label = u'访问次数'

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

class AndroidcnChannel(ChannelSpider):
    """
    url: http://down.androidcn.com/detail/2025.html
    软件编号：2025
    更新日期：2012-09-12
    文件大小：3.20M
    下载次数：105
    """

    domain = "www.androidcn.com"
    fuzzy_xpath = "//div[@id='app-info_2']/p[position()<5]/text()"
    down_xpath = "//p[@class='dl-add-3']/a/@href"
    seperator = u'：'
    label = u'下载次数'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                content = item
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

class SohoChannel(ChannelSpider):
    """
    url: http://download.sohu.com/app/info?app_id=21174
    下载： 1455 次
    资费： 免费
    语言： 简体中文
    固件： Android 2.2
    开发商： 网之易信息技术（北京）有限公司
    大小： 10 Mb
    分类： 社交
    版本： 2.4.0
    时间： 2014-07-08
    """

    domain = "download.sohu.com"
    fuzzy_xpath = "//div[@class='gy_02']/ul/li[position()<3]/text()"
    down_xpath = "//div[@class='gy_03 clear']/div[2]/a/@href"
    seperator = u'：'
    label = u'下载'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                if u'：' in item:
                    content = item
                    #print content
                    label, value = content.split(self.seperator)
                    label = label.strip().replace(' ', '')
                    value = value.strip().replace(' ', '')
                    print label, value
                    result[label] = value

        times = result.get(self.label)
        print times
        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

#error 下载需要Cookie
class ShoujiChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://soft.shouji.com.cn/down/20275.html
    更新时间：2014-08-27
    资费提示：免费版
    当前版本：4.0.1
    软件语言：中文
    软件类别：新闻资讯
    软件大小：18.62 MB
    适用固件：1.6及更高固件
    内置广告：没有广告
    适用平台：Android
    """

    domain = "soft.shouji.com.cn"
    domain1 = "game.shouji.com.cn"
    fuzzy_xpath = "//ul[@class='des']/li[position()<10]"
    info_xpath = "child::text()|child::*/text()"
    down_xpath = "//span[@class='bdown']/a[1]/@href"
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

        #times = result.get(self.label)
        #print times
        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                              'Cookie': 'JSESSIONID=abcfXvdIMD3UlhKjxFQGu; Hm_lvt_eaff2b56fe662d8b2be9c4157d8dab61=1409462138; Hm_lpvt_eaff2b56fe662d8b2be9c4157d8dab61=1409463774'}
            storage = self.download_app(down_link, headers=headers)
           #storage = self.download_app(down_link)
        return result

class OnlineDownChannel(ChannelSpider):
    """
    url: http://down.androidcn.com/detail/2025.html
    软件编号：2025
    更新日期：2012-09-12
    文件大小：3.20M
    下载次数：105
    """

    domain = "www.onlinedown.net"
    fuzzy_xpath = "//div[@class='app_other']/ul[1]/li"
    #info_xpath = "child::text()|child::span/text()|child::a/text()|child::strong/text()"
    info_xpath = "child::text()|child::*//a/text()|child::span/text()|child::a/text()|child::strong/text()|child::div/text()"
    pagedown_xpath = "//a[@class='btn_page']/@href"
    down_xpath = "//div[@class='info']/div[@class='down-menu']/a/@href"
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
                content = ''.join(info).strip()
                #print content
                label, value = content.split(self.seperator)
                label = label.strip()
                value = value.strip()
                print label, value
                result[label] = value

        #times = result.get(self.label)
        #print times
        pagedown_link = etree.xpath(self.pagedown_xpath)[0]
        pagedown_link = self.normalize_url(url, pagedown_link)
        print pagedown_link
        downdetail = self.send_request(pagedown_link)
        down_link = downdetail.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

#error 乱码
class EoemarketChannel(ChannelSpider):
    """
    url: http://www.eoemarket.com/soft/33223.html
    下载：26万次
    大小：21.8MB
    版本：4.4.3
    更新时间：2014-08-19
    分类：阅读与图书
    适用：1.6以上
    """

    domain = "www.eoemarket.com"
    fuzzy_xpath = "//ol[@class='feileis']/li"
    info_xpath = "child::text()|child::span/text()"
    down_xpath = "//div[@class='detailsright']/ol/li[1]/a/@href"
    seperator = u'：'
    label = u'下载'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.get_elemtree(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            info = item.xpath(self.info_xpath)
            print info
            content = info[0]
            print content
            #import chardet
            #a = chardet.detect(content)
            #print a 
            #print content
            #if 'M' in content:
            #    content = content.strip()
                #print content.split(self.seperator)
                #label = label.strip()
                #value = value.strip()
                #print label, value
                #result[label] = value

        times = result.get(self.label)
        #print times
        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        #if down_link:
        #   storage = self.download_app(down_link)
        return result

class BkillChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://www.bkill.com/download/23765.html
    软件大小 7.1MB
    软件语言 简体中文
    软件授权 免费软件
    更新日期 2014-07-05
    软件人气 
    """

    domain = "www.bkill.com"
    fuzzy_xpath = "//div[@class='soft_Abstract h305 w412 l top7 bd']/ul/li[@class='right']"
    info_xpath = "child::text()|child::span/text()"
    down_xpath = "//div[@class='down_link_main']/ul/li/a/@href"
    seperator = u'：'
    label = u'软件人气'    #js生成

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

        #times = result.get(self.label)
        #print times
        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

class AibalaChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://www.aibala.com/android-soft-16102.html
    发布时间：2012-03-30
    软件大小：3MB
    版本：1.2.1
    研发公司：网易（杭州）网络有限公司MAG安卓团队
    运行环境：Android 1.6及以上

    """

    domain = "www.aibala.com"
    fuzzy_xpath = "//div[@class='tabRightM']/div[contains(@class,'tabRightM')]/text()"
    down_xpath = "//div[@class='listMainRightBottomL']/div[@class='RightB1']/a[1]/@onclick"
    seperator = u'：'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                label, value = item.split(self.seperator)
                label = label.strip()
                value = value.strip()
                print label, value
                result[label] = value

        down_link = etree.xpath(self.down_xpath)[0]
        r = re.compile("window.location.href='(.+)';return false;")
        down_link = r.search(down_link)
        down_link = down_link.group(1)
        print down_link
        if down_link:
           down_link = self.normalize_url(url, down_link)
           storage = self.download_app(down_link)
        return result

class VmallChannel(ChannelSpider):
    """
    url: http://app.vmall.com/app/C9147
    下载：18991665次
    大小：18.62MB
    日期：2014-08-26
    开发者：网之易信息技术…
    版本：4.0.1

    """

    domain = "app.vmall.com"
    times_xpath = "//div[@class='app-info flt']/ul[1]/li[2]/p/span[2]/text()"
    fuzzy_xpath = "//div[@class='app-info flt']/ul[2]/li[position()<5]"
    info_xpath = "child::text()|child::span/text()"
    down_xpath = "//a[@class='mkapp-btn mab-download']/@onclick"
    seperator = u'：'
    label = u'下载'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                content = ''.join(info)
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        times = etree.xpath(self.times_xpath)[0]
        tlable, tvalue = [x.strip() for x in times.split(self.seperator)]
        result[tlable] = tvalue
        times = result.get(self.label)
        print times

        down_link = etree.xpath(self.down_xpath)[0]
        r = re.compile("'(http://appdl\.hicloud\.com/[^']+)'")
        down_link = r.search(down_link)
        down_link = down_link.group(1)
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

class YruanChannel(ChannelSpider):
    """
    url: http://www.yruan.com/softdetail/584/
    软件分类： 网络浏览
    软件资费： 免费软件
    更新时间： 2011-06-01
    软件语言： 中文
    软件大小： 2M
    下载次数： 49 
    """

    domain = "www.yruan.com"
    times_xpath = "//div[@class='app-info flt']/ul[1]/li[2]/p/span[2]/text()"
    fuzzy_xpath = "//ul[@class='Download-m']//dl[@class='leftdl']/dt"
    info_xpath = "child::text()|child::*/text()"
    down_xpath = "//li[@class='downimg']/div[@class='down_link']/a/@href"
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
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        times = result.get(self.label)
        print times

        pagedown_link = etree.xpath(self.down_xpath)[0]
        if pagedown_link is not None:
            r = re.compile("id=([0-9]+)&")
            soft_id = r.search(pagedown_link)
            soft_id = soft_id.group(1)
            down_link = "http://www.yruan.com/down.php?id=%s" % soft_id
            print down_link

            if down_link:
               storage = self.download_app(down_link)

        return result


class ZhuodownChannel(ChannelSpider):
    """
    ***无下载次数***
    url: http://www.anzow.com/download/Software/JQKRDPQQP8.shtml
    所属分类：通讯辅助
    授权方式：免费使用
    软件大小：3.1MB
    应用版本：1.0.1
    软件语言：简体中文
    适用平台：Android 2.3+
    推荐指数：★★☆☆☆
    作者：网易
    更新时间：2014-7-16 11:33:26
    """

    domain = "www.zhuodown.com"
    fuzzy_xpath = "//dl[@class='down_info clear']/dd/dl/dt/ul/li"
    info_xpath = "child::text()|child::*/text()|child::*/*/text()"
    pagedown_xpath = "//ul[@class='downurllist']/a/@href"
    down_xpath = "//div[@class='advancedsearch']/table/tr[2]/td/li[1]/a/@href"
    seperator = u'：'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                content = ''.join(info)
                print content
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

class Xz7Channel(ChannelSpider):
    """
    ***无下载次数***
    url: http://www.7xz.com/softs/view/10034884
    大小：13.62MB
    格式：apk
    更新日
    """

    domain = "www.7xz.com"
    fuzzy_xpath = "//div[@class='values']/ul/li[@class='c1']"
    info_xpath = "child::text()|child::*/text()"
    down_xpath = "//div[@class='downloadWrap1']/div[@class='diannao']/a/@href"
    seperator = u'：'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                info = item.xpath(self.info_xpath)
                content = ''.join(info)
                print content
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result


class Channel3533Channel(ChannelSpider):
    """
    ***无下载次数***
    url: http://game.3533.com/ruanjian/974.htm
    版本：V3.5 Build 19 
    大小：4.0 MB 格式：APK 
    系统要求：安卓2.2以上系统 
    适用屏幕像素：通用 
    """

    domain = "www.3533.com"
    fuzzy_xpath = "//div[@class='appdownbox']/dl[1]//div[@class='packinfo']/p[1]//span/text()"
    down_xpath = "//div[@class='appdownbox']/dl[1]//div[@class='packdown']/a/@href"
    seperator = u'：'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        print items
        for item in items:
            if self.seperator in item:
                content = item.strip()
                label, value = [x.strip() for x in content.split(self.seperator)]
                print label, value
                result[label] = value

        down_link = etree.xpath(self.down_xpath)[0]
        print down_link
        if down_link:
           storage = self.download_app(down_link)
        return result

class BaicentChannel(ChannelSpider):
    """
    url: http://www.baicent.com/plus/view-288996-1.html
    软件类型：国产软件 
    授权方式：共享软件 
    界面语言：简体中文 
    软件大小： 
    文件类型： 
    运行环境：Android 
    软件等级：★★★☆☆ 
    发布时间：2011-09-23 
    官方网址： 
    演示网址： 
    下载次数：0 
    """

    domain = "www.baicent.com"
    fuzzy_xpath = "//div[@class='viewbox']/div[@class='infolist']"
    label_xpath = "child::small/text()"
    value_xpath = "child::span/text()"
    down_xpath = "//ul[@class='downurllist']/li[1]/a/@href"
    label = u'下载次数'
    seperator = u'：'

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        item = etree.xpath(self.fuzzy_xpath)[0]
        if item is not None:
            labels = item.xpath(self.label_xpath)
            print labels
            values = item.xpath(self.value_xpath)
            info = zip(labels, values)
            for content in info:
                label, value = content
                print label, value
                result[label] = value

        times = result.get(self.label)

        down_link = etree.xpath(self.down_xpath)[0]
        down_link = self.normalize_url(url, down_link)
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

    #url = "http://dl.pconline.com.cn/download/172907.html"
    #pconline = PcOnlineChannel()
    #print pconline.run(url)

    #url = "http://down.tech.sina.com.cn/3gsoft/download.php?id=296"
    #sina = SinaChannel()
    #print sina.run(url)

    #url = "http://www.duote.com/soft/32673.html"
    #duote = DuoteChannel()
    #print duote.run(url)

    #url = "http://app.imobile.com.cn/android/app/8025.html"
    #imobile = ImobileChannel()
    #print imobile.run(url)

    #url = "http://www.apkzu.com/soft/5206.shtml"
    #apkzu = ApkzuChannel()
    #print apkzu.run(url)

    #url = "http://www.nduoa.com/apk/detail/11990"
    #nduoa = NduoaChannel()
    #print nduoa.run(url)

    #url = "http://android.155.cn/soft/10198.html"
    #android115 = Android115Channel()
    #print android115.run(url)

    url = "http://d.958shop.com/soft/196F4351-CCB4-46B3-9A6F-DB705CB88A75.html"
    shop958 = Shop958Channel()
    print shop958.run(url)

    #url = "http://os-android.liqucn.com/rj/12910.shtml"
    #liqucn = LiqucnChannel()
    #print liqucn.run(url)

    #url = "http://android.crsky.com/soft/25385.html"
    #crsky = CrskyChannel()
    #print crsky.run(url)

    #url = "http://down.androidcn.com/detail/2025.html"
    #Androidcn = AndroidcnChannel()
    #print Androidcn.run(url)

    #url = "http://download.sohu.com/app/info?app_id=21174"
    #soho = SohoChannel()
    #print soho.run(url)

    #url = "http://soft.shouji.com.cn/down/20275.html"
    #shouji = ShoujiChannel()
    #print shouji.run(url)

    #url = "http://www.onlinedown.net/soft/110940.htm"
    #onlinedown = OnlineDownChannel()
    #print onlinedown.run(url)

    #url = "http://www.eoemarket.com/soft/33223.html"
    #eoemarket = EoemarketChannel()
    #print eoemarket.run(url)

    #url = "http://www.bkill.com/download/23765.html"
    #bkill = BkillChannel()
    #print bkill.run(url)

    #url = "http://www.aibala.com/android-soft-16102.html"
    #aibala = AibalaChannel()
    #print aibala.run(url)

    #url = "http://app.vmall.com/app/C9147"
    #vmall = VmallChannel()
    #print vmall.run(url)

    #url = "http://www.yruan.com/softdetail/584/"
    #yruan = YruanChannel()
    #print yruan.run(url)

    #url = "http://www.anzow.com/download/Software/JQKRDPQQP8.shtml"
    #anzow = AnzowChannel()
    #print anzow.run(url)

    #url = "http://www.7xz.com/softs/view/10034884"
    #xz7 = Xz7Channel()
    #print xz7.run(url)

    #url = "http://www.wandoujia.com/apps/com.netease.newsreader.activity"
    #wandoujia = WandoujiaChannel()
    #print wandoujia.run(url)

    #url = "http://game.3533.com/ruanjian/974.htm"
    #channel3533 = Channel3533Channel()
    #print channel3533.run(url)

    #url = "http://www.baicent.com/plus/view-288996-1.html"
    #baicent = BaicentChannel()
    #print baicent.run(url)
