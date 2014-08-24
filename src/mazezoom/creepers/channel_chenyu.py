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
                value = item.xpath(self.value_xpath)[0]
                print label, value
                result[label.strip()] = value.strip()

        down_link = etree.xpath(self.down_xpath)[0]
        down_link = self.normalize_url(url, down_link)
        if down_link:
           storage = self.download_app(down_link)
        return result 

class AngeeksChannel(ChannelSpider):
    """
    >>>angeek = AngeeksPosition()
    >>>angeek.run(u'飞机')
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

if __name__ == '__main__':
    url = "http://apk.hiapk.com/appinfo/com.tencent.mm"
    hiapk = HiapkChannel()
    print hiapk.run(url)

    #url = "http://apk.angeeks.com/soft/10069485.html"
    #angeeks = AngeeksChannel()
    #print angeeks.run(url)
