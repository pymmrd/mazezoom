# -*- coding:utf-8 -*-

#Author:zoug
#Date:2014/08/20
#Email:b.zougang@gmail.com


"""
    渠道下载页面爬虫:
    抓取因子：软件大小，版本，下载次数, 软件
    下载次数抓取策略：
        1.位于detail页面的可以直接抓取
        2.位于搜索结果中的可以保存此app在搜索结果中的名字,
          重新搜索获取下载次数
"""

import re
import urlparse

if __name__ == "__main__":
    import os
    import sys
    current_path = os.path.abspath(os.path.dirname(__file__))
    creepers_path = os.path.abspath(os.path.dirname(current_path))
    sys.path.append(creepers_path)

from base import ChannelSpider

class ZhuShou360Channel(ChannelSpider):
    seperator = u'：'
    domain = "zhushou.360.cn"
    size_xpath = "//div[@class='pf']/span[@class='s-3'][2]/text()"

    def download_times(self):
        from position import ZhuShou360Position
        position = ZhuShou360Position(
            self.title,
            has_orm=False,
        )
        times = position.download_times()
        return times

    def parser(self):
        result = {}
        etree = self.send_request(self.url)
        size_raw = etree.xpath(self.size_xpath)
        if size_raw:
            size_raw = size_raw[0].strip()
            result['size'] = size_raw
        times = self.download_times()
        result['download_times'] = times
        return result


class MiChannel(ChannelSpider):
    """
    url: http://app.mi.com/detail/19732
    软件大小: 30.82 M
    版本号：1.9.6
    更新时间：2014-09-01
    包名：com.halfbrick.fruitninja
    """
    domain = "app.mi.com"
    times_xpath = "//div[@class='intro-titles']/span[@class='app-intro-comment']"
    fuzzy_xpath = "//div[@class='details preventDefault']/ul/li[@class='weight-font']"
    value_xpath = "following::li"

    def download_times(self, etree):
        times = None

        regx = re.compile('\d+')
        dom = etree.xpath(self.times_xpath)[0]
        number_text = dom.text_content().strip()
        if number_text:
            match = regx.search(number_text)
            if match is not None:
                rawtimes = match.group(0)
                try:
                    times = int(rawtimes)
                except (TypeError, ValueError):
                    pass
        return times

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'版本号': 'human_version',
            u'更新时间': 'update_time',
            u'包名': 'name',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            label = item.text_content().strip()[:-1]
            value_dom = item.xpath(self.value_xpath)[0]
            value = value_dom.text_content()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        print result
        return result

class NearMeChannel(ChannelSpider):
    """
    url: http://store.nearme.com.cn/product/0000/563/963_1.html?from=1152_2
    发布时间：2014.09.28
    大小：29.51M
    版本：1.9.6
    类别：休闲游戏
    适用系统：Andriod2.3.3及以上
    下载：900万+次下载 
    """
    seperator = u'：'
    domain = "store.nearme.com.cn"
    times_xpath = "//div[@class='soft_info_nums']/text()"
    fuzzy_xpath = "//ul[@class='soft_info_more']/li"

    def download_times(self, etree):
        times = None

        translate = u"万"
        regx = re.compile('\d+')
        number_text = ''.join(etree.xpath(self.times_xpath)).strip()
        if number_text:
            match = regx.search(number_text)
            if match is not None:
                rawtimes = match.group(0)
                try:
                    times = int(rawtimes)
                except (TypeError, ValueError):
                    pass
                else:
                    if translate in number_text:
                        times = times * 10000
        return times

    def parser(self):
        result = {}
        mapping = {
            u'大小': 'size',
            u'版本': 'human_version',
            u'发布时间': 'update_time',
            u'类别': 'category',
            u'适用系统': 'env',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
                    print label, value

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        print result
        return result

class UCChannel(ChannelSpider):
    """
    url: http://apps.uc.cn/detail?appChannelId=456916
    版本：V1.0.0
    分类：动作游戏
    大小：8.7M
    更新时间：2014-10-10
    资费说明：使用完全免费
    """
    seperator = u'：'
    domain = "apps.uc.cn"
    fuzzy_xpath = "//div[@class='param']/dl[position()<last()]"

    def parser(self):
        result = {}
        mapping = {
            u'大小': 'size',
            u'版本': 'human_version',
            u'更新时间': 'update_time',
            u'分类': 'category',
            u'资费说明': 'price',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            print content
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
                    print label, value

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        print result
        return result


class LenovoChannel(ChannelSpider):
    domain = 'app.lenovo.com'

class M163Channel(ChannelSpider):
    domain = "m.163.com"


class Sj91Channel(ChannelSpider):
    domain = "sj.91.com"

class Gao7Channel(ChannelSpider):
    domain = "www.gao7.com"


class AndroidmiChannel(ChannelSpider):
    domain = "www.androidmi.com"


class Vapp51Channel(ChannelSpider):
    domain = "www.51vapp.com"


class OperaChannel(ChannelSpider):
    domain = "apps.opera.com"
    

class AppchinaChannel(ChannelSpider):
    domain = "www.appchina.com"


class Zhidian3Channel(ChannelSpider):
    domain = "app.zhidian3g.cn"


class PaojiaoChannel(ChannelSpider):
    domain = "kuang.paojiao.cn"


class TompdaChannel(ChannelSpider):
    domain = "android.tompda.com"


class BorporChannel(ChannelSpider):
    domain = "www.borpor.com"


class MaopaokeChannel(ChannelSpider):
    domain = "www.maopaoke.com"


class SoyingyongChannel(ChannelSpider):
    domain = "www.soyingyong.com"


class BaikceChannel(ChannelSpider):
    domain = "apps.baikce.cn"


class SoftonicChannel(ChannelSpider):
    domain = "www.softonic.cn"


class A280Channel(ChannelSpider):
    domain = "www.a280.cn"


class MeizumiChannel(ChannelSpider):
    domain = "www.meizumi.com"


class CncrkChannel(ChannelSpider): 
    domain = "www.cncrk.com"


class ZerosjChannel(ChannelSpider):
    domain = "www.zerosj.com"


class AppdhChannel(ChannelSpider):
    domain = "www.appdh.com"


class ItopdogChannel(ChannelSpider):
    domain = "www.itopdog.cn"


class MogustoreChannel(ChannelSpider):
    domain = "www.mogustore.cn"


class LeidianChannel(ChannelSpider):
    domain = "www.leidian.com"


class Channel2265(ChannelSpider):
    domain = "www.2265.com"

if __name__ == '__main__':
    mi = MiChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://app.mi.com/detail/19732',
        title=u'水果忍者'
    )
    #mi.run()

    nearme = NearMeChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://store.nearme.com.cn/product/0000/553/613_1.html?from=1152_1',
        title=u'水果忍者'
    )
    #nearme.run()

    uc = UCChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://apps.uc.cn/detail?appChannelId=456916',
        title=u'忍者砍僵尸'
    )
    #uc.run()
