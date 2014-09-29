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

    def download_times(self, title):
        from position import OyksoftPosition
        position = OyksoftPosition()
        times = position.download_times(title)
        return times

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'软件语言': 'language',
            u'授权类型': 'authorize',
            u'运行环境': 'env',
            u'软件类别': 'category',
            u'更新时间': 'update_time'
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        #down_link = etree.xpath(self.down_xpath)[0]
        #storage = self.download_app(down_link)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0][:-1].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
            else:
                label = mapping.get(label, '')
                if label:
                    result[label] = value
        return result


class GameDogChannel(ChannelSpider):
    """
    ***无下载次数***

    页面包含因子：
        更新时间：2014-08-22 12:31
        网游类别：角色
        网游大小：42.72MB
        语言：简体
        固件：2.1以上版本
        运营公司：上海三七玩网络科技有限公司
        查看更多版本
    评论
    """
    domain = "www.gamedog.cn"
    down_xpath = "//dd[@id='downs_box']/span[1]/a/@href"
    fuzzy_xpath = "//div[@class='info_m']/ul/li"
    label_xpath = "child::text()"
    value_xpath = "child::span[1]/text()|child::a/text()"
    title_xpath = "//h1[@class='s_title']/span/text()"

    def parser(self):
        result = {}
        mapping = {
            u'更新时间': 'update_time',
            u'网游类别': 'category',
            u'网游大小': 'size',
            u'语言': 'language',
            u'固件': 'env',
            u'运营公司': 'company'
        }
        seperator = u'安卓版'
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        #down_link = etree.xpath(self.down_xpath)[0]
        title = etree.xpath(self.title_xpath)[0]
        version = title.split(seperator)[-1]
        result['human_version'] = version
        #storage = self.download_app(down_link)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0][:-1].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
            else:
                label = mapping.get(label, '')
                if label:
                    result[label] = value
        return result


class Mm10086Channel(ChannelSpider):
    """
    ***无下载次数***

    开发者　：广州承兴营销管理有限公司
    所属类别：游戏 网络游戏
    更新时间：2014-08-14
    文件大小：91.76MB
    商品 I D ：300008279684
    系统支持：Android 2.3 及以上
    评论

    """
    domain = "mm.10086.cn"
    down_xpath = "//ul[@class='ml40 o-hidden']/li[@class='mt20']/a[2]/@href"
    version_xpath = "//span[@id='appversion']/text()"

    def parser(self):
        result = {}
        mapping = {
            u'开发者': 'company',
            u'所属类别': 'category',
            u'更新时间': 'update_time',
            u'文件大小': 'size',
            u'系统支持': 'env',
        }
        etree = self.send_request(self.url)
        version = etree.xpath(self.version_xpath)[0]
        result['human_version'] = version
        #down_link = etree.xpath(self.down_xpath)[0]
        #下载app
        #storage = self.download_app(down_link)
        return result


class Channel520Apk(ChannelSpider):
    """
    ***无下载次数***
    类别：动作游戏
    语言：简体中文
    版本：V2.6.9
    大小：22.01MB
    时间：2013-12-30
    要求：Android 2.1 以上
    标签：QQ部落下载QQ部落安卓版
    """
    domain = "www.520apk.com"
    down_xpath = "//a[@class='icon_downbd']/@href"
    fuzzy_xpath = "//div[@class='center']/span"
    lable_xpath = "child::text()"
    value_xpath = "child::i/text()"

    def parser(self):
        mapping = {
            u'类别': 'category',
            u'语言': 'language',
            u'大小': 'size',
            u'版本': 'human_version',
            u'时间': 'update_time',
            u'要求': 'env',
        }
        result = {}
        #stroage = None
        etree = self.send_request(self.url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
            else:
                label = mapping.get(label, '')
                if label:
                    result[label] = value

        version = result.get('human_version', '').strip().lower()
        if version.startswith('v'):
            version = version[1:]
            result['human_version'] = version

        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            down_link = down_link[0]
            #storage = self.download_app(down_link)
        return result


class Apk3Channel(ChannelSpider):
    """
    ***无下载次数***
    软件大小：4.44 MB
    推荐星级：4星级软件
    更新时间：2014-08-19
    软件类别：国产软件 / 系统管理
    软件语言：简体中文
    授权方式：免费版
   【相关软件】
        刷机精灵Android官方版 1.0.5
        刷机精灵 2.1.9
    """

    domain = "www.apk3.com"
    seperator = u"："
    down_xpath = "//ul[@class='downlistbox']/li/a/@href"  # Detail
    xpath = "//ul[@id='downinfobox']/li/text()"
    version_xpath = "//div[@class='downInfoTitle']/b/text()"

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'更新时间': 'update_time',
            u'软件类别': 'category',
            u'软件语言': 'language',
            u'授权方式': 'authorize'
        }
        download_times = 0
        etree = self.send_request(self.url)
        items = etree.xpath(self.xpath)

        version = etree.xpath(self.version_xpath)
        if version:
            version = version[0].strip()

        for item in items:
            if item.strip():
                label, value = item.split(self.seperator)
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        download_times = result.get('download_times', 0)
        result['download_times'] = int(download_times)
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(self.url, down_link[0])
            #storage = self.download_app(down_link)
        return result


