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

    seperator = u'：'
    domain = "www.oyksoft.com"
    down_xpath = "//a[@class='normal']/@href"
    fuzzy_xpath = "//div[@id='softinfo']/ul/li"

    def download_times(self):
        from position import OyksoftPosition
        position = OyksoftPosition(
            self.title,
            has_orm=False,
        )
        times = position.download_times()
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
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value
        times = self.download_times()
        result['download_times'] = times
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
    开发者　：广州承兴营销管理有限公司
    所属类别：游戏 网络游戏
    更新时间：2014-08-14
    文件大小：91.76MB
    商品 I D ：300008279684
    系统支持：Android 2.3 及以上
    评论

    """
    domain = "mm.10086.cn"
    seperator = u'：'
    down_xpath = "//ul[@class='ml40 o-hidden']/li[@class='mt20']/a[2]/@href"
    fuzzy_xpath = "//div[@class='mj_info font-f-yh']/ul/li"

    def download_times(self, dom):
        lower = u'<'
        times = base = 10000
        content = dom.text_content().strip()
        regx = re.compile('\d+')
        match = regx.search(content)
        if match is not None:
            rawtimes = match.group(0)
            if content.startswith(lower):
                times = base
            else:
                try:
                    times = int(rawtimes) * base
                except (TypeError, ValueError):
                    pass
        return times

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'开发者': 'company',
            u'所属类别': 'category',
            u'更新时间': 'update_time',
            u'文件大小': 'size',
            u'系统支持': 'env',
            u'版　　本': 'human_version',
            u'大　　小': 'size',
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
        times = self.download_times(items[0])
        result['download_times'] = times
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
    seperator = u'：'
    domain = "www.520apk.com"
    down_xpath = "//a[@class='icon_downbd']/@href"
    fuzzy_xpath = "//div[@class='center']/span"

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

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
        version = result.get('human_version', '').strip().lower()
        if version.startswith('v'):
            version = version[1:]
            result['human_version'] = version
        print result
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

    seperator = u"："
    domain = "www.apk3.com"
    down_xpath = "//ul[@class='downlistbox']/li/a/@href"  # Detail
    xpath = "//ul[@id='downinfobox']/li/text()"
    version_xpath = "//div[@class='downInfoTitle']/b/text()"

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(self.url, down_link[0])
            storage = self.download_app(down_link)
        return storage

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

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

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
                elems = item.split(self.seperator)
                if len(elems) == 2:
                    label, value = elems
                    label = label.strip()
                    label = mapping.get(label, '')
                    if label:
                        result[label] = value.strip()
        download_times = result.get('download_times', 0)
        result['download_times'] = int(download_times)
        print result
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
        storage = None
        down_link = ''
        down_text = etree.xpath(self.down_xpath)
        if down_text:
            down_text = down_text[0]
            regx = re.compile('opendown\((?P<pk>\d+)\).+')
            match = regx.match(down_text)
            if match is not None:
                pk = match.group('pk')
                down_link = self.down_url % pk
        if down_link:
            storage = self.download_app(down_link)
        return storage

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
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()

        #下载次数
        times = self.download_times(result)
        result['download_times'] = times
        print result
        return result


class AngeeksChannel(ChannelSpider):
    """
    软件大小： 59.7MB
    更新时间：2014-07-09
    下载次数：2991
    """
    domain = "www.angeeks.com"
    down_xpath = "//div[@class='rgmainsrimg']/a/@href"
    seperator = u'：'
    version_xpath = "//dl[@class='clear_div hr']/dd/span[@class='ko']/text()"
    fuzzy_xpath = "//div[@class='rgmainslx']/span/text()"

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

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
            content = item.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        times = result.get('download_times', '')
        result['download_times'] = self.download_times(times)
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
    #seperator = u"\uff1a"
    seperator = u"："
    fuzzy_xpath = "//div[@class='appmsg_titlemid']/table/tr/td/span/text()"
    domain = "jiqimao.com"

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'下载次数': 'download_times',
            u'类型': 'category',
            u'资源': 'authorize',
            u'更新时间': 'update_time',
            u'大小': 'size',
            u'系统': 'env',
        }

        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = label.strip()
                label = mapping.get(label, '')
                if label:
                    result[label] = value.strip()
        times = result.get('download_times', '')
        result['download_times'] = self.download_times(times)
        print result
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

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(self.url, down_link[0])
            storage = self.download_app(down_link, session=self.session)
        return storage

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
        if down_link:
            storage = self.download_app(down_link, session=self.session)
        return storage

    def download_times(self, dtimes):
        times = 0
        translate = u"万"
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            try:
                times = int(match.group())
            except (TypeError, ValueError):
                #log
                pass
            else:
                if translate in dtimes:
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

        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        print result
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
    fuzzy_xpath = (
        "//div[@class='aniu']/dl/dt/text()"
        "|//div[@class='aniu']/dl/dd/text()"
    )
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

    def download_link(self, etree):
        appkey = self.get_appkey(etree)
        appid = self.get_appid(self.url)
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
        storage = self.download_app(
            down_app,
            session=self.session
        )
        return storage

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

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
        print result
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

    def download_times(self, dtimes):
        times = None
        translate = u"万"
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            try:
                times = int(match.group())
            except (TypeError, ValueError):
                #log
                pass
            else:
                if translate in dtimes:
                    times = times * 10000
        return times

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return storage

    def parser(self):
        result = {}
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
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
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

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'大小': 'size',
            u'更新日期': 'update_time',
            u'适用于': 'env',
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
        version = self.get_version(etree)
        result['human_version'] = version
        print result
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

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return storage

    def parser(self):
        result = {}
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
        return result


class Channel3533(ChannelSpider):
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

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
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

    def set_header(self, url):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': url
        }
        self.update_request_headers(headers)

    def flush_header(self, fields=None):
        if fields:
            for field in fields:
                del self.session.headers[field]

    def download_times(self, etree):
        times = 0
        game = '/game/'
        soft = '/soft/'
        regx = re.compile('\d+')
        source = self.url.rsplit('/', 1)[-1]
        match = regx.search(source)
        if match:
            pid = match.group(0)
            if game in self.url:
                url = "http://www.apk8.com/getpl.php"
                data = {
                    'act': 'down',
                    'game_id': pid
                }
            elif soft in self.url:
                url = "http://www.apk8.com/getSoft.php"
                data = {
                    'act': 'down',
                    'soft_id': pid
                }
            self.set_header(self.url)
            content = self.send_request(data=data, url=url, tree=False)
            self.flush_header(('X-Requested-With',))
            if content:
                content = content.strip()
                try:
                    times = int(content)
                except (TypeError, ValueError):
                    pass
        return times

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'游戏版本': 'human_version',
            u'游戏类型': 'category',
            u'适用固件': 'env',
            u'游戏语言': 'language',
            u'文件大小': 'size',
            u'更新时间': 'update_time',
            u'软件版本': 'human_version',
            u'软件类型': 'category',
            u'软件提供': 'company',
            u'软件语言': 'language',
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

        times = self.download_times(etree)
        result['download_times'] = times
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

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
        return storage

    def parser(self):
        result = {}
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
                result[label] = value
        version = self.get_version(etree)
        result['human_version'] = version
        return result


class AnRuanChannel(ChannelSpider):
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
    down_xpath = "child::a/@href"
    version_label = u'版本'

    def download_link(self, etree):
        down_link = None
        storage = None
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def parser(self):
        result = {}
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
        times = self.download_times(result.get('download_times', 0))
        result['download_times'] = times
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

    domain = "www.pchome.net"
    seperator = u"："
    fuzzy_xpath = "//div[@class='dl-info-con']/ul/li"
    down_xpath = "//div[@class='dl-download-links mg-btm20']/dl/dd/a/@onclick"

    def download_times(self):
        from position import PcHomePosition
        pchome = PcHomePosition(
            self.title,
            has_orm=False,
        )
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
        #storage = None
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
        #down_link = self.download_link(etree)
        #if down_link:
            #storage = self.download_app(down_link)
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
        #storage = None
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

        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = self.normalize_url(self.url, down_link[0])
            #storage = self.download_app(down_link)
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
    fuzzy_xpath = (
        "//div[@class='app-infoAintro']/"
        "div[@class='app-info']/p[position()<5]/text()"
    )
    down_xpath = "//a[@id='computerLoad']/@href"
    seperator = u'：'

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'版 本 号': 'human_version',
            u'开 发 者': 'company',
            u'发布时间': 'update_time',
            u'文件大小': 'size',
            u'支持固件': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            if item is not None:
                content = item.strip()
                label, value = content.split(self.seperator)
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
        return result


class Apk91Channel(ChannelSpider):
    """
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
    fuzzy_xpath = "//ul[@class='s_info']/li/text()"
    down_xpath = "//a[@class='s_btn s_btn4']/@href"
    seperator = u'：'

    def download_times(self, dtimes):
        times = 0
        token = u'万'
        if token in dtimes:
            try:
                times = int(dtimes[:-1]) * 10000
            except (TypeError, ValueError):
                pass
        else:
            try:
                times = int(dtimes)
            except (TypeError, ValueError):
                pass
        return times

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'版本': 'human_version',
            u'下载次数': 'download_times',
            u'文件大小': 'size',
            u'适用固件': 'env',
            u'分享日期': 'update_time',
            u'开发商': 'company',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times

        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = self.normalize_url(self.url, down_link[0])
        #    storage = self.download_app(down_link)
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
    seperator = ':'
    fuzzy_xpath = "//div[@class='right_con1_2 mt8 border1']/ul/li"
    down_xpath = "//li[@class='sign11 four_li1']/a/@href"

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'软件作者': 'company',
            u'语言界面': 'language',
            u'软件授权': 'authorize',
            u'下载次数': 'download_times',
            u'更新时间': 'update_time',
        }
        #storage = None
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()

        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times

        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
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
    times_xpath = "//div[@class='det-ins-num']/text()"
    size_xpath = "//div[@class='det-size']/text()"
    category_xpath = (
        "//div[@class='det-type-bdx']/"
        "a[@class='det-type-link']/text()"
    )
    label_xpath = "//div[@class='det-othinfo-tit']/text()"
    value_xpath = "//div[@class='det-othinfo-data']/text()"
    down_xpath = "//a[@class='det-down-btn']/@data-apkurl"

    def download_times(self, etree):
        times = 0
        token = u'亿'
        token1 = u'万'
        regx = re.compile('(?P<times>[\d\.]+)')
        times_dom = etree.xpath(self.times_xpath)
        if times_dom:
            rawtimes = times_dom[0]
            match = regx.search(rawtimes)
            if match is not None:
                try:
                    base_times = float(match.group('times'))
                except (TypeError, ValueError):
                    pass
                else:
                    if token in rawtimes:
                        times = int(base_times * 100000000)
                    elif token1 in rawtimes:
                        times = int(base_times * 10000)
                    else:
                        times = int(base_times)
        return times

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'版本号': 'human_version',
            u'更新时间': 'update_time',
            u'开发商': 'company',
        }
        etree = self.send_request(self.url)

        sizeraw = etree.xpath(self.size_xpath)
        if sizeraw:
            size = sizeraw[0].strip()
            result['size'] = size

        categoryraw = etree.xpath(self.category_xpath)
        if categoryraw:
            category = categoryraw[0].strip()
            result['category'] = category

        times = self.download_times(etree)
        result['download_times'] = times

        label_dom = etree.xpath(self.label_xpath)
        labels = [item.strip()[:-1] for item in label_dom]

        value_dom = etree.xpath(self.value_xpath)
        values = [item.strip() for item in value_dom]

        items = zip(labels, values)
        for item in items:
            label = item[0]
            label = mapping.get(label, '')
            if label:
                value = item[1]
                result[label] = value
        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
        return result


