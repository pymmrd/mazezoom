# -*- coding:utf-8 -*-

#Author:zoug
#Date:2014/08/20
#Email:b.zougang@gmail.com


"""
    渠道下载页面爬虫:
    抓取因子：软件大小，版本，下载次数, 软件
"""

form base import ChannelSpider


class OykSoftChannel(ChannelSpider):
    domain = "www.oyksoft.com"
    down_xpath = "//a[@class='normal']/@href"
    down_