class DownzaChannel(ChannelSpider):
    """
    软件大小：4.10MB
    下载次数：4099
    更新时间：2014-08-23
    授权方式：免费版
    语言：简体中文
    软件类别：Android
    """

    seperator = u"："
    domain = "www.downza.cn"
    version_regx = re.compile(r'\d+(?:(\.\d+))+')
    fuzzy_xpath = (
        "//div[@class='intro']/"
        "ul[@class='clearfix']/li/text()"
    )
    version_xpath = "//h1/text()"
    down_xpath = "//div[@class='down_view_down_list fl']/ul/li/a/@href"

    def get_version(self, etree):
        version = ''
        version_raw = etree.xpath(self.version_xpath)
        if version_raw:
            version_raw = version_raw[0].strip()
            match = self.version_regx.search(version_raw)
            if match is not None:
                version = match.group()
        return version

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'下载次数': 'download_times',
            u'更新时间': 'update_time',
            u'授权方式': 'authorize',
            u'语言': 'language',
            u'软件类别': 'category',
        }
        download_times = 0
        etree = self.send_request(self.url)
        version = self.get_version(etree)
        result['human_version'] = version

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item.strip():
                label, value = item.split(self.seperator)
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        download_times = result.get('download_times', 0)
        result['download_times'] = int(download_times)
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            #storage = self.download_app(down_link)
        return result


class AnZhiChannel(ChannelSpider):
    """
        软件分类：综合服务
        下载：1000万+
        时间：2014年08月23日
        大小：16M
        系统支持：Android 3.0及以上
        资费：免费
        作者：去哪儿网
    """

    seperator = u"："
    domain = "www.anzhi.com"
    down_xpath = "//div[@class='detail_down']/a/@onclick"
    version_xpath = "//span[@class='app_detail_version']/text()"
    fuzzy_xpath = "//ul[@id='detail_line_ul']/li"
    down_url = "http://www.anzhi.com/dl_app.php?s=%s&n=5"

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

    def parser(self):
        result = {}
        mapping = {
            u'软件分类': 'category',
            u'下载': 'download_times',
            u'时间': 'update_time',
            u'大小': 'size',
            u'系统支持': 'env',
            u'资费': 'authorize',
        }
        etree = self.send_request(self.url)
        #版本
        version = etree.xpath(self.version_xpath)
        if version:
            version = version[0]
            #(1.1.1)
            if version.startswith('('):
                version = version[1:-1]
                result['human_version'] = version
        #所有属性
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()

        #下载次数
        times = self.download_times(result)
        result['download_times'] = times
        #下载链接
        down_link = self.download_link(etree)
        if down_link:
            pass
            #storage = self.download_app(down_link)
        return result


class AngeeksChannel(ChannelSpider):
    """
    软件大小： 59.7MB
    更新时间：2014-07-09
    下载次数：2991
    """
    domain = "www.angeeks.com"
    down_xpath = "//div[@class='rgmainsrimg']/a/@href"
    seperator = u':'
    version_xpath = "//dl[@class='clear_div hr']/dd/span[@class='ko']/text()"
    fuzzy_xpath = "//div[@class='rgmainslx']/span/text()"
    label = u'下载次数'

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'更新时间': 'update_time',
            u'下载次数': 'download_times',
        }
        etree = self.send_request(self.url)

        version = etree.xpath(self.version_xpath)
        if version:
            version = version[0].split(self.seperator)[-1]
            result['human_version'] = version

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            #storage = self.download_app(down_link)
        return result


