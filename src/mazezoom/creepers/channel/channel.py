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
import base64
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

    def run(self, url):
        result = {}
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        down_link = etree.xpath(self.down_xpath)[0]
        storage = self.download_app(down_link)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
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

    def run(self, url):
        result = {}
        seperator = u'安卓版'
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        down_link = etree.xpath(self.down_xpath)[0]
        title = etree.xpath(self.title_xpath)[0]
        version = title.split(seperator)[-1]
        result['version'] = version
        storage = self.download_app(down_link)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
            else:
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

    def run(self, url):
        result = {}
        etree = self.send_request(url)
        version = etree.xpath(self.version_xpath)[0]
        down_link = etree.xpath(self.down_xpath)[0]
        #下载app
        storage = self.download_app(down_link)
        result['version'] = version
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

    def run(self, url):
        label_version = u'版本：'
        result = {}
        stroage = None
        etree = self.send_request(url)

        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            try:
                label = item.xpath(self.label_xpath)[0].strip()
                value = item.xpath(self.value_xpath)[0].strip()
            except IndexError:
                pass
            else:
                result[label] = value

        version = result.get(label_version, '').strip().lower()
        if version.startswith('v'):
            version = version[1:]

        down_link = etree.xpath(self.down_xpath)[0]
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
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

    def run(self, url):
        result = {}
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.xpath)

        version = etree.xpath(self.version_xpath)
        if version:
            version = version[0].strip()

        for item in items:
            if item.strip():
                label, value = item.split(self.seperator)
                result[label.strip()] = value.strip()

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(url,down_link[0])
            storage = self.download_app(down_link)
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
    fuzzy_xpath = "//div[@class='intro']/ul[@class='clearfix']/li/text()" 
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


    def run(self, appname, chksum=None, is_accurate=True):
        result = {}
        dlabel = u"下载次数" 
        stroage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        version = self.get_version(etree)
        for item in items:
            if item.strip():
                label, value = item.split(self.seperator)
                result[label.strip()] = value.strip()

        times = int(result.get(dlabel, 0))

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        
        #版本
        version = etree.xpath(self.version_xpath)
        if version:
            version = version[0] 
            #(1.1.1)
            if version.startswith('('):
                version = version[1:-1]
        #所有属性
        items = etree.xpath(self.fuzzy_xpath) 
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()

        #下载次数
        times = self.download_times(result)
        
        #下载链接
        down_link = self.download_link(etree)
        if down_link:
            storage = self.download_app(down_link)

        return result


class AngeeksChannel(ChannelSpider):
    """
    """
    domain = "www.angeeks.com"
    down_xpath = "//div[@class='rgmainsrimg']/a/@href"
    seperator = u':'
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
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()
        times = result.get(self.label)

        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
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
    label = u'下载次数'

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            print content
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()
        times = int(result.get(self.label))
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link, session=self.session)
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

    def run(self, url):
        result = {}
        storage = None
        seperator = u'：'
        version_label = "版本"
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            values = item.text_content().strip().split(' ')
            values = [v for v in values if bool(v)]
            for vl in values:
                lv = vl.split(seperator)
                if len(lv) == 2:
                    result[lv[0].strip()] = lv[1].strip()

        version = result.get(version_label, None)
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = self.normalize_url(url, down_link[0])
            storage = self.download_app(down_link, session=self.session)
        return result


class CoolApkChannel(ChannelSpider):
    """
     52人关注，6万+次下载，300个评论，1
     3个权限，简体中文，127.00 M，
     支持2.2及更高版本，3天前更新 
    """
    domain = "www.coolapk.com"
    fuzzy_xpath = "//div[@class='hidden-md hidden-lg ex-page-infobar']/div/a/span"
    down_xpath = "//div[@class='ex-page-header']/following::script[1]/text()"
    label_xpath = "child::text()"
    value_xpath = "child::strong/text()"
    version_xpath = "/h1[@class='media-heading ex-apk-view-title']/small/text()"

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
            extra_xpath = "//div[@class='media-btns ex-apk-view-btns']/a/@onclick"
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
                down_link = 'http://%s%s%s' % (self.domain, down_match.group('url'), extra)
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            value = item.xpath(self.value_xpath)[0].strip()
            label = item.xpath(self.label_xpath)[0].strip()
            result[label] = value

        times = self.download_times(result)

        down_link = self.download_link(etree) 
        if down_link:
            storage = self.download_app(down_link, session=self.session)
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
    label = u'下载次数'
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
        ) %(appkey, appid)
        down_app = (
            "http://soft.crossmo.com/softdown_topc_v5.php?"
            "crossmo=%s&downloadtype=local&appid=%s"
        ) % (appkey, appid)
        headers = {
            'X-Requested-With':'XMLHttpRequest',
            'Referer': url
        }
        self.update_request_headers(headers)
        self.send_request(url=check_app, tree=False)
        return down_app


    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()
        try:
            times = int(result.get(self.label))
        except (TypeError, ValueError):
            times = 0

        appkey = self.get_appkey(etree)
        appid = self.get_appid(url)
        down_link = self.download_link(appkey, appid)
        if down_link:
            storage = self.download_app(down_link,session=self.session)
        return result


