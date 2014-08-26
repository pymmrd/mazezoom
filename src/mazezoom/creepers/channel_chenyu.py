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