class JiQiMaoChannel(ChannelSpider):
    """
    下载次数：97340
    类型：角色
    资源：免费版
    更新时间：2013-11-21
    大小：未知
    系统：安卓android
    """
    down_xpath = "//div[@class='appmsg_titlemid']/table/tr[3]/td/a/@href"
    seperator = u"\uff1a"
    fuzzy_xpath = "//div[@class='appmsg_titlemid']/table/tr/td/span/text()"
    domain = "jiqimao.com"

    def parser(self):
        result = {}
        mapping = {
            u'下载次数': 'download_times',
            u'类型': 'category',
            u'资源': 'authorize',
            u'更新时间': 'update_time',
            u'大小': 'size',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            #storage = self.download_app(down_link, session=self.session)
        return result


class SjapkChannel(ChannelSpider):
    """
    资费类型：完全免费
    语言：中文
    最低系统：2.3.3
    版本：1.0
    """
    domain = "www.sjapk.com"
    down_xpath = "//div[@class='main_r_xiazai5']/a/@href"
    fuzzy_xpath = "//div[@class='main_r_f']/p"

    def parser(self):
        result = {}
        mapping = {
            u'资费类型': 'authorize',
            u'语言': 'language',
            u'最低系统': 'env',
            u'版本': 'human_version',
        }
        seperator = u'：'
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            values = item.text_content().strip().split(' ')
            values = [v for v in values if bool(v)]
            for vl in values:
                lv = vl.split(seperator)
                if len(lv) == 2:
                    label = lv[0].strip()
                    label = mapping.get(label, '')
                    if label:
                        result[label] = lv[1].strip()

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(self.url, down_link[0])
            #storage = self.download_app(down_link, session=self.session)
        return result


class CoolApkChannel(ChannelSpider):
    """
     52人关注，6万+次下载，300个评论，1
     3个权限，简体中文，127.00 M，
     支持2.2及更高版本，3天前更新
    """
    domain = "www.coolapk.com"
    fuzzy_xpath = (
        "//div[@class='hidden-md hidden-lg"
        " ex-page-infobar']/div/a/span"
    )
    down_xpath = (
        "//div[@class='ex-page-header']"
        "/following::script[1]/text()"
    )
    label_xpath = "child::text()"
    value_xpath = "child::strong/text()"
    version_xpath = (
        "/h1[@class='media-heading"
        " ex-apk-view-title']/small/text()"
    )

    def get_version(self, etree):
        version = None
        version_raw = etree.xpath(self.version_xpath)
        if version_raw:
            version = version_raw[0]
        return version

    def download_link(self, etree):

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

    def download_times(self, result):
        times = None
        label = u"下载"
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

    def parser(self):
        result = {}
        mapping = {
            u'下载': 'download_times',
            u'权限': 'authorize',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            value = item.xpath(self.value_xpath)[0].strip()
            label = item.xpath(self.label_xpath)[0].strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value

        times = self.download_times(result)
        result['download_times'] = times

        down_link = self.download_link(etree)
        if down_link:
            pass
            #storage = self.download_app(down_link, session=self.session)
        return result


class CrossmoChannel(ChannelSpider):
    """
    开 发 商：源结科技
    软件类别： 生活助手
    更新时间：2014-08-20
    推荐指数：
    版　　本：2.0.0
    下载次数：189
    价　　格：免费
    """
    domain = "www.crossmo.com"
    fuzzy_xpath = "//div[@class='aniu']/dl/dt/text()"
    head_xpath = "//head"
    seperator = u'：'

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

    def download_link(self, appkey, appid):
        check_app = (
            "http://soft.crossmo.com/softdown_topc_v5.php?"
            "crossmo=%s&downloadtype=checkapks&appid=%s"
        ) % (appkey, appid)
        down_app = (
            "http://soft.crossmo.com/softdown_topc_v5.php?"
            "crossmo=%s&downloadtype=local&appid=%s"
        ) % (appkey, appid)
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.url
        }
        self.update_request_headers(headers)
        self.send_request(url=check_app, tree=False)
        return down_app

    def parser(self):
        result = {}
        mapping = {
            u'开 发 商': 'company',
            u'软件类别': 'category',
            u'更新时间': 'update_time',
            u'版　　本': 'human_version',
            u'下载次数': 'download_times',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()
        try:
            times = int(result.get('download_times', 0))
        except (TypeError, ValueError):
            times = 0
        result['download_times'] = times
        appkey = self.get_appkey(etree)
        appid = self.get_appid(self.url)
        down_link = self.download_link(appkey, appid)
        if down_link:
            pass
            #storage = self.download_app(
            #    down_link,
            #    session=self.session
            #)
        return result


class ShoujiBaiduChannel(ChannelSpider):
    """
    大小: 8.3MB
    版本: 1.11
    下载次数: 50万
    """

    domain = "shouji.baidu.com"
    seperator = u':'
    fuzzy_xpath = "//div[@class='detail']/span/text()"
    down_xpath = "//div[@class='area-download']/a[@class='apk']/@href"
    down_label = u"下载次数"
    version_label = u'版本'

    def download_times(self, result):
        times = None
        translate = u"万"
        regx = re.compile('\d+')
        number_text = result.get(self.down_label, '')
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

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'大小': 'size',
            u'版本': 'human_version',
            u'下载次数': 'download_times',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()

        times = self.download_times(result)
        result['download_times'] = times
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return result


class Channel7xz(ChannelSpider):
    """
    无下载次数
    大小：1.17MB
    格式：apk
    更新日期：2012-09-25 13:25:52
    适用于：Android 1.6及以上
    专题： 赛车飞行 EA
    """
    domain = "www.7xz.com"
    seperator = u'：'
    fuzzy_xpath = "//ul[@class='values_one']/li"
    version_regx = re.compile(r'\d+(?:(\.\d+))+')
    down_xpath = "//div[@class='diannao']/a[@class='d_pc_normal_dn']/@href"
    version_xpath = "//div[@class='title']/span[@class='left']/strong/text()"

    def get_version(self, etree):
        version = ''
        version_raw = etree.xpath(self.version_xpath)
        if version_raw:
            version_raw = version_raw[0].strip()
            match = self.version_regx.search(version_raw)
            if match is not None:
                version = match.group()
        return version

    def parser(self):
        result = {}
        mapping = {
            u'大小': 'size',
            u'更新日期': 'update_time',
            u'适用于': 'env',
        }
        storage = None
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
        version = self.get_version(etree)
        result['human_version'] = version
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return result


class PC6Channel(ChannelSpider):
    """
    无下载次数
    售价：免费
    类别：飞行射击
    更新：2014/8/25
    系统支持：安卓, 2.2以上
    版本：v6.0.1官网版
    大小：47M
    """
    domain = "www.pc6.com"
    seperator = u'：'
    fuzzy_xpath = "//div[@class='left3']/div"
    down_xpath = "//div[@class='left2']/a[@class='wdj']/@href"

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'类别': 'category',
            u'更新': 'update_time',
            u'系统支持': 'env',
            u'版本': 'human_version',
            u'大小': 'size',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split('\n')
            for elem in elems:
                label, value = elem.split(self.seperator)
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return result


class Channel3533(ChannelSpider):
    """
    >>>p3533 = Position3533()
    >>>p3533.run(u'功夫西游')
    """
    domain = "www.3533.com"
    seperator = u'：'
    down_xpath = "//div[@class='andorid']/dl/dt/a/@href"
    base_xpath = "//div[@class='appdownbox']/dl[@class='packbox']"
    andorid_xpath = "child::dt/a/img/@alt"
    andorid_token = u'安卓版下载'
    fuzzy_xpath = (
        "child::dd/div/div[@class='packclear']/"
        "div[@class='packright']/div/p/span"
    )

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'版本': 'human_version',
            u'大小': 'size',
            u'系统要求': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.base_xpath)
        andorid_dom = None
        for item in items:
            andorid = item.xpath(self.andorid_xpath)
            if andorid:
                andorid = andorid[0]
                if self.andorid_token in andorid:
                    andorid_dom = item
                    break

        if andorid_dom:
            items = andorid_dom.xpath(self.fuzzy_xpath)
            for item in items:
                span = item.xpath("child::span/text()")
                if span:
                    content = span[0]
                else:
                    content = item.text_content().strip()
                label, value = content.split(self.seperator)
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        print result
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return result


class Apk8Channel(ChannelSpider):
    """
    游戏版本：2.0.0
    游戏类型：卡牌手游游戏
    适用固件：安卓1.5以上
    游戏语言：中文
    文件大小：128M
    游戏提供：已通过手机安全软件检测
    更新时间：2014-08-25 18:59:33
    游戏标签：

    所属专题：手机卡牌游戏  动作卡牌类安卓网游

    """
    domain = "www.apk8.com"
    times_xpath = "//span[@id='downNum']/text()"
    seperator = u'：'
    down_xpath = "//div[@class='downnew']/a[@class='bt_bd']/@href"
    fuzzy_xpath = "//div[@class='detailsleft']/ol[@class='feileis']/li"

    def download_times(self, etree):
        times = 0
        try:
            times = int(etree.xpath(self.times_xpath)[0])
        except (TypeError, ValueError, IndexError):
            times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'游戏版本': 'human_version',
            u'游戏类型': 'category',
            u'适用固件': 'env',
            u'游戏语言': 'language',
            u'文件大小': 'size',
            u'更新时间': 'update_time',
        }
        storage = None
        etree = self.send_request(self.url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split('\n')
            for elem in elems:
                label, value = elem.split(self.seperator)
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        times = self.download_times(etree)
        result['download_times'] = times
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return result


class XiaZaiZhiJiaChannel(ChannelSpider):
    """
     微信 V5.3.1.51 for Android安卓版
     软件大小：25.12 MB
     下载次数：6454次
     所属类型：聊天社交
     更新时间：2014-07-21
    """

    seperator = u'：'
    charset = 'gb2312'
    domain = "www.xiazaizhijia.com"
    fuzzy_xpath = "//div[@class='AMI_desc']/div[@class='clearfix']/dl"
    version_regx = re.compile(r'\d+(?:(\.\d+))+')
    down_label = '下载次数'
    version_xpath = "//h1/a/text()"
    down_xpath = "//a[@class='AMIC_downStylea']/@href"

    def get_version(self, etree):
        version = ''
        version_raw = etree.xpath(self.version_xpath)
        if version_raw:
            version_raw = version_raw[0].strip()
            match = self.version_regx.search(version_raw)
            if match is not None:
                version = match.group()
        return version

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'软件大小': 'size',
            u'下载次数': 'download_times',
            u'所属类型': 'category',
            u'更新时间': 'update_time',
        }

        self.send_request(self.url, tree=False)
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.url
        }
        self.update_request_headers(headers)
        etree = self.send_request('%s?' % self.url, ignore=True)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            title = item.xpath("child::dt/text()")[0][0:-1]
            script_dom = item.xpath("child::dd/script/@src")
            if script_dom:
                query = script_dom[0]
                parse = urlparse.parse_qs(query)
                value = parse.get('aid', 0)
                if value:
                    try:
                        value = int(value[0])
                    except (TypeError, ValueError):
                        value = 0
            else:
                item_dom = item.xpath("child::dd")[0]
                value_raw = item_dom.text_content().strip()
                if value_raw:
                    value = value_raw
            label = title.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()
        version = self.get_version(etree)
        result['human_version'] = version

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return result


