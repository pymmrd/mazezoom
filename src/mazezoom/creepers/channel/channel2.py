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
import json
import urlparse

if __name__ == "__main__":
    import os
    import sys
    current_path = os.path.abspath(os.path.dirname(__file__))
    creepers_path = os.path.abspath(os.path.dirname(current_path))
    sys.path.append(creepers_path)
    sys.path.append('/root/mazezoom/src/mazezoom/creepers/position')

from base import ChannelSpider

class ZhuShou360Channel(ChannelSpider):
    seperator = u'：'
    domain = "zhushou.360.cn"
    size_xpath = "//div[@class='pf']/span[@class='s-3'][2]/text()"

    def download_times(self):
        from position2 import ZhuShou360Position
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

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
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
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result


class LenovoChannel(ChannelSpider):
    """
    url: http://www.lenovomm.com/app/15396162.html
    大小：78.96MB
    版本：1.6.0
    适用系统：Android 2.3.1以上
    开发者：上海乐堂网络科技有限公司
    更新时间：2014-09-29
    下载：108万次安装
    """
    seperator = u'：'
    domain = 'app.lenovo.com'
    times_xpath = "//div[@class='f12 detailDownNum cb clearfix']/span"
    fuzzy_xpath = "//li[@class='f12 fgrey4 txtCut']"

    def download_times(self, etree):
        times = None

        translate = u"万"
        translate2 = u"千"
        regx = re.compile('\d+')
        number_dom = etree.xpath(self.times_xpath)[0]
        number_text = number_dom.text_content()
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
                    elif translate2 in number_text:
                        times = times * 1000
        return times

    def parser(self):
        result = {}
        mapping = {
            u'大小': 'size',
            u'版本': 'human_version',
            u'更新时间': 'update_time',
            u'开发者': 'company',
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

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class M163Channel(ChannelSpider):
    """
    url: http://m.163.com/android/software/323s6t.html
    价格： 	免费 	
    类别：	休闲益智
    大小：	29.51M 	
    语言：	中文
    版本：	1.9.6
    开发者：	乐逗游戏
    """
    seperator = u'：'
    domain = "m.163.com"
    fuzzy_xpath = "//table[@class='table-appinfo']/tr/th"
    value_xpath = "following::td[1]"

    def parser(self):
        result = {}
        mapping = {
            u'价格': 'price',
            u'类别': 'category',
            u'大小': 'size',
            u'语言': 'language',
            u'版本': 'human_version',
            u'开发者': 'company',
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

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class Sj91Channel(ChannelSpider):
    """
    url: http://play.91.com/android/App/index-12599.html
    版本： 1.0.1 
    文件大小：37 MB
    适用固件：Android 2.3.3 及以上
    分享日期： 2014-01-13
    开发商：Halfbrick Studios
    热门标签：水果忍者大战彩虹糖,休闲,益智,娱乐
    """
    seperator = u'：'
    domain = "sj.91.com"
    fuzzy_xpath = "//div[@class='left detail_page_intro_c']/p/span"

    def download_times(self):
        from position2 import Sj91Position
        position = Sj91Position(
            self.title,
            has_orm=False,
        )
        times = position.download_times()
        return times

    def parser(self):
        result = {}
        mapping = {
            u'版本': 'human_version',
            u'文件大小': 'size',
            u'适用固件': 'env',
            u'分享日期': 'update_time',
            u'开发商': 'company',
            u'热门标签': 'category',
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

        times = self.download_times()
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class Gao7Channel(ChannelSpider):
    """
    url: http://d.gao7.com/game/android-97872-20140328.html
    游戏版本：1.1006
    游戏大小：6.8M
    适用机型： Android 2.2及以上 
    """
    seperator = u'：'
    domain = "www.gao7.com"
    label_xpath = "//dd[@class='app-meta fl']/p/text()"
    value_xpath = "//dd[@class='app-meta fl']/p/strong/text()"

    def parser(self):
        result = {}
        mapping = {
            u'游戏大小': 'size',
            u'游戏版本': 'human_version',
            u'适用机型': 'env',
        }

        etree = self.send_request(self.url)
        label_dom = etree.xpath(self.label_xpath)
        value_dom = etree.xpath(self.value_xpath)
        labels = []
        values = []
        if label_dom:
            labels = [l.strip()[:-1] for l in label_dom if l.strip()]

        if value_dom:
            values = [v.strip() for v in value_dom if v.strip()]

        items = zip(labels, values)
        for item in items:
            label, value = item
            label = mapping.get(label, '')
            if label:
                result[label] = value

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

#error 太繁琐
class AndroidmiChannel(ChannelSpider):
    domain = "www.androidmi.com"


class Vapp51Channel(ChannelSpider):
    """
    url: http://www.51vapp.com/market/apps/detail.vhtml?appPkg=com.halfbrick.fruitninja
    价格：免费
    版本：1.9.5
    大小：30.49 M
    语言：中文
    下载：10624 次
    支持固件：Android2.3.3及以上 
    """
    seperator = u'：'
    domain = "www.51vapp.com"
    fuzzy_xpath = "//span[@class='fl']/p[2]/text()"

    def download_times(self, dtimes):
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            rawtimes = match.group(0)
            try:
                times = int(rawtimes)
            except (TypeError, ValueError):
                times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'价格': 'price',
            u'版本': 'human_version',
            u'大小': 'size',
            u'语言': 'language',
            u'下载': 'download_times',
            u'支持固件': 'env',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item:
                elems = item.strip().split(self.seperator)
                if len(elems) == 2:
                    label, value = elems
                    label = label.strip()
                    label = mapping.get(label, '')
                    if label:
                        result[label] = value.strip()

        times = result.get('download_times', '')
        result['download_times'] = self.download_times(times)
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class OperaChannel(ChannelSpider):
    """
    url: http://apps.opera.com/zh_cn/saasfet4744.html
    下载: 1 
    更新的: 2013-02-16
    """
    seperator = u':'
    domain = "apps.opera.com"
    fuzzy_xpath = "//div[@class='metaData']/span"

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'下载': 'download_times',
            u'更新的': 'update_time',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items[1:]:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        times = self.download_times(
            result.get('download_times', '')
        )
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class AppChinaChannel(ChannelSpider):
    """
    url: http://www.appchina.com/app/com.netease.rz
    更新：2014-08-14
    版本：1.1.0
    要求：Android 2.2以上
    """
    seperator = u'：'
    domain = "www.appchina.com"
    fuzzy_xpath = "//p[@class='art-content']/text()"
    times_xpath = "//span[@class='app-statistic']"

    def download_times(self, etree):
        times = 0
        translate = u"万"
        regx = re.compile('[\d\.]+')

        times_dom = etree.xpath(self.times_xpath)[0]
        content = times_dom.text_content().strip()
        number_text = content.split('/')[0]
        match = regx.search(number_text)
        if match is not None:
            rawtimes = match.group(0)
            try:
                times = float(rawtimes)
            except (TypeError, IndexError, ValueError):
                pass
            else:
                if translate in number_text:
                    times = times * 10000

            times = int(times)
        return times

    def parser(self):
        result = {}
        mapping = {
            u'更新': 'update_time',
            u'版本': 'human_version',
            u'要求': 'env',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item:
                elems = item.strip().split(self.seperator)
                if len(elems) == 2:
                    label, value = elems
                    label = label.strip()
                    label = mapping.get(label, '')
                    if label:
                        result[label] = value.strip()

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class Zhidian3gChannel(ChannelSpider):
    """
    url: http://app.zhidian3g.cn/appSoftware_download.shtml?id=2046
    应用版本：1.0
    系统要求：Android 2.0以上
    软件大小：9.8 M
    更新时间：2014-09-10
    """
    seperator = u'：'
    domain = "app.zhidian3g.cn"
    fuzzy_xpath = "//div[@class='article_side_app_info']/ul/li"

    def parser(self):
        result = {}
        mapping = {
            u'应用版本': 'human_version',
            u'系统要求': 'env',
            u'软件大小': 'size',
            u'更新时间': 'update_time',
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

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class PaojiaoChannel(ChannelSpider):
    """
    url: http://kuang.paojiao.cn/danji/detail_1546.html
    状态：公测    
    平台：安卓
    类型：即时    
    大小：8.6M
    """
    seperator = u'：'
    domain = "kuang.paojiao.cn"
    fuzzy_xpath = "//div[@class='appinfo-content']/p"

    def download_times(self):
        from position2 import PaojiaoPosition
        position = PaojiaoPosition(
            self.title,
            has_orm=False,
        )
        times = position.download_times()
        return times

    def parser(self):
        result = {}
        mapping = {
            u'状态': 'state',
            u'平台': 'env',
            u'类型': 'category',
            u'大小': 'size',
        }

        etree = self.get_elemtree(self.url, ignore=True)
        items = etree.xpath(self.fuzzy_xpath)
        infos = []
        for item in items[1:]:
            content = item.text_content()
            info = content.split(' ')
            infos.extend(info)

        for info in infos:
            elems = info.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
            
        times = self.download_times()
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class TompdaChannel(ChannelSpider):
    """
    url: http://android.tompda.com/48127.html
    软件类型：动作游戏                   
    软件版本：1.5.4
    资费类型：完全免费                   
    软件大小：17.6MB
    软件时间：2011-04-28
    热门标签：超棒 有创意 画面精美 。。。 好 扣人心弦 非常好 兴奋
    """
    seperator = u'：'
    domain = "android.tompda.com"
    times_xpath = "//div[@class='mainBody1_right']/p/text()"
    fuzzy_xpath = "//div[@class='mainBody1_left_2_p']/p/text()"

    def download_times(self, etree):
        times = None

        regx = re.compile('\d+')
        number_text = etree.xpath(self.times_xpath)[0]
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
            u'软件类型': 'category',
            u'软件版本': 'human_version',
            u'资费类型': 'price',
            u'软件大小': 'size',
            u'软件时间': 'update_time',
            u'热门标签': 'tag',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        items = [x.strip() for x in items if x.strip()]    #去除空格元素
        infos = []
        for item in items:
            if item:
                regx = re.compile(u'\xa0+')
                content = re.sub(regx, ' ', item)
                info = content.split(' ')
                infos.extend(info)
                
        for info in infos:
            elems = info.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class BorporChannel(ChannelSpider):
    """
    url: http://www.borpor.com/enddisplay.php?gid=17041
    资费： 	0 
    作者： 	wan123
    版本： 	V1.8.7
    发布时间： 	2014-08-12
    软件大小： 	8.00 MB
    """
    seperator = u'：'
    domain = "www.borpor.com"
    fuzzy_xpath = "//table[@class='f-11-b3b3b3']/tr"

    def parser(self):
        result = {}
        mapping = {
            u'资费': 'price',
            u'作者': 'company',
            u'版本': 'human_version',
            u'发布时间': 'update_time',
            u'软件大小': 'size',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items[2:-2]:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class MaopaokeChannel(ChannelSpider):
    """
    url: http://store.nearme.com.cn/product/0000/563/963_1.html?from=1152_2
    类型：网游-即时 
    版本：2.3.0 
    游戏包大小：66.8M 
    上线时间：2014.09.04
    标签：格斗 动漫 忍者 王者 动作
    """
    seperator = u'：'
    domain = "www.maopaoke.com"
    fuzzy_xpath = "//div[@class='app-info']/div[@class='row']"

    def parser(self):
        result = {}
        mapping = {
            u'类别': 'category',
            u'版本': 'human_version',
            u'游戏包大小': 'size',
            u'上线时间': 'update_time',
            u'标签': 'tag',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        infos = []
        for item in items:
            content = item.text_content().strip()
            info = content.split('\n')
            infos.extend(info)

        for info in infos:
            elems = info.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

#404
class SoyingyongChannel(ChannelSpider):
    domain = "www.soyingyong.com"

class BaikceChannel(ChannelSpider):
    """
    url: http://www.baikce.cn/app/67362.html
    APK大小： 	50KB
    更新日期： 	2014-08-01
    软件授权： 	软件
    最新版本： 	网页版
    适用平台： 	Android系统平台
    开发者官方： 	www.baikce.cn/360/
    """
    seperator = u'：'
    domain = "apps.baikce.cn"
    times_xpath = "//span[@class='col-94 download-num'][1]"
    fuzzy_xpath = "//div[@class='detailed-info']/table/tbody/tr"

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
            u'APK大小': 'size',
            u'更新日期': 'update_time',
            u'版本授权': 'authorize',
            u'最新版本': 'human_version',
            u'适用平台': 'env',
            u'开发者官方': 'company',
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

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class SoftonicChannel(ChannelSpider):
    """
    url: http://ninja-rush.softonic.cn/android
    软件授权:免费软件 
    语言:简体中文 
    操作系统:Android
    最新版本:1.21 Android 2012-02-17 
    最近一个月下载量:224 
    开发者:http://www.feelingtouch.com/
    """
    seperator = u'：'
    domain = "www.softonic.cn"
    fuzzy_xpath = "//div[@id='program_info']/dl/dt"
    value_xpath = "following::dd[1]"
    company_xpath = "////div[@id='program_info']/dl/dd[last()]/a/@href"

    def download_times(self):
        from position2 import SoftonicPosition
        position = SoftonicPosition(
            self.title,
            has_orm=False,
        )
        times = position.download_times()
        return times

    def parser(self):
        result = {}
        mapping = {
            u'软件授权': 'authorize',
            u'语言': 'language',
            u'操作系统': 'env',
            u'最新版本': 'human_version',
            u'开发者': 'company',
        }

        etree = self.get_elemtree(self.url, ignore=True)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items[:-1]:
            label = item.text_content().strip()[:-1]
            value_dom = item.xpath(self.value_xpath)[0]
            value = value_dom.text_content()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()
        company_site = etree.xpath(self.company_xpath)[0]
        result['company'] = company_site

        times = self.download_times()
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class A280Channel(ChannelSpider):
    """
    url: http://www.a280.com/soft/haidaodazhanrenzhehaohuaban.v2.1.0
    所属分类：动作冒险
    系统需求：1.6以上
    界面语言：英文
    软件类型：免费
    软件大小：8.36M
    更新时间：2012-04-14
    """
    seperator = u'：'
    domain = "www.a280.cn"
    fuzzy_xpath = "//div[@class='des']/ul/li"

    def parser(self):
        result = {}
        mapping = {
            u'所属分类': 'category',
            u'系统需求': 'env',
            u'界面语言': 'language',
            u'软件类型': 'price',
            u'软件大小': 'size',
            u'更新时间': 'update_time',
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

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class MeizumiChannel(ChannelSpider):
    """
    url: http://www.meizumi.com/apk/2408.html
    游戏名称：豆腐忍者 
    应用包名：com.idreamsky.tofu
    最新版本：1.3.5
    支持系统：Android 1.5
    游戏分类：益智休闲
    界面语言：简体中文
    游戏大小：21.2 MB
    更新日期：2012-01-14
    """
    seperator = u'：'
    domain = "www.meizumi.com"
    times_xpath = "//div[@class='info_row3']/span[1]"
    fuzzy_xpath = "//div[@class='app_info']/p"

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
            u'游戏名称': 'name',
            u'最新版本': 'human_version',
            u'支持系统': 'env',
            u'游戏分类': 'category',
            u'界面语言': 'language',
            u'游戏大小': 'size',
            u'更新时间': 'update_time',
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

        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class CncrkChannel(ChannelSpider): 
    """
    url: http://www.cncrk.com/downinfo/65995.html
    软件大小：47 MB 【我要点评？】
    软件语言：简体中文
    软件类别：手机软件 / 免费软件 / Android
    运行环境：Android
    更新时间：2014/10/12 13:13:20
    软件标签：水果忍者休闲游戏
    """
    seperator = u'：'
    domain = "www.cncrk.com"
    charset = 'gb2312'
    fuzzy_xpath = "//div[@id='softinfo']/ul/li"

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'软件语言': 'language',
            u'软件类别': 'category',
            u'运行环境': 'env',
            u'更新时间': 'update_time',
            u'软件标签': 'tag',
        }

        #etree = self.send_request(self.url)
        etree = self.get_elemtree(self.url, ignore=True)
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

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

#error 网站打不开
class ZerosjChannel(ChannelSpider):
    domain = "www.zerosj.com"


class AppdhChannel(ChannelSpider):
    """
    url: http://www.appdh.com/app/renzhetuxi-ninja-rush/
    分类：冒险类
    版本：1.20
    更新：2011-12-13
    语言：简体中文
    固件：Android 2.0 以上
    作者：Feelingtouch Inc.
    官网：http://www.feelingtouch.com
    下载：463 次
    """
    seperator = u'：'
    domain = "www.appdh.com"
    fuzzy_xpath = "//div[@class='grid_7 alpha omega']/p"

    def download_times(self, dtimes):
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            rawtimes = match.group(0)
            try:
                times = int(rawtimes)
            except (TypeError, ValueError):
                times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'分类': 'category',
            u'版本': 'human_version',
            u'更新': 'update_time',
            u'语言': 'language',
            u'固件': 'env',
            u'作者': 'company',
            u'官网': 'website',
            u'下载': 'download_times',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content()#.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        times = result.get('download_times', '')
        result['download_times'] = self.download_times(times)
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class ItopdogChannel(ChannelSpider):
    """
    url: http://www.itopdog.cn/az/fruitninja.html
    资源大小:31.33 kb
    语言种类:简体中文
    应用分类:角色扮演
    系统要求:Android 
    """
    seperator = u'：'
    domain = "www.itopdog.cn"
    times_xpath = "//div[@class='nine down_all']"
    fuzzy_xpath = "//dl[@class='clearfix appinfo']/dt"
    value_xpath = "following::dd[1]"

    def download_times(self, url):
        times = None
        regx = re.compile('id = \'(?P<id>\d+)\'')
        content = self.get_content(url)
        match = regx.search(content)
        if match is not None:
            id = match.group('id')

            times_url = 'http://www.itopdog.cn/home.php?ct=home&ac=get_updown_api&id=%s' % id
            down_info = self.get_content(times_url)
            output = json.loads(down_info)
            rawtimes = output.get('down_all', 0)
            if rawtimes:
                try:
                    times = int(rawtimes)
                except (TypeError, ValueError):
                    pass
        return times

    def parser(self):
        result = {}
        mapping = {
            u'资源大小': 'size',
            u'语言种类': 'language',
            u'应用分类': 'category',
            u'系统要求': 'env',
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

        times = self.download_times(self.url)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

#error 网站打不开
class MogustoreChannel(ChannelSpider):
    domain = "www.mogustore.cn"


class LeidianChannel(ChannelSpider):
    """
    url: http://game.leidian.com/detail/index/soft_id/12251
    下载次数：650万次 
    更新时间：2014-09-24
    大小：7.98MB
    版本：1.22
    系统：Android 1.6以上
    语言：英文
    分类：动作冒险
    作者：CandyMobile
    """
    seperator = u'：'
    domain = "www.leidian.com"
    times_xpath = "//div[@class='soft-extra-info']/span"
    fuzzy_xpath = "//div[@class='mod-base-info']/ul[@class='clearfix']/li"

    def download_times(self, result):
        times = None
        label = "download_times"
        translate = u"万"
        regx = re.compile('\d+')
        number_text = result.get(label, '')
        if number_text:
            match = regx.search(number_text)
            if match is not None:
                try:
                    times = int(match.group())
                except (TypeError, ValueError):
                    #log
                    pass
                else:
                    if translate in number_text:
                        times = times * 10000
        return times

    def get_size(self, url):
        size = None
        content = self.get_content(url)
        regx = re.compile("'size':'(?P<size>[\d\.]+MB)',")
        match = regx.search(content)
        if match is not None:
            size = match.group('size')
        return size

    def parser(self):
        result = {}
        mapping = {
            u'下载次数': 'download_times',
            u'更新时间': 'update_time',
            u'大小': 'size',
            u'版本': 'human_version',
            u'系统': 'env',
            u'语言': 'language',
            u'分类': 'category',
            u'作者': 'company',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        items2 = etree.xpath(self.times_xpath)
        items.extend(items2)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        #大小
        size = self.get_size(self.url)
        result['size'] = size
        #下载次数
        times = self.download_times(result)
        result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class Channel2265(ChannelSpider):
    """
    url: http://www.2265.com/game/android_16409.html
    下载：94次
    大小：2.9MB
    时间：2012-10-25
    类别：益智棋牌
    语言：中文
    系统：Android 1.5
    """
    seperator = u'：'
    domain = "www.2265.com"
    fuzzy_xpath = "//div[@class='detinfo']/div/p"
    version_xpath = "//div[@class='proinfo']/h1/span/text()"

    def download_times(self, dtimes):
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            rawtimes = match.group(0)
            try:
                times = int(rawtimes)
            except (TypeError, ValueError):
                times = 0
        return times

    def get_version(self, etree):
        version = None
        version_raw = etree.xpath(self.version_xpath)
        if version_raw:
            version = version_raw[0]
        return version

    def parser(self):
        result = {}
        mapping = {
            u'下载': 'download_times',
            u'大小': 'size',
            u'时间': 'update_time',
            u'类别': 'category',
            u'系统': 'env',
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

        result['human_version'] = self.get_version(etree)
        times = result.get('download_times', '')
        result['download_times'] = self.download_times(times)
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

class Sz1001Channel(ChannelSpider):
    """
    url: http://www.sz1001.net/soft/73650.htm
    软件大小: 21.30MB
    软件语言: 简体中文
    软件类别: apk - 休闲益智
    运行环境: Android
    授权方式: 特别版
    开 发 商: Home Page
    更新时间: 2014-9-15 15:39:38
    标签Tags: 银河忍者  
    """
    seperator = u':'
    domain = "www.sz1001.net"
    fuzzy_xpath = "//div[@id='down']/ul/li"

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'软件语言': 'language',
            u'软件类别': 'category',
            u'运行环境': 'env',
            u'授权方式': 'authorize',
            u'开发商': 'company',
            u'更新时间': 'update_time',
            u'标签Tags': 'tag',
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

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result


class XdownsChannel(ChannelSpider):
    """
    url: http://www.xdowns.com/soft/184/phone/Android/2014/Soft_118253.html
    软件授权：免费软件
    软件大小：10.71 MB
    软件语言：中文版
    更新时间：2014-3-10 13:52:03
    应用平台：安卓
    """
    seperator = u'：'
    domain = "www.xdowns.com"
    fuzzy_xpath = "//ul[@class='meta_list']/li"

    def parser(self):
        result = {}
        mapping = {
            u'软件授权': 'authorize',
            u'软件大小': 'size',
            u'软件语言': 'language',
            u'更新时间': 'update_time',
            u'应用平台': 'env',
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

        #times = self.download_times(etree)
        #result['download_times'] = times
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
        return result

if __name__ == '__main__':
    zhushou360 = ZhuShou360Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://zhushou.360.cn/detail/index/soft_id/95487?recrefer=SE_D_360',
        title=u'360浏览器'
    )
    #zhushou360.run()

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

    lenovo = LenovoChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.lenovomm.com/app/10560755.html',
        title=u'忍者砍僵尸'
    )
    #lenovo.run()

    m163 = M163Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://m.163.com/android/software/323s6t.html',
        title=u'忍者砍僵尸'
    )
    #m163.run()

    sj91 = Sj91Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://play.91.com/android/App/index-12599.html',
        title=u'水果忍者大战彩虹糖 Fruit Ninja vs Skittles'
    )
    #sj91.run()

    gao7 = Gao7Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://d.gao7.com/game/android-97872-20140328.html',
        title=u'疯狂的忍者(HD)'
    )
    #gao7.run()

    vapp51 = Vapp51Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.51vapp.com/market/apps/detail.vhtml?appPkg=com.halfbrick.fruitninja',
        title=u'水果忍者'
    )
    #vapp51.run()

    opera = OperaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://apps.opera.com/zh_cn/saasfet4744.html',
        title=u'忍者急襲'
    )
    #opera.run()

    appchina = AppChinaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.appchina.com/app/com.netease.rz',
        title=u'忍者必须死2'
    )
    #appchina.run()

    zhidian3g = Zhidian3gChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://app.zhidian3g.cn/appSoftware_download.shtml?id=2046',
        title=u'忍者刷刷刷'
    )
    #zhidian3g.run()

    paojiao = PaojiaoChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://kuang.paojiao.cn/danji/detail_1546.html',
        title=u'迷你忍者'
    )
    #paojiao.run()

    tompda = TompdaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://android.tompda.com/48127.html',
        title=u'水果忍者高清中文版 Fruit Ninja HD',
    )
    #tompda.run()

    borpor = BorporChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.borpor.com/enddisplay.php?gid=17041',
        title=u'魔界忍者-2',
    )
    #borpor.run()

    maopaoke = MaopaokeChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.maopaoke.com/open/app/2690',
        title=u'格斗之皇',
    )
    #maopaoke.run()

    baikce = BaikceChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.baikce.cn/app/67362.html',
        title=u'音乐',
    )
    #baikce.run()

    softonic = SoftonicChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://ninja-rush.softonic.cn/android',
        title=u'忍者突袭 1.21',
    )
    #softonic.run()

    a280 = A280Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.a280.com/soft/haidaodazhanrenzhehaohuaban.v2.1.0',
        title=u'海盗大战忍者豪华版 v2.1.0',
    )
    #a280.run()

    meizumi = MeizumiChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.meizumi.com/apk/2408.html',
        title=u'豆腐忍者',
    )
    #meizumi.run()

    cncrk = CncrkChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.cncrk.com/downinfo/65995.html',
        title=u'水果忍者中文版 v1.9.6 官方免费版',
    )
    #cncrk.run()

    appdh = AppdhChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.appdh.com/app/renzhetuxi-ninja-rush/',
        title=u'忍者突袭 – Ninja Rush',
    )
    #appdh.run()

    itopdog = ItopdogChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.itopdog.cn/az/fruitninja.html',
        title=u'水果忍者 v1.9.1 官方版',
    )
    #itopdog.run()

    leidian = LeidianChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://game.leidian.com/detail/index/soft_id/12251',
        title=u'跳跃忍者',
    )
    #leidian.run()

    c2265 = Channel2265(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.2265.com/game/android_16409.html',
        title=u'50忍者 V1.0.0',
    )
    #c2265.run()

    sz1001 = Sz1001Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.sz1001.net/soft/73650.htm',
        title=u'银河忍者 1.0.1 安卓内购破解版',
    )
    #sz1001.run()

    xdowns = XdownsChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.xdowns.com/soft/184/phone/Android/2014/Soft_118253.html',
        title=u'魔界忍者2洞穴版 1.3.5 安卓版',
    )
    #xdowns.run()
