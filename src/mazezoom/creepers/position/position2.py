# -*- coding:utf-8 -*-

#Author: zoug
#Email: b.zougang@gmail.com
#Date: 2014/09/28

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


class ZhuShou360Position(PositionSpider):
    """
    (S,D)
    """
    name = u'360手机助手'
    domain = "zhushou.36.cn"
    base_xpath = "//div[@class='SeaCon']/ul/li"
    search_url = "http://zhushou.360.cn/search/index/?kw=%s"
    link_xpath = "//child::dl/dd/h3/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.attrib['title']
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results


class TaoBaoPosition(PositionSpider):
    name = u'淘宝手机助手'
    domain = "app.taobao.com"
    abstract = True


class MiPosition(PositionSpider):
    name = u'小米应用商店'
    domain = "app.mi.com"
    search_url = "http://app.mi.com/searchAll?keywords=%s&typeall=phone"
    xpath = "//ul[@class='applist']/li/h5/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.xpath)
        for item in items:
            title = item.attrib['title']
            if self.app_name in title:
                link = self.normalize_url(
                    self.search_url,
                    item.attrib['href']
                )
                results.append((link, title))
        return results


class NearMePosition(PositionSpider):
    """
    (S, D)
    """
    name = u'可可'
    domain = "store.nearme.com.cn"
    search_url = "http://store.nearme.com.cn/search/do.html?keyword=%s&nav=index"
    base_xpath = "//div[@class='list_item']"
    link_xpath = "child::div[@classs='li_middle']/div/a" 

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(link_xpath)[0]
            title = elem.text.strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results


class LenovoPosition(PositionSpider):
    """
    (S, D)
    """
    name = u'乐商店'
    doamin = 'app.lenovo.com'
    search_url = "http://app.lenovo.com/search/index.html?q=%s"
    base_xpath = "//ul[@class='appList']/li[@class='borderbtm1 pr']"
    link_xpath = "child::div[@class='appDetails']/p[@class='f16 ff-wryh appName']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(link_xpath)[0]
            title = elem.text.strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results
        