class CngbaChannel(ChannelSpider):
    """
    游戏原名：名将决
    所属分类： 游戏
    大小：KB
    界面语言：简体中文
    开发厂商：
    更新时间：2012-11-19
    """
    seperator = u'：'
    domain = "www.cngba.com"
    fuzzy_xpath = "//div[@class='page_Ftxt']/em/text()"

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'所属分类': 'category',
            u'大小': 'size',
            u'界面语言': 'language',
            u'开发厂商': 'company',
            u'更新时间': 'update_time',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            item = item.strip()
            if item:
                label, value = item.split(self.seperator)
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
        return result


class SjwyxChannel(ChannelSpider):
    """
    T
    游戏大小：82.43M
    文件格式：APK
    更新时间：2014-8-4 14:21:33
    """
    domain = "www.sjwyx.com"
    seperator = u'：'
    charset = 'gb2312'
    fuzzy_list_xpath = "//ul[@id='d_l']/li"
    accurate_token = u'Android通用版'
    title_xpath = "child::div[@class='l']/h3/text()"
    fuzzy_xpath = "child::div[@class='l']/p"

    def parser(self):
        result = {}
        down_link = ''
        mapping = {
            u'游戏大小': 'size',
            u'更新时间': 'update_time',
        }
        storage = None
        etree = self.send_request(self.url, ignore=True)
        lists = etree.xpath(self.fuzzy_list_xpath)
        for elem in lists:
            title = elem.xpath(self.title_xpath)[0].strip()
            if title == self.accurate_token:
                items = elem.xpath(self.fuzzy_xpath)
                for item in items:
                    downbtn = item.xpath("child::a[@class='downbtn']/@href")
                    if downbtn:
                        down_link = downbtn[0]
                    else:
                        content = item.text_content().strip()
                        label, value = content.split(self.seperator)
                        label = label.strip()
                        label = mapping.get(label, '')
                        if label:
                            result[label] = value.strip()
        #times = self.download_times():
        if down_link:
            storage = self.download_app(down_link)
        return result


