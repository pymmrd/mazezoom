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
            elem = item.xpath(self.link_xpath)[0]
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
    domain = 'app.lenovo.com'
    search_url = "http://app.lenovo.com/search/index.html?q=%s"
    base_xpath = "//ul[@class='appList']/li[@class='borderbtm1 pr']"
    link_xpath = "child::div[@class='appDetails']/p[@class='f16 ff-wryh appName']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text.strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results


class UCPosition(PositionSpider):
    """
    """
    name = u'UC应用商店'
    domain = "apps.uc.cn"
    search_url = "http://apps.uc.cn/search?keyword=%s"
    base_xpath = "//ul[@class='J_commonAjaxWrap']/li"
    link_xpath = "child::div[@class='sq-app-list small']/dl/dt/a"
    down_xpath = "child::a[@class='sq-btn blue-light']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class YeskyPosition(PositionSpider):
    """
    """
    name = u'天极下载'
    domain = u'mydown.yesky.com'
    abstract = True

class QQAppPosition(PositionSpider):
    """
    """
    name = u'腾讯应用中心'
    domain = "http://qqapp.qq.com"
    abstract = True


class M163Position(PositionSpider):
    """
    """
    name = u'网易应用中心'
    domain = "m.163.com"
    search_url = "http://m.163.com/search/multiform?platform=2&query=%s"
    base_xpath = "//div[@class='arti m-b15']"
    token_xpath = "child::div[@class='arti-hd arti-hd-bar']/div/div/h3/span/@class"
    android_token = 'ico-android'
    link_base_xpath = "child::div[@class='arti-bd']/descendant::li"
    link_xpath = "descendant::h3/a"
    down_xpath = "descendant::div[@class='m-t5']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            token_dom = item.xpath(self.token_xpath)
            if token_dom:
                rawtoken = token_dom[0].strip()
                if rawtoken == self.android_token:
                    doms = item.xpath(self.link_base_xpath)
                    for dom in doms: 
                        elem = dom.xpath(self.link_xpath)[0]
                        title = elem.text_content().strip()
                        if self.app_name in title:
                            link = self.normalize_url(self.search_url, elem.attrib['href'])
                            results.append((link, title))
        return results

class MopPosition(PositionSpider):
    """
    无用
    """
    name = u'掌上猫扑'
    domain = "http://m.mop.com"
    abstract = True

class Sj91Position(PositionSpider):
    """
    """
    name = u'手机娱乐'
    domain = "sj.91.com"
    search_url = "http://play.91.com/android/Search/index.html?keyword=%s"
    base_xpath = "//div[@class='box search_list']/dl"
    link_xpath = "child::dt/a"
    times_xpath = "child::em[@class='cor_blue']/text()"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class VmallPosition(PositionSpider):
    """
    重复
    """
    name = u'华为应用市场'
    domain = "app.vmall.com"
    abstract = True

class Gao7Position(PositionSpider):
    """
    """
    name = u'搞趣网'
    domain = "http://www.gao7.com"
    search_url = "http://www.gao7.com/search.do?key=%s&listType=6"
    base_xpath = "//ul[@class='app-list']/li"
    link_xpath = "child::div[@class='app-list-main']/h3/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class UucunPosition(PositionSpider):
    """
    无用
    """
    name = u'悠悠村'
    domain = "http://www.uucun.com/"
    abstract = True

class DomobPosition(PositionSpider):
    """
    无用
    """
    name = u'多盟'
    domain = "http://www.domob.cn/"
    abstract = True

class AndroidmiPosition(PositionSpider):
    """
    """
    name = u'安智迷'
    domain = "www.androidmi.com"
    search_url = "http://www.androidmi.com/index.php?m=search&c=index&a=init&typeid=55&siteid=1&q=%s"
    base_xpath = "//ul[@class='wrap']/li[@class='wrap']"
    link_xpath = "child::div/h5/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class Vapp51Position(PositionSpider):
    """
    """
    name = u'安卓商店'
    domain = "www.51vapp.com"
    search_url = "http://www.51vapp.com/market/apps/search.vhtml?ct=%s"
    base_xpath = "//div[@class='l_list']/ul/li"
    link_xpath = "child::a[1]"
    title_xpath = "child::a/h4"
    down_xpath = "child:a[2]/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class OperaPosition(PositionSpider):
    """
    """
    name = u'Opera'
    domain = "apps.opera.com"
    search_url = "http://apps.opera.com/zh_cn/catalog.php?search=%s"
    base_xpath = "//ul[@class='appList category']/li[@class='appItem']"
    link_xpath = "child::a[@class='appLink download']"
    title_xpath = "child::a[@class='appLink download']/span[@class='appTitle']"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            title_elem = item.xpath(self.title_xpath)[0]
            title = title_elem.text_content().strip()
            if self.app_name in title:
                link_elem = item.xpath(self.link_xpath)[0]
                link = link_elem.attrib['href']
                results.append((link, title))
        return results

