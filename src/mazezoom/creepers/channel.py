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
    >>>p520apk = Position520Apk()
    >>>p520apk.run(u'QQ部落')
    """
    domain = "www.520apk.com"


class Apk3Channel(ChannelSpider):
    """
    >>>apk3 = Apk3Position()
    >>>apk3.run(u'刷机精灵')
    """
    domain = "www.apk3.com"


class DreamsDownChannel(ChannelSpider):
    domain = "www.dreamsdown.com"


class AnZhiChannel(ChannelSpider):
    """
    >>>anzhi = AnZhiPosition()
    >>>anzhi.run(u'去哪儿')
    """
    domain = "www.anzhi.com"


class AngeeksChannel(ChannelSpider):
    """
    >>>angeek = AngeeksPosition()
    >>>angeek.run(u'飞机')
    """
    domain = "www.angeeks.com"


class JiQiMaoChannel(ChannelSpider):
    """
    >>>jiqimao = JiQiMaoPosition()
    >>>jiqimao.run(u'金银岛')
    """
    domain = "jiqimao.com"


class SjapkChannel(ChannelSpider):
    """
    >>>sjapk = SjapkPosition()
    >>>sjapk.run(u'喜羊羊之灰太狼闯关')
    """
    domain = "www.sjapk.com"


class CoolApkChannel(ChannelSpider):
    """
    >>>coolapk = CoolApkPosition()
    >>>coolapk.run(u'刀塔传奇')
    """
    domain = "www.coolapk.com"


class Channel365Nokia(ChannelSpider):
    """
    >>>nokia365 = Position365Nokia()
    >>>nokia365.run(u'HTC')
    """
    domain = "www.365nokia.cn"


class CrossmoChannel(ChannelSpider):
    """
    >>>cs = CrossmoPosition()
    >>>cs.run(u'LT来电报号')
    """
    domain = "www.crossmo.com"


class ShoujiBaiduChannel(ChannelSpider):
    """
    >>>shouji = ShoujiBaiduSpider()
    >>>shouji.run(u'HOT市场')
    """

    domain = "shouji.baidu.com"


class Channel7xz(ChannelSpider):
    """
    >>>p7xz = Position7xz()
    >>>p7xz.run(u'极品飞车13')
    """
    domain = "www.7xz.com"


class PC6Channel(ChannelSpider):
    """
    >>>pc6 = PC6Position()
    >>>pc6.run(u'弹跳忍者')
    """
    domain = "www.pc6.com"


class Channel3533(ChannelSpider):
    """
    >>>p3533 = Position3533()
    >>>p3533.run(u'功夫西游')
    """
    domain = "www.3533.com"


class Apk8Channel(ChannelSpider):
    """
    >>>apk8 = Apk8Position()
    >>>apk8.run(u'天天跑酷')
    """
    domain = "www.apk8.com"


class XiaZaiZhiJiaChannel(ChannelSpider):
    """
    >>>xzzj = XiaZaiZhiJiaPosition()
    >>>xzzj.run(u'微信')
    """
    domain = "www.xiazaizhijia.com"


class CngbaChannel(ChannelSpider):
    """
    >>>cngba = CngbaPosition()
    >>>cngba.run(u'名将决')
    """
    domain = "www.cngba.com"


class SjwyxChannel(ChannelSpider):
    """
    >>>sjwyx = SjwyxPosition()
    >>>sjwyx.run(u'龙印')
    """
    domain = "www.sjwyx.com"


class Ruan8Channel(ChannelSpider):
    """
    >>>ruan8 = Ruan8Position()
    >>>ruan8.run(u'360')
    """
    domain = "soft.anruan.com"


class PcHomeChannel(ChannelSpider):
    """
    >>>pchome = PcHomePosition()
    >>>pchome.run(u'微信')
    """
    domain = "www.pchome.com"

if __name__ == '__main__':
    #url = "http://www.oyksoft.com/soft/32456.html"
    #oyk = OykSoftChannel()
    #print oyk.run(url)

    #url = "http://android.gamedog.cn/online/233523.html"
    #gamedog = GameDogChannel()
    #print gamedog.run(url)

    url = "http://mm.10086.cn/android/info/300008279684.html?from=www&stag=cT0lRTglQTElOTclRTUlQTQlQjQlRTglQjYlQjMlRTclOTAlODMmcD0xJnQ9JUU1JTg1JUE4JUU5JTgzJUE4JnNuPTEmYWN0aXZlPTE%3D"
    mm10086 = Mm10086Channel()
    mm10086.run(url)