class Ruan8Channel(ChannelSpider):
    """
    版本：1.0
    软件语言：简体中文
    软件资费：免费软件
    适用固件：Android2.2+
    更新时间：2014-08-26
    软件大小：5.7M
    下载次数：68
    """
    domain = "soft.anruan.com"
    fuzzy_xpath = "//div[@class='app_info']/ul/li"
    seperator = u"："
    down_label = u'下载次数'
    down_xpath = "child::a/@href"
    version_label = u'版本'

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'版本': 'human_version',
            u'软件语言': 'language',
            u'软件资费': 'authorize',
            u'适用固件': 'env',
            u'更新时间': 'update_time',
            u'软件大小': 'size',
            u'下载次数': 'download_times',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        down_link = None
        for item in items:
            cls = item.attrib.get('class', '')
            if cls == 'app_green':
                content_raw = item.xpath("child::span/text()")
                if content_raw:
                    content = content_raw[0]
            elif cls == 'app_down':
                down_link = item.xpath(self.down_xpath)
            else:
                content = item.text_content().strip()
            if content:
                elems = content.split(self.seperator)
                if len(elems) == 2:
                    label, value = elems
                    label = label.strip()
                    label = mapping.get(label, '')
                    if label:
                        result[label] = value.strip()

        times = int(result.get('donwload_times', 0))
        result['download_times'] = times

        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return result