class AduuPosition(PositionSpider):
    """
    无用
    """
    name = u'优友'
    domain = "www.aduu.cn"
    abstract = True

class AppchinaPosition(PositionSpider):
    """
    """
    name = u'应用汇'
    domain = "www.appchina.com"
    search_url = "http://www.appchina.com/sou/%s/?catname=应用"
    search_url2 = "http://www.appchina.com/sou/%s/?catname=游戏"
    base_xpath = "//ul[@class='app-list']/li[@class='has-border app']"
    link_xpath = "child::div[@class='app-info']/h1[@class='app-name']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url2)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        items2 = etree2.xpath(self.base_xpath)
        items.extend(items2)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

####
class Zhidian3gPosition(PositionSpider):
    """
    """
    name = u'指效应用中心'
    domain = "app.zhidian3g.cn"
    token = 'Android'
    search_url = "http://app.zhidian3g.cn/appSoftware_search_index.shtml"
    base_xpath = "//div[@class='app_list_table_box']"
    link_xpath = "child::div[@class='app_list_table_title']/a"
    info_xpath = "child::div[@class=='app_list_table_info']"

    def position(self):
        results = []
        data = {'appName': self.app_name.encode(self.charset)}
        etree = self.send_request(data=data)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            info_elem = item.xpath(self.info_xpath)[0]
            info = info_elem.text_content().strip()
            print info
            if self.app_name in title and self.token in info:
                link = elem.attrib['href']
                results.append((link, title))
        return results

#error 汉字乱码
class PaojiaoPosition(PositionSpider):
    """
    """
    name = u'泡椒网'
    domain = "kuang.paojiao.cn"
    search_url = "http://kuang.paojiao.cn/search/list_%s_1.html"
    base_xpath = "//ul[@id='ajaxContainer']/li"
    link_xpath = "child::a[@class='module-list-wrap cf tapLink']"
    down_xpath = "child::span[@class='btn-green download_apk']"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.attrib['title'].strip()
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                down_elem = item.xpath(self.down_xpath)[0]
                down_link = self.normalize_url(self.search_url, down_elem.attrib['href'])
                results.append((link, title))
        return results

class TompdaPosition(PositionSpider):
    """
    """
    name = u'TOMPDA'
    domain = "android.tompda.com"
    search_url = "http://android.tompda.com/0-7-1-0-1?keyword=%s"
    search_url2 = "http://android.tompda.com/game/0-12-1-0-1?keyword=%s"
    base_xpath = "//div[@class=' content_list']"
    link_xpath = "child::dl/dt/b/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url2)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        items2 = etree2.xpath(self.base_xpath)
        items.extend(items2)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class BorporPosition(PositionSpider):
    """
    """
    name = u'宝瓶网'
    domain = "www.borpor.com"
    charset= 'gb2312'
    search_url = "http://www.borpor.com/class.php"
    base_xpath = "//div[@class=' b  center_ner']/ul"
    link_xpath = "child::li[2]/p[1]/a"

    def position(self):
        results = []
        data = {'keyword': self.app_name.encode(self.charset)}
        etree = self.send_request(data=data)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

#error
class MaopaokePosition(PositionSpider):
    """
    """
    name = u'冒泡客'
    domain = "www.maopaoke.com"
    search_url = "http://www.maopaoke.com/open/list?keyword=%s"
    base_xpath = "//ul/li"
    #link_xpath = "child::div[@class='card']//div[@class='appname']/a"
    link_xpath = "child::a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

if __name__ == "__main__":
    m163 = UCPosition(
       u'忍者',
       is_accurate=False,
       has_orm=False,
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    print m163.run()
