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
    domain = "zhushou.36.cn"


class MiChannel(ChannelSpider):
    domain = "app.mi.com"


class NearMeChannel(ChannelSpider):
    domain = "store.nearme.com.cn"


class LenovoChannel(ChannelSpider):
    domain = 'app.lenovo.com'


class UCChannel(ChannelSpider):
    domain = "apps.uc.cn"


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