class PcHomeChannel(ChannelSpider):
    """
    Android 5.3.1.67 1161 533
    更新时间：2014-07-16
    软件大小：25.12MB
    软件分类：即时通讯
    开发商：腾讯微信
    软件性质：[免费软件]
    支持系统：Android
    """

    domain = "www.pchome.com"
    seperator = u"："
    fuzzy_xpath = "//div[@class='dl-info-con']/ul/li"
    down_xpath = "//div[@class='dl-download-links mg-btm20']/dl/dd/a/@onclick"

    def download_times(self):
        from poistion import PcHomePosition
        pchome = PcHomePosition()
        times = pchome.download_times()
        return times

    def download_link(self, etree):
        down_link = None
        down_label = '下载地址'
        regx = re.compile(".+\('(?P<link>.+)'\).+")
        xpath = "//ul[@class='dl-tab-6 clearfix']/li/a"
        links = etree.xpath(xpath)
        for link in links:
            text = link.text().strip()
            if text == down_label:
                etree = self.send_request(self.url)
                items = etree.xpath(self.down_xpath)
                if items:
                    item = items[0]
                    match = regx.search(item)
                    if match is not None:
                        down_link = match.group('link')
        return down_link

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'更新时间': 'update_time',
            u'软件大小': 'size',
            u'软件分类': 'category',
            u'开发商': 'comapny',
            u'软件性质': 'authorize',
            u'支持系统': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()
        times = self.download_times()
        result['download_times'] = times
        down_link = self.download_link(etree)
        if down_link:
            storage = self.download_app(down_link)
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
    seperator = u"："
    version_xpath = "//span[@class='version']/text()"
    times_xpath = "//div[@class='levelCount']/span[@class='count']/text()"
    size_xpath = "//div[@class='size row']/text()"
    env_xpath = "//div[@class='adapt row popup']/h4/text()"
    update_time_xpath = "//div[@class='updateTime row']/em/text()"
    author_xpath = "//div[@class='author row']/span/a/text()"
    down_xpath = "//a[@id='BDTJDownload']/@href"
    label = u'下载次数'

    def download_times(self, etree):
        down_times = 0
        regx = re.compile(',')
        dregx = re.compile('(?P<times>\d+)')
        raw_string = etree.xpath(self.times_xpath)
        if raw_string:
            raw_string = raw_string[0]
            raw_string = regx.sub('', raw_string)
            match = dregx.search(raw_string)
            if match is not None:
                try:
                    down_times = int(match.group('times'))
                except:
                    pass
        return down_times

    def parser(self):
        result = {}
        etree = self.send_request(self.url)
        times = self.download_times(etree)
        result['download_times'] = times
        sizeraw = etree.xpath(self.size_xpath)
        if sizeraw:
            size = sizeraw[0].strip()
            size = size.split(self.seperator)[-1]
            result['size'] = size

        envraw = etree.xpath(self.env_xpath)
        if envraw:
            env = envraw[0]
            env = env.split(self.seperator)[-1]
            result['env'] = env

        author = etree.xpath(self.author_xpath)
        if author:
            company = author[0]
            result['company'] = company

        update_time_raw = etree.xpath(self.update_time_xpath)
        if update_time_raw:
            update_time = update_time_raw[0]
            result['update_time'] = update_time

        version_raw = etree.xpath(self.version_xpath)
        if version_raw:
            version = version_raw[0].strip()
            if version.startswith('('):
                version = version[1:-1]
            result['human_version'] = version
        return result