class ShoujiBaiduChannel(ChannelSpider):
    """
    >>>shouji = ShoujiBaiduSpider()
    >>>shouji.run(u'HOT市场')
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()

        version = result.get(self.version_label, '')
        times = self.download_times(result)
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split(self.seperator)
            if len(elems) == 2:
                label, value = elems
                result[label.strip()] = value.strip()
        version = self.get_version(etree)
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split('\n')
            for elem in elems:
                label, value = elem.split(self.seperator)
                result[label.strip()] = value.strip()
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()

        times = int(result.get(self.label))
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
    version_label = u'游戏版本'

    def download_times(self, etree):
        times = 0
        try:
            times = int(etree.xpath(self.times_xpath)[0])
        except (TypeError, ValueError, IndexError):
            times = 0
        return times

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            elems = content.split('\n')
            for elem in elems:
                label, value = elem.split(self.seperator)
                result[label.strip()] = value.strip()
        version = result.get(self.version_label, '') 
        times = self.download_times(etree)
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

    def run(self, url):
        result = {}
        storage = None
        self.send_request(url, tree=False)
        headers = {
            'X-Requested-With':'XMLHttpRequest',
            'Referer': url
        }
        self.update_request_headers(headers)
        etree = self.send_request('%s?' % url, ignore=True)
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
                    print value
            result[title] = value
        times = result.get(self.down_label, 2)
        version = self.get_version(etree)
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            item = item.strip()
            if item:
                label, value = content.split(self.seperator)
                result[label.strip()] = value.strip()
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

    def run(self, url):
        result = {}
        down_link = ''
        storage = None
        etree = self.send_request(url, ignore=True)
        lists = etree.xpath(self.fuzzy_list_xpath)
        for elem in lists:
            title = elem.xpath(self.title_xpath)[0].strip()
            if title == self.accurate_token:
                items = elem.xpath(self.fuzzy_xpath) 
                for item in items: 
                    downbtn = item.xpath("child::a[@class='downbtn']/@href")
                    if downbtn:
                        down_link = donwbtn[0]
                    else:
                        content = item.text_content().strip()
                        label, value = content.split(self.seperator)
                        result[label.strip()] = value.strip()
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

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        down_link = None
        for item in items:
            cls = item.attrib.get('class', '')
            if cls == 'app_green' :
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
                    result[label.strip()] = value.strip()
        version = result.get(self.version_label, '')
        times = int(result.get(self.down_label))
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
    seperator = "："
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
                href = link.attrib.get('href', '')
                etree = self.send_request(url)
                items = etree.xpath(self.fuzzy_xpath)
                if items:
                    item = items[0]
                    match = regx.search(item)
                    if match is not None:
                        down_link = match.group('link')
        return down_link

    def run(self, url):
        result = {}
        storage = None
        etree = self.send_request(url)
        items = etree.xpath(self.fuzzy_xpath)
        for item in items:
            content = item.text_content().strip()
            label, value = content.split(self.seperator)
            result[label.strip()] = value.strip()
        times = self.download_times()
        down_link = etree.xpath(self.down_xpath)
        if down_link:
            down_link = down_link[0]
            storage = self.download_app(down_link)
        return result

if __name__ == '__main__':
    #url = "http://www.oyksoft.com/soft/32456.html"
    #oyk = OykSoftChannel()
    #print oyk.run(url)

    #url = "http://android.gamedog.cn/online/233523.html"
    #gamedog = GameDogChannel()
    #print gamedog.run(url)

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
    #ruan8.run(ur)

    url = ""
