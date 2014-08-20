# -*- coding:utf-8 -*-

#Author:zoug
#Date:2014/08/20
#Email:b.zougang@gmail.com


"""
    渠道下载页面爬虫:
    抓取因子：软件大小，版本，下载次数, 软件
"""

from base import ChannelSpider


class OykSoftChannel(ChannelSpider):
    """
    页面包含因子: 
        软件大小：16.03 MB
        软件语言：简体中文
        授权类型：免费版
        软件类别：国产软件/Android
        责任编辑：快乐无极
        运行环境：GoogleAndroid
        更新时间：2014/8/19 13:00:42
        关键词项：VST全聚合 全媒体聚合 VST电视直播 电视回播 视频点播
    """
    domain = "www.oyksoft.com"
    down_xpath = "//a[@class='normal']/@href"
    fuzzy_xpath = "//div[@id='softinfo']/ul/li"
    label_xpath = "child::strong/text()"
    value_xpath = "child::text()"

    def run(self, url):
        result = {}
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
            result[label] = value
        return result

if __name__ == '__main__':
    url = "http://www.oyksoft.com/soft/32456.html"
    oyk = OykSoftChannel()
    print oyk.run(url)
    