class DChannel(ChannelSpider):
    """
    url: http://android.d.cn/software/12486.html
    类别 阅读工具
    下载 128.72万次
    版本 4.6.1.680
    时间 2014-07-24
    大小 7.32MB
    星级
    资费 完全免费
    热度 65℃
    支持系统 1.6以上
    开发商 Tencent Technology
    语言英文, 中文
    """
    domain = "www.d.cn"
    fuzzy_xpath = "//ul[@class='de-game-info clearfix']/li"
    label_xpath = "child::span/text()"
    value_xpath = "child::text()"

    def download_times(self, rawstring):
        times = 0
        dot = '.'
        regx = re.compile('(?P<times>[\d\.]+)')
        match = regx.search(rawstring)
        if match is not None:
            raw_times = match.group('times')
            if dot in raw_times:
                times = int(float(raw_times) * 10000)
            else:
                times = int(raw_times)
        return times

    def parser(self):
        result = {}
        etree = self.send_request(self.url, ignore=True)
        mapping = {
            u'类别': 'category',
            u'下载': 'download_times',
            u'版本': 'human_version',
            u'大小': 'size',
            u'时间': 'update_time',
            u'开发商': 'company',
            u'支持系统': 'env',
            u'语言': 'language',
            u'资费': 'authorize',
        }
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            value = ''
            label = item.xpath(self.label_xpath)[0].strip()
            label = mapping.get(label, '')
            if label:
                vraw = item.xpath(self.value_xpath)
                if vraw:
                    value = ''.join(vraw).strip()
                result[label] = value

        dtimes = result.get('download_times', '')
        if dtimes:
            times = self.download_times(dtimes)
            result['download_times'] = times
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
    fuzzy_xpath = "//div[@class='app_boxcon']/table/tr/td"
    info_xpath = "child::text()|child::*/text()"
    down_xpath = "//a[@id='content_mobile_href']/@href"
    seperator = u'：'
    label = u'下载次数'

    def download_times(self, dtimes):
        times = 0
        try:
            times = int(dtimes[:-1])
        except (TypeError, ValueError):
            pass
        return times

    def parser(self):
        result = {}
        storage = None
        mapping = {
            u'下载次数': 'download_times',
            u'大小': 'size',
            u'更新时间': 'update_time',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                value = value.strip()
                result[label] = value
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            storage = self.download_app(down_link)
        return result


class WandoujiaChannel(ChannelSpider):
    """
    url: http://www.wandoujia.com/apps/com.netease.newsreader.activity
    大小 18.62M
    分类 新闻资讯 新闻 精品 网易 世界杯
    更新 8月26日
    版本 4.0.1
    要求 Android 2.3 以上
    网站 网之易信息技术（北京）有限公司
    来自 官方提供
    """

    domain = "www.wandoujia.com"
    label_xpath = "//div[@class='infos']/dl[@class='infos-list']/dt/text()"
    value_xpath = "//div[@class='infos']/dl[@class='infos-list']/dd"
    times_xpath = "//div[@class='num-list']/span[@class='item']/i/text()"
    down_xpath = "//div[@class='download-wp']/a[@class='install-btn']/@href"

    def download_times(self, etree):
        times = 0
        token = u'万'
        raw_times = etree.xpath(self.times_xpath)
        if raw_times:
            raw_times = raw_times[0].strip()
            if token in raw_times:
                raw_times = raw_times[:-1].strip()
                try:
                    times = int(raw_times) * 10000
                except (TypeError, ValueError):
                    pass
            else:
                try:
                    times = int(raw_times)
                except (TypeError, ValueError):
                    pass
        return times

    def parser(self):
        result = {}
        stroage = None
        env_token = "perms"
        mapping = {
            u'大小': 'size',
            u'分类': 'category',
            u'更新': 'update_time',
            u'版本': 'human_version',
            u'要求': 'env',
            u'网站': 'company',
        }
        etree = self.send_request(self.url)
        labels = etree.xpath(self.label_xpath)
        value_dom = etree.xpath(self.value_xpath)
        labels = [item.strip() for item in labels]
        values = []
        for v in value_dom:
            if v.attrib.get('class', '') == env_token:
                value = v.text.strip().split(' ')
            else:
                value = v.text_content().strip().split(' ')
            value = [va.strip() for va in value if va]
            value = ' '.join(value)
            values.append(value)
        items = zip(labels, values)
        for item in items:
            label, value = item
            label = mapping.get(label, '')
            if label:
                result[label] = value
        times = self.download_times(etree)
        result['download_times'] = times
        #down_link = etree.xpath(self.down_xpath)[0]
        #if down_link:
        #    storage = self.download_app(down_link)
        return result


class AnzowChannel(ChannelSpider):
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

    domain = "www.anzow.com"
    fuzzy_xpath = "//dl[@class='down_info clear']/dd/dl/dt/ul/li"
    info_xpath = "child::text()|child::*/text()|child::*/*/text()"
    down_xpath = "//div[@class='contentdbtn']/a[@class='commentbtn']/@href"
    seperator = u'：'

    def parser(self):
        result = {}
        stroage = None
        mapping = {
            u'所属分类': 'category',
            u'授权方式': 'authorize',
            u'软件大小': 'size',
            u'应用版本': 'human_version',
            u'软件语言': 'language',
            u'适用平台': 'env',
            u'更新时间': 'update_time',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                result[label] = value.strip()
        #down_link = etree.xpath(self.down_xpath)[0]
        #if down_link:
        #    storage = self.download_app(down_link)
        return result


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
    down_xpath = "//a[@class='link_btn']/@href"
    seperator = u'：'

    def download_times(self, dtimes):
        times = 0
        token1 = u'万'
        token2 = u'千万'
        regx = re.compile('(?P<times>[\d\.]+)')
        match = regx.search(dtimes)
        if match is not None:
            try:
                raw_times = float(match.group('times'))
            except (TypeError, ValueError):
                pass
            else:
                if token2 in dtimes:
                    times = int(raw_times * 10000)
                elif token1 in dtimes:
                    times = int(raw_times * 10000000)
                else:
                    times = 1000
        return times

    def parser(self):
        result = {}
        stroage = None
        etree = self.send_request(self.url, ignore=True)
        mapping = {
            u'作者': 'company',
            u'大小': 'size',
            u'类别': 'category',
            u'热度': 'download_times',
            u'语言': 'language',
            u'固件': 'env',
            u'上架时间': 'update_time',
        }
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label = elems[0].strip()
                value = elems[1].strip()
                label = mapping.get(label, '')
                result[label] = value.strip()
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(self.url, down_link[0])
            storage = self.download_app(down_link)
        return result 



if __name__ == '__main__':
    #url = "http://www.oyksoft.com/soft/32456.html"
    #oyk = OykSoftChannel()
    #print oyk.run(url)

    #url = "http://android.gamedog.cn/online/233523.html"
    hiapk = HiapkChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://apk.hiapk.com/appinfo/com.mobi.screensaver.fzlxqx2',
        title=u'水果忍者安卓版v1.9.5'
    
    )
    hiapk.run()

    wandoujia = WandoujiaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.wandoujia.com/apps/com.halfbrick.fruitninja',
        title=u'水果忍者安卓版v1.9.5'
    )
    #wandoujia.run()

    gamedog = GameDogChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://android.gamedog.cn/game/386653.html',
        title=u'水果忍者安卓版v1.9.5'
    )
    #gamedog.run()

    #url = "http://mm.10086.cn/android/info/300008279684.html?from=www&stag=cT0lRTglQTElOTclRTUlQTQlQjQlRTglQjYlQjMlRTclOTAlODMmcD0xJnQ9JUU1JTg1JUE4JUU5JTgzJUE4JnNuPTEmYWN0aXZlPTE%3D"
    #mm10086 = Mm10086Channel()
    #mm10086.run(url)

    #url = "http://www.520apk.com/android/dongzuoyouxi/100012517.html"
    #c520 = Channel520Apk()
    #c520.run(url)

    #url = "http://www.apk3.com/soft/4393.html"
    #apk3 = Apk3Channel()
    #apk3.run(url)

    #url = "http://www.anzhi.com/soft_1322730.html"
    #anzhi = AnZhiChannel()
    #anzhi.run(url)

    #url = "http://www.downza.cn/soft/22271.html"
    #downza = DownzaChannel()
    #downza.run(url)

    #url = "http://www.coolapk.com/game/sh.lilith.dgame.uc"
    #ca = CoolApkChannel()
    #ca.run(url)

    #url = "http://www.sjapk.com/36195.Html"
    #js = SjapkChannel()
    #print js.run(url)

    #url = "http://jiqimao.com/game-199571/"
    #jiqimao = JiQiMaoChannel()
    #jiqimao.run(url)

    #url = "http://soft.crossmo.com/softinfo_13185.html"
    #cs = CrossmoChannel()
    #cs.run(url)

    #url = "http://shouji.baidu.com/soft/item?docid=6865605&from=&f=search_app_%E6%9F%9A%E5%AD%90%E7%9B%B8%E6%9C%BA%40list_1_title%401%40header_software_input_btn_search"
    #shouji = ShoujiBaiduChannel()
    #shouji.run(url)

    #url = "http://www.7xz.com/games/view/10020683"
    #c7xz = Channel7xz()
    #c7xz.run(url)

    #url = "http://www.pc6.com/azyx/82254.html"
    #pc6 = PC6Channel()
    #pc6.run(url)

    #url = "http://www.apk8.com/game/game_14104.html"
    #apk8 = Apk8Channel()
    #apk8.run(url)

    #url = "http://www.xiazaizhijia.com/shouji/6570.html"
    #xiazai = XiaZaiZhiJiaChannel()
    #xiazai.run(url)

    #url = "http://shijie.sjwyx.com/down/"
    #sjwyx = SjwyxChannel()
    #sjwyx.run(url)

    #url = "http://soft.anruan.com/7295/"
    #ruan8 = Ruan8Channel()
    #ruan8.run(url)
    p3533 = Channel3533(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://game.3533.com/game/49703/',
        title=u'水果忍者安卓版v1.9.5'
    )
    #p3533.run()
    nduoa = NduoaChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url='http://www.nduoa.com/apk/detail/634370',
        title=u'工行短信银行'
    )
    #print nduoa.run()
    dchannel = DChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://android.d.cn/software/12486.html",
        title=u'工行短信银行'
    )
    #dchannel.run()
    liqucn = LiqucnChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://os-android.liqucn.com/yx/15024.shtml",
        title=u'工行短信银行'
    )
    #liqucn.run()