class MumayiChannel(ChannelSpider):
    """
    url: http://www.mumayi.com/android-28640.html
    软件类型：免费软件
    所属类别：新闻资讯
    更新时间：2014-08-26
    程序大小：18.62MB
    系统要求：1.5以上
    分  辨  率：240*320等
    运行权限：可放心下载
    安全检测：包含AdMob广告等1项插件
    """

    domain = "android.mumayi.com"
    seperator = u'：'
    fuzzy_xpath = "//ul[@class='istyle fl']/li"
    down_xpath = "//a[@class='download fl']/@href"

    def download_times(self):
        """
        下载次数：1620472次
        """
        from position import MumayiPosition
        position = MumayiPosition(
            self.title,
            has_orm=False,
        )
        times = position.download_times()
        return times

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'软件类型': 'authorize',
            u'所属类别': 'category',
            u'更新时间': 'update_time',
            u'程序大小': 'size',
            u'系统要求': 'env',
        }
        etree = self.send_request(self.url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()

        times = self.download_times()
        result['download_times'] = times

        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
        return result


class ZolChannel(ChannelSpider):
    """
    url: http://sj.zol.com.cn/mkey/
    下载次数： 93,866次
    """
    domain = "sj.zol.com.cn"
    down_xpath = (
        "//ul[@class='download-items']/li/"
        "a[@class='downLoad-button androidDown-button']/@onclick"
    )
    fuzzy_xpath = "//ul[@class='soft-text']/li"
    fuzzy2_xpath = "//ul[@class='summary-text clearfix']/li"
    seperator = u'：'
    env_xpath = (
        "//ul[@class='download-items']/li/"
        "a[@class='downLoad-button androidDown-button']/following::span/text()"
    )

    def download_times(self, dtimes):
        down_times = 0
        regx = re.compile(',')
        dregx = re.compile('(?P<times>\d+)')
        if dtimes:
            raw_string = regx.sub('', dtimes)
            match = dregx.search(raw_string)
            if match is not None:
                try:
                    down_times = int(match.group('times'))
                except:
                    pass
        return down_times

    def download_link(self, etree):
        down_link = None
        onclick = etree.xpath(self.down_xpath)[0]
        regx = re.compile("corpsoft\('([^']+)','1'\)")
        match = regx.search(onclick)
        if match is not None:
            down_link = match.group(1)
            down_link = self.normalize_url(self.url, down_link)
        return down_link

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'分类': 'category',
            u'厂商': 'company',
            u'更新': 'update_time',
            u'下载次数': 'download_times',
            u'系统要求': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        items2 = etree.xpath(self.fuzzy2_xpath)
        items.extend(items2)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()

        envraw = etree.xpath(self.env_xpath)
        if envraw:
            env = envraw[0].split(self.seperator)[-1]
            result['env'] = env

        times = self.download_times(
            result.get('download_times', '')
        )
        result['download_times'] = times
        #down_link = self.download_link(etree)
        return result


class PcOnlineChannel(ChannelSpider):
    """
    url: http://dl.pconline.com.cn/download/172907.html
    提供商：百度无线
    软件大小：7.59M
    软件授权：免费
    更新：2014-8-22
    软件评级：
    语言：简体中文
    """
    domain = "dl.pconline.com.cn"
    fuzzy_xpath = "//div[@class='megR']//i[@class='item']"
    info_xpath = "child::*/text()"
    times_xpath = "//a[@id='linkPage']/em[@id='span_dl_count']/text()"
    seperator = u'：'

    def download_link(self):
        pass

    def download_times(self, etree):
        times = 0
        dtimes = etree.xpath(self.times_xpath)
        if dtimes:
            dtimes = dtimes[0]
            try:
                times = int(dtimes)
            except (TypeError, ValueError):
                pass
        return times

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'语言': 'language',
            u'软件授权': 'authorize',
            u'更新': 'update_time',
            u'软件大小': 'size',
            u'提供商': 'company',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(etree)
        result['download_times'] = times
        return result


class SinaChannel(ChannelSpider):
    """
    url: http://down.tech.sina.com.cn/3gsoft/download.php?id=296
    文件类型：邮件收发
    软件厂商：网易
    版本信息：1.2.1
    文件大小：0.33 MB
    发布时间：2012-09-02
    推荐度：
    软件标签：邮件收发
    是否收费：免费
    适用系统：Android
    软件下载统计：本周：65　本月：70　总计：601
    """
    domain = "tech.sina.com.cn"
    fuzzy_xpath = "//div[@class='zcbox clearfix']/ul/li"
    child_p_xpath = "child::p"
    seperator = u'：'
    charset = 'gb2312'

    def download_times(self, dtimes):
        times = 0
        regx = re.compile('\d+')
        matches = regx.findall(dtimes)
        if matches:
            try:
                times = int(matches[-1])
            except (TypeError, ValueError):
                pass
        return times

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'文件类型': 'category',
            u'是否收费': 'authorize',
            u'适用系统': 'env',
            u'软件下载统计': 'download_times',
            u'软件厂商': 'company',
            u'版本信息': 'human_version',
            u'文件大小': 'size',
            u'发布时间': 'update_time',
        }
        etree = self.send_request(self.url, ignore=True)
        items = etree.xpath(self.fuzzy_xpath)
        leaives = []
        for item in items:
            child_p = item.xpath(self.child_p_xpath)
            if child_p:
                for dom in child_p:
                    leaives.append(dom)
            else:
                leaives.append(item)

        for item in leaives:
            content = item.text_content().strip()
            elems = content.split(self.seperator, 1)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
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

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def parser(self):
        result = {}
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        mapping = {
            u'版本': 'human_version',
            u'人气': 'download_times',
            u'更新': 'update_time',
            u'大小': 'size',
            u'授权': 'authorize',
            u'语言': 'language',
            u'系统要求': 'env',
        }
        for item in items:
            content = item.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
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
    seperator = u'：'

    def download_times(self, rawstring):
        times = 0
        translate = u"万"
        regx = re.compile('\d+')
        match = regx.search(rawstring)
        if match is not None:
            try:
                times = int(match.group())
            except (TypeError, ValueError):
                #log
                pass
            else:
                if translate in rawstring:
                    times = times * 10000
        return times

    def parser(self):
        result = {}
        mapping = {
            u'版\xa0本\xa0号': 'human_version',
            u'所属类型': 'category',
            u'更新时间': 'update_time',
            u'文件大小': 'size',
            u'下载次数': 'download_times',
            u'支持固件': 'env',
            u'开 发 者': 'company',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
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


class Android155Channel(ChannelSpider):
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
    seperator = u':'
    domain = "www.155.cn"
    child_a = "child::a/text()"
    fuzzy_xpath = "//div[@class='c1_xxi']/span"
    fuzzy2_xpath = "//div[@class='c1_xxi2']/span"
    down_xpath = "//div[@class='c1_bot']/a[@class='down']/@href"

    def download_times(self, dtimes):
        times = 0
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            rawtimes = match.group()
            try:
                times = int(rawtimes)
            except (TypeError, ValueError):
                pass
        return times

    def parser(self):
        result = {}
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        category = items[0].text_content().strip()
        result['category'] = category

        language_raw = items[1].text_content().strip()
        lang_auth = language_raw.split('/')
        if len(lang_auth) == 2:
            language, authorize = lang_auth
            result['language'] = language
            result['authorize'] = authorize
        else:
            language = lang_auth[0]
            result['language'] = language

        size = items[2].text_content().strip()
        result['size'] = size
        times = items[3].text_content().strip()
        times = self.download_times(times)
        result['download_times'] = times

        items = etree.xpath(self.fuzzy2_xpath)
        company_raw = items[0].text_content().split(self.seperator)
        if company_raw:
            company = company_raw[-1].strip()
            result['company'] = company

        update_time = items[1].text_content().strip()
        result['update_time'] = update_time
        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
        return result


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
    charset = 'gb2312'
    domain = "d.958shop.com"
    fuzzy_xpath = "//table[@class='m_word']/tr[position()>2 and position()<10]"
    down_xpath = "//div[@class='todown1']/a[@class='d1']"
    seperator = u'：'

    def download_times(self, etree):
        times = 0
        regx = re.compile('\d+')
        dom = etree.xpath(self.down_xpath)
        if dom:
            dom = dom[0]
            timesraw = dom.text_content().strip()
            match = regx.search(timesraw)
            if match is not None:
                rawtimes = match.group()
                try:
                    times = int(rawtimes)
                except (TypeError, ValueError):
                    pass
        return times

    def parser(self):
        result = {}
        mapping = {
            u'分类': 'category',
            u'大小': 'size',
            u'运行平台': 'env',
            u'软件性质': 'authorize',
            u'上传时间': 'update_time',
            u'浏览/下载次数': 'download_times',
        }
        etree = self.send_request(self.url, charset=self.charset)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(etree)
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

    seperator = u'：'
    domain = "www.liqucn.com"
    fuzzy_xpath = "//div[@class='app_boxcon']/table/tr/td"
    down_xpath = "//a[@id='content_mobile_href']/@href"

    def download_times(self, dtimes):
        times = 0
        try:
            times = int(dtimes[:-1])
        except (TypeError, ValueError):
            pass
        return times

    def parser(self):
        result = {}
        mapping = {
            u'下载次数': 'download_times',
            u'大小': 'size',
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
                value = value.strip()
                result[label] = value
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        #down_link = etree.xpath(self.down_xpath)[0]
        #if down_link:
            #storage = self.download_app(down_link)
        return result


class CnmoChannel(ChannelSpider):
    """
    应用价格：
    应用大小：22.7 MB
    应用分类：社交
    开发厂商：腾讯
    安全检测：安全
    版本：5.4.0.51_r798589
    语言：中文
    时间：2014-08-29 10:10:30
    运行环境：Android 2.2及更高版本
    """

    seperator = u'：'
    domain = 'www.cnmo.com'
    fuzzy_xpath = "//div[@class='basicInforL']/ul/li"

    def parser(self):
        result = {}
        mapping = {
            u'应用大小': 'size',
            u'应用分类': 'category',
            u'开发厂商': 'company',
            u'版本': 'human_version',
            u'语言': 'language',
            u'时间': 'update_time',
            u'运行环境': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            label = label.strip()
            label = mapping.get(label, '')
            if label:
                value = value.strip()
                result[label] = value
        print result
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
    domain = "www.crsky.com"
    fuzzy_xpath = "//div[@class='left']/div[@class='s_line']/p"
    down_xpath = "//div[@class='btns']/ul/li/a/@href"
    seperator = u'：'

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def download_link(self, etree):
        storage = None
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'开发厂商': 'company',
            u'软件大小': 'size',
            u'支持语言': 'language',
            u'所属分类': 'category',
            u'访问次数': 'download_times',
            u'上架时间': 'update_time',
            u'系统要求': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()

        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
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
        #storage = None
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
        #if down_link:
            #storage = self.download_app(down_link)
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
        #storage = None
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
    down_xpath = "//div[@class='contentdbtn']/a[@class='commentbtn']/@href"
    seperator = u'：'

    def parser(self):
        result = {}
        #storage = None
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
        print result
        return result


class BkillChannel(ChannelSpider):
    """
    url: http://www.bkill.com/download/23765.html
    软件大小 7.1MB
    软件语言 简体中文
    软件授权 免费软件
    更新日期 2014-07-05
    软件人气
    """

    seperator = u'：'
    domain = "www.bkill.com"
    fuzzy_xpath = (
        "//div[@class='soft_Abstract h305 w412 l top7 bd']"
        "/ul/li[@class='right']"
    )
    down_xpath = "//div[@class='down_link_main']/ul/li/a/@href"

    def download_times(self):
        times = 0
        times_url = "http://www.bkill.com/download/js/%s.js"
        pid = self.url.rsplit('/', 1)[-1].split('.')[0]
        url = times_url % pid
        regx = re.compile('\d+')
        content = self.send_request(url=url, tree=False)
        match = regx.search(content)
        if match is not None:
            times = int(match.group(0))
        return times

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'软件大小': 'size',
            u'软件语言': 'language',
            u'软件授权': 'authorize',
            u'更新日期': 'update_time',
            u'软件人气': 'download_times',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            elems = item.text_content().split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times()
        result['download_times'] = times
        return result


class ApkzuChannel(ChannelSpider):
    """
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
    seperator = u'：'

    def download_times(self):
        times = 0
        times_url = "http://www.apkzu.com/Inc/H.asp?id=%s"
        pid = self.url.rsplit('/', 1)[-1].split('.')[0]
        url = times_url % pid
        regx = re.compile('\d+')
        content = self.send_request(url=url, tree=False)
        match = regx.search(content)
        if match is not None:
            times = int(match.group(0))
        return times

    def parser(self):
        result = {}
        mapping = {
            u'类别': 'category',
            u'时间': 'update_time',
            u'大小': 'size',
            u'系统': 'env',
            u'授权': 'authorize',
            u'语言': 'language',
            u'人气': 'download_times',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times()
        result['download_times'] = times
        return result


class CngbaChannel(ChannelSpider):
    """
    资源类型： 其它
    资源厂商：
    资源大小： 4.51MB
    资源语言： 简体中文
    资源作者：
    授权方式： 共享软件
    整理时间： 2010-11-18
    """
    seperator = u'：'
    domain = "www.cngba.com"
    fuzzy_xpath = "//div[@class='down_softtext']/ul/li"

    def parser(self):
        result = {}
        #storage = None
        mapping = {
            u'资源类型': 'category',
            u'资源厂商': 'company',
            u'资源大小': 'size',
            u'资源语言': 'language',
            u'授权方式': 'authorize',
            u'整理时间': 'update_time',
            u'所属分类': 'category',
            u'大小': 'size',
            u'界面语言': 'language',
            u'开发厂商': 'company',
            u'更新时间': 'update_time',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            item = item.text_content().strip()
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
        print result
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

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'更新日期': 'update_time',
            u'文件大小': 'size',
            u'下载次数': 'download_times',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()

        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        #down_link = etree.xpath(self.down_xpath)
        #if down_link:
        #    down_link = down_link[0]
        #    storage = self.download_app(down_link)
        return result


class SohuChannel(ChannelSpider):
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

    seperator = u'：'
    domain = "download.sohu.com"
    fuzzy_xpath = "//div[@class='gy_02']/ul/li[position()<3]/text()"
    down_xpath = "//div[@class='gy_03 clear']/div[2]/a/@href"

    def download_times(self, dtimes):
        times = 0
        regx = re.compile('\d+')
        match = regx.search(dtimes)
        if match is not None:
            rawtimes = match.group()
            try:
                times = int(rawtimes)
            except (TypeError, ValueError):
                pass
        return times

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'下载': 'download_times',
            u'资费': 'authorize',
            u'语言': 'language',
            u'固件': 'env',
            u'开发商': 'company',
            u'大小': 'size',
            u'分类': 'category',
            u'版本': 'human_version',
            u'时间': 'update_time',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            elems = item.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip().replace(' ', '')
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        return result


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

    seperator = u'：'
    domain = "soft.shouji.com.cn"
    domain1 = "game.shouji.com.cn"
    fuzzy_xpath = "//ul[@class='des']/li[position()<10]"
    down_xpath = "//span[@class='bdown']/a[1]/@href"

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            headers = {
                'Cookie': 'JSESSIONID=abcfXvdIMD3UlhKjxFQGu;'
            }
            storage = self.download_app(down_link, headers=headers)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'更新时间': 'update_time',
            u'资费提示': 'authorize',
            u'当前版本': 'human_version',
            u'软件语言': 'language',
            u'软件类别': 'category',
            u'软件大小': 'size',
            u'适用固件': 'env',
        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            elems = item.text_content().split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip().replace(' ', '')
        return result


class OnlineDownChannel(ChannelSpider):
    """
    价格：免费版
    版本：5.4.0.66
    For Android
    类别：国产软件/社交
    大小：23592KB
    开发商：官方网站 相关软件
    人气：351888
    语言：简体中文
    日期：2014-9-10 15:29:54
    """

    seperator = u'：'
    domain = "www.onlinedown.net"
    fuzzy_xpath = "//div[@class='app_other']/ul[1]/li"
    pagedown_xpath = "//a[@class='btn_page']/@href"
    down_xpath = "//div[@class='info']/div[@class='down-menu']/a/@href"

    def download_link(self, etree):
        storage = None
        pagedown_link = etree.xpath(self.pagedown_xpath)[0]
        pagedown_link = self.normalize_url(self.url, pagedown_link)
        downdetail = self.send_request(pagedown_link)
        down_link = downdetail.xpath(self.down_xpath)[0]
        if down_link:
            storage = self.download_app(down_link)
        return storage

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def parser(self):
        result = {}
        mapping = {
            u'版本': 'human_version',
            u'类别': 'category',
            u'大小': 'size',
            u'开发商': 'company',
            u'人气': 'download_times',
            u'语言': 'language',
            u'日期': 'update_time',

        }
        etree = self.send_request(self.url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            elems = item.text_content().split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip().replace(' ', '')
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        return result


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

    seperator = u'：'
    domain = "www.eoemarket.com"
    fuzzy_xpath = "//ol[@class='feileis']/li"
    down_xpath = "//div[@class='detailsright']/ol/li[1]/a/@href"

    def download_times(self, dtimes):
        times = 0
        token = u'万'
        regx = re.compile('(?P<times>\d+)')
        match = regx.search(dtimes)
        if match is not None:
            times_raw = match.group('times')
            try:
                times = int(times_raw)
            except (TypeError, ValueError):
                pass
            else:
                if token in dtimes:
                    times = times * 10000
        return times

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'下载': 'download_times',
            u'大小': 'size',
            u'版本': 'human_version',
            u'更新时间': 'update_time',
            u'分类': 'category',
            u'适用': 'env',
        }
        etree = self.send_request(self.url, ignore=True)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            elems = item.text_content().split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                label = mapping.get(label.strip(), '')
                if label:
                    result[label] = value.strip()
        times = self.download_times(result.get('download_times', ''))
        result['download_times'] = times
        return result


class AibalaChannel(ChannelSpider):
    """
    url: http://www.aibala.com/android-soft-16102.html
    发布时间：2012-03-30
    软件大小：3MB
    版本：1.2.1
    研发公司：网易（杭州）网络有限公司MAG安卓团队
    运行环境：Android 1.6及以上
    """

    seperator = u'：'
    domain = "www.aibala.com"
    fuzzy_xpath = (
        "//div[@class='tabRightM']/"
        "div[contains(@class,'tabRightM')]/text()"
    )
    times_xpath = (
        "//div[@class='listMainRightBottomL']/"
        "div[@class='tabLeftB']/div[@class='tabLeftB1']/text()"
    )
    down_xpath = (
        "//div[@class='listMainRightBottomL']"
        "/div[@class='RightB1']/a[1]/@onclick"
    )

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

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        r = re.compile("window.location.href='(.+)';return false;")
        down_link = r.search(down_link)
        down_link = down_link.group(1)
        if down_link:
            down_link = self.normalize_url(self.url, down_link)
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'发布时间': 'update_time',
            u'软件大小': 'size',
            u'版本': 'human_version',
            u'运行环境': 'env',
            u'研发公司': 'company',
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
        times = self.download_times(etree)
        result['download_times'] = times
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

    seperator = u'：'
    domain = "app.vmall.com"
    times_xpath = "//span[@class='grey sub']/text()"
    fuzzy_xpath = (
        "//ul[@class='app-info-ul nofloat']"
        "/li[@class='ul-li-detail']"
    )
    down_xpath = "//a[@class='mkapp-btn mab-download']/@onclick"

    def download_times(self, etree):
        times = 0
        regx = re.compile('(?P<times>\d+)')
        times_dom = etree.xpath(self.times_xpath)
        if times_dom:
            raw_times = times_dom[0]
            match = regx.search(raw_times)
            if match is not None:
                times = int(match.group('times'))
        return times

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        r = re.compile("'(http://appdl\.hicloud\.com/[^']+)'")
        down_link = r.search(down_link)
        down_link = down_link.group(1)
        print down_link
        if down_link:
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'大小': 'size',
            u'日期': 'update_time',
            u'开发者': 'company',
            u'版本': 'human_version',
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
        result['download_times'] = self.download_times(etree)
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

    seperator = u'：'
    domain = "www.yruan.com"
    fuzzy_xpath = (
        "//ul[@class='Download-m']/"
        "li[@class='rightd']/dl[@class='leftdl']/dt"
    )
    down_xpath = "//li[@class='downimg']/div[@class='down_link']/a/@href"

    def download_times(self, dtimes):
        try:
            times = int(dtimes)
        except (TypeError, ValueError):
            times = 0
        return times

    def download_link(self, etree):
        pagedown_link = etree.xpath(self.down_xpath)[0]
        if pagedown_link is not None:
            r = re.compile("id=([0-9]+)&")
            soft_id = r.search(pagedown_link)
            soft_id = soft_id.group(1)
            down_link = "http://www.yruan.com/down.php?id=%s" % soft_id
            if down_link:
                storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'软件分类': 'category',
            u'软件资费': 'authorize',
            u'更新时间': 'update_time',
            u'软件语言': 'language',
            u'软件大小': 'sieze',
            u'下载次数': 'download_times',
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
        times = result.get('download_times', '')
        result['download_times'] = self.download_times(times)
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

    seperator = u'：'
    domain = "www.baicent.com"
    fuzzy_xpath = "//div[@class='viewbox']/div[@class='infolist']"
    label_xpath = "child::small[position()<last()]/text()"
    value_xpath = "child::span[position()<last()]"
    times_xpath = "//div[@class='infolist']/span/script/@src"
    script_xpath = "child::script/@src"
    down_xpath = "//ul[@class='downurllist']/li[1]/a/@href"

    def download_times(self, etree):
        times = 0
        regx = re.compile('\d+')
        times_url = etree.xpath(self.times_xpath)
        if times_url:
            times_url = self.normalize_url(self.url, times_url[0])
            content = self.send_request(url=times_url, tree=False)
            match = regx.search(content)
            if match is not None:
                times = int(match.group(0))
        return times

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        down_link = self.normalize_url(self.url, down_link)
        if down_link:
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'软件类型': 'category',
            u'授权方式': 'authorize',
            u'界面语言': 'language',
            u'软件大小': 'size',
            u'运行环境': 'env',
            u'发布时间': 'update_time',
            u'下载次数': 'download_times',
        }
        etree = self.send_request(self.url)
        base_dom = etree.xpath(self.fuzzy_xpath)
        if base_dom:
            base_dom = base_dom[0]
            labels = base_dom.xpath(self.label_xpath)
            values_dom = base_dom.xpath(self.value_xpath)
            values = [v.text_content().strip() for v in values_dom]
            items = zip(labels, values)
            for item in items:
                label = item[0].strip()[:-1]
                label = mapping.get(label, '')
                if label:
                    result[label] = item[1].strip()
            times = self.download_times(etree)
            result['download_times'] = times
        return result


class ZhuodownChannel(ChannelSpider):
    """
    ***无下载次数***
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
    pagedown_xpath = "//ul[@class='downurllist']/a/@href"
    down_xpath = "//div[@class='advancedsearch']/table/tr[2]/td/li[1]/a/@href"
    seperator = u'：'

    def download_link(self, etree):
        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            storage = self.download_app(down_link)
        return storage

    def parser(self):
        result = {}
        mapping = {
            u'所属分类': 'category',
            u'授权方式': 'authorize',
            u'软件大小': 'size',
            u'应用版本': 'human_version',
            u'软件语言': 'language',
            u'适用平台': 'env',
            u'作者': 'company',
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
        return result

if __name__ == '__main__':
    zhuodown = ZhuodownChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url=(
            "http://www.zhuodown.com/a/yingyongruanjian/"
            "wangluotongxin/20140909/32225.html"
        ),
        title=u'网易新闻'
    )
    #zhuodown.run()

    baicent = BaicentChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.baicent.com/plus/view-288996-1.html",
        title=u'网易新闻'
    )
    #baicent.run()

    yruan = YruanChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.yruan.com/softdetail/584/",
        title=u'网易新闻'
    )
    #yruan.run()

    vmall = VmallChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://app.vmall.com/app/C9147",
        title=u'网易新闻'
    )
    #vmall.run()

    aibala = AibalaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.aibala.com/android-soft-61.html",
        title=u'网易新闻'
    )
    #aibala.run()

    eomarket = EoemarketChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.eoemarket.com/soft/33223.html",
        title=u'网易新闻'
    )
    #eomarket.run()

    onlinedown = OnlineDownChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.onlinedown.net/soft/110940.htm",
        title=u'网易新闻'
    )
    #onlinedown.run()

    shouji = ShoujiChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://soft.shouji.com.cn/down/20275.html#dlshow",
        title=u'网易新闻'
    )
    #shouji.run()

    sohu = SohuChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://download.sohu.com/app/info?app_id=21174",
        title=u'网易新闻'
    )
    #sohu.run()

    androidcn = AndroidcnChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://down.androidcn.com/detail/1234.html",
        title=u'网易新闻'
    )
    #androidcn.run()

    cngba = CngbaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://android.cngba.com/androidruanjian/20101118117822.shtml",
        title=u'网易新闻'
    )
    cngba.run()

    apkzu = ApkzuChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.apkzu.com/game/12569.shtml",
        title=u'网易新闻'
    )
    #apkzu.run()

    bkill = BkillChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.bkill.com/download/23765.html",
        title=u'网易新闻'
    )
    #bkill.run()

    anzow = AnzowChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.anzow.com/download/Software/JQKRDPQQP8.shtml",
        title=u'网易新闻'
    )
    anzow.run()

    wandoujia = WandoujiaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://www.wandoujia.com/apps/com.halfbrick.fruitninja',
        title=u'水果忍者安卓版v1.9.5'
    )
    #wandoujia.run()

    sjwyx = SjwyxChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://sklr.sjwyx.com/down/",
        title=u'网易新闻'
    )
    #sjwyx.run()

    dchannel = DChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://android.d.cn/software/12486.html",
        title=u'工行短信银行'
    )
    #dchannel.run()

    cnmo = CnmoChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://app.cnmo.com/android/1440/',
        title=u'水果忍者安卓版v1.9.5'
    )
    cnmo.run()

    crsky = CrskyChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://android.crsky.com/soft/25385.html",
        title=u'网易新闻'
    )
    #crsky.run()

    shop958 = Shop958Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url=(
            "http://d.958shop.com/soft/196F4351-"
            "CCB4-46B3-9A6F-DB705CB88A75.html"
        ),
        title=u'网易新闻'
    )
    #shop958.run()

    liqucn = LiqucnChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://os-android.liqucn.com/yx/15024.shtml",
        title=u'工行短信银行'
    )
    #liqucn.run()

    android155 = Android155Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://android.155.cn/soft/10198.html",
        title=u'网易新闻'
    )
    #android155.run()

    nduoa = NduoaChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url='http://www.nduoa.com/apk/detail/634370',
        title=u'工行短信银行'
    )
    #nduoa.run()

    imobile = ImobileChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://app.imobile.com.cn/android/app/8025.html",
        title=u'网易新闻'
    )
    #imobile.run()

    duote = DuoteChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.duote.com/soft/23385.html",
        title=u'网易新闻'
    )
    #duote.run()

    sina = SinaChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://down.tech.sina.com.cn/3gsoft/download.php?id=296",
        title=u'网易新闻'
    )
    #sina.run()

    pconline = PcOnlineChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://dl.pconline.com.cn/download/172907.html",
        title=u'网易新闻'
    )
    #pconline.run()

    zol = ZolChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://sj.zol.com.cn/umplayer/",
        title=u'网易新闻'
    )
    #zol.run()

    mumayi = MumayiChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://www.mumayi.com/android-28640.html",
        title=u'网易新闻'
    )
    #mumayi.run()

    qq = QQChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://sj.qq.com/myapp/detail.htm?apkName=com.tencent.mm",
        title=u'水果忍者安卓版v1.9.5'
    )
    #qq.run()

    it168 = It168Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url="http://down.it168.com/315/321/130157/index.shtml",
        title=u'水果忍者安卓版v1.9.5'
    )
    #it168.run()

    apk91 = Apk91Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url=(
            "http://apk.91.com/Soft/Android/com."
            "tencent.mm-480-5.4.0.66_r807534.html"
        ),
        title=u'水果忍者安卓版v1.9.5'
    )
    #apk91.run()

    gfan = GfanChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://apk.gfan.com/Product/App235332.html',
        title=u'水果忍者安卓版v1.9.5'
    )
    #gfan.run()

    hiapk = HiapkChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://apk.hiapk.com/appinfo/com.mobi.screensaver.fzlxqx2',
        title=u'水果忍者安卓版v1.9.5'
    )
    #hiapk.run()

    pchome = PcHomeChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://soft.anruan.com/3751/",
        title=u'水果忍者手机版 For Android'
    )
    pchome.run()

    anruan = AnRuanChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://soft.anruan.com/3751/",
        title=u'工行短信银行'
    )
    #anruan.run()

    xiazaizhijia = XiaZaiZhiJiaChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.xiazaizhijia.com/shouji/6570.html",
        title=u'工行短信银行'
    )
    #xiazaizhijia.run()

    apk8 = Apk8Channel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        #url="http://www.apk8.com/game/game_14104.html",
        url="http://www.apk8.com/soft/soft_127.html",
        title=u'工行短信银行'
    )
    #apk8.run()

    p3533 = Channel3533(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://game.3533.com/game/49703/',
        title=u'水果忍者安卓版v1.9.5'
    )
    #p3533.run()

    pc6 = PC6Channel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.pc6.com/azyx/82254.html",
        title=u'工行短信银行'
    )
    #pc6.run()

    c7xz = Channel7xz(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.7xz.com/games/view/10020683",
        title=u'工行短信银行'
    )
    #c7xz.run()

    shoujibaidu = ShoujiBaiduChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://shouji.baidu.com/game/item?docid=7022461",
        title=u'工行短信银行'
    )
    #shoujibaidu.run()

    crossmo = CrossmoChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://soft.crossmo.com/softinfo_13185.html",
        title=u'工行短信银行'
    )
    #crossmo.run()

    coolapk = CoolApkChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.coolapk.com/game/sh.lilith.dgame.uc",
        title=u'工行短信银行'
    )
    #coolapk.run()

    sjapk = SjapkChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.sjapk.com/36195.Html",
        title=u'工行短信银行'
    )
    #sjapk.run()

    jiqimao = JiQiMaoChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://jiqimao.com/game-199571/",
        title=u'工行短信银行'
    )
    #jiqimao.run()

    angeeks = AngeeksChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://apk.angeeks.com/soft/10133401.html",
        title=u'工行短信银行'
    )
    #angeeks.run()

    anzhi = AnZhiChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.anzhi.com/soft_1322730.html",
        title=u'工行短信银行'
    )
    #anzhi.run()

    downza = DownzaChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.downza.cn/soft/22271.html",
        title=u'工行短信银行',
    )
    #downza.run()

    apk3 = Apk3Channel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.apk3.com/soft/4393.html",
        title=u'工行短信银行',
    )
    #apk3.run()

    c520 = Channel520Apk(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.520apk.com/android/dongzuoyouxi/100012517.html",
        title=u'工行短信银行'
    )
    #c520.run()

    mm10086 = Mm10086Channel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url=(
            "http://mm.10086.cn/android/info/300002796373.html?from=www"
            "&stag=cT0zRCVFNyVCQiU4OCVFNiU5RSU4MSVFNyU4QiU4MiVFOSVBMyU5O"
            "TMmcD0xJnQ9JUU1JTg1JUE4JUU5JTgzJUE4JnNuPTImYWN0aXZlPTE%3D"
        ),
        title=u'水果忍者安卓版v1.9.5'
    )
    #mm10086.run()

    gamedog = GameDogChannel(
        channellink=1,
        app_uuid='1',
        app_version=1,
        channel=1,
        url='http://android.gamedog.cn/game/386653.html',
        title=u'水果忍者安卓版v1.9.5'
    )
    #gamedog.run()

    oyksoft = OykSoftChannel(
        channellink=1,
        app_uuid='acfd7fd6-74a3-42ab-82b3-dfc541caad72',
        app_version=1,
        channel=36,
        url="http://www.oyksoft.com/soft/20852.html",
        title=u'微软官方Windows 7主题《水果忍者》'
    )
    #oyksoft.run()
