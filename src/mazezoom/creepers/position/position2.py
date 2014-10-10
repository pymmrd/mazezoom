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
    domain = "zhushou.360.cn"
    search_url = "http://zhushou.360.cn/search/index/?kw=%s"
    base_xpath = "//div[@class='SeaCon']/ul/li"
    link_xpath = "child::dl/dd/h3/a"
    down_xpath = "child::div[@class='seaDown']/div[@class='download comdown']/a/@href"    #S

    def download_link(self, etree):
        down_link = ''
        down_text = etree.xpath(self.down_xpath)
        if down_text:
            down_text = down_text[0]
            regx = re.compile('url=(?P<down_link>.+)')
            match = regx.search(down_text)
            if match is not None:
                down_link = match.group('down_link')
        return down_link

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.attrib['title']
            if self.app_name in title:
                link = self.normalize_url(
                    self.search_url,
                    elem.attrib['href']
                )
                if self.is_accurate:
                    down_link = self.download_link(item)
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    results.append((link, title))
        return results


class TaoBaoPosition(PositionSpider):
    """
    无用
    """
    name = u'淘宝手机助手'
    domain = "app.taobao.com"
    abstract = True


class MiPosition(PositionSpider):
    name = u'小米应用商店'
    domain = "app.mi.com"
    search_url = "http://app.mi.com/searchAll?keywords=%s&typeall=phone"
    #xpath = "//ul[@class='applist']/li/h5/a"
    base_xpath = "//ul[@class='applist']/li"
    link_xpath = "child::h5/a"
    down_xpath = "//div[@class='app-info-down']/a/@href"    #D

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text.strip()
            if self.app_name in title:
                link = self.normalize_url(
                    self.search_url,
                    elem.attrib['href']
                )

                detail = self.send_request(url=link)
                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    down_link = self.normalize_url(
                        link,
                        down_link[0]
                    )
                print down_link

                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    results.append((link, title))
        return results

#error 下载js
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

class UCPosition(PositionSpider):
    """
    """
    name = u'UC应用商店'
    domain = "apps.uc.cn"
    search_url = "http://apps.uc.cn/search?keyword=%s"
    base_xpath = "//ul[@class='J_commonAjaxWrap']/li"
    link_xpath = "child::div[@class='sq-app-list small']/dl/dt/a"
    down_xpath = "child::a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = self.normalize_url(
                    self.search_url,
                    elem.attrib['href']
                )
                print title, link 
                down_link = item.xpath(self.down_xpath)
                if down_link:
                    down_link = self.normalize_url(
                        link,
                        down_link[0]
                    )
                print down_link

                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
                    results.append((link, title))
        return results

#error 下载js
class MeizuPosition(PositionSpider):
    """
    (S,D)
    """
    name = u'魅族应用商店'
    domain = "app.meizu.com"
    search_url = "http://app.meizu.com/apps/public/search/page?cat_id=1&keyword=%s&start=0&max=60"    #cat_id=2游戏
    detail_url = "http://app.meizu.com/apps/public/detail?package_name=%s"

    def position(self):
        results = []
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % quote_app
        content = self.get_content(url)
        content = content.decode(self.charset)
        output = json.loads(content)
        appList = output.get('value', {}).get('list', [])
        print len(appList)
        #获取搜索结果title和链接
        for app in appList:
            link = self.detail_url % app.get('package_name', '')
            title = app.get('name', '').strip()
            print title, link
            #downcount = app.get('download_count', '')
            if self.app_name in title:
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
    down_xpath = "child::div[@class='appListDown tcenter']/a/@href"    #S

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

                down_link = item.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]

                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
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
    down_xpath = "descendant::div[@class='m-t5']/a/@href"

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

                            down_link = dom.xpath(self.down_xpath)
                            if down_link:
                                down_link = down_link[0]

                            if self.is_accurate:  # 精确匹配
                                match = self.verify_app(
                                down_link=down_link,
                                )
                                if match:
                                    results.append((link, title))
                                    break
                            else:
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
    (S,)
    """
    name = u'手机娱乐'
    domain = "sj.91.com"
    search_url = "http://play.91.com/android/Search/index.html?keyword=%s"
    base_xpath = "//div[@class='box search_list']/dl"
    link_xpath = "child::dt/a"
    times_xpath = "child::em[@class='cor_blue']/text()"
    down_xpath = "child::dd[last()]/a[@class='spr down_btn']/@href"

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

                down_link = item.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]

                if self.is_accurate:  # 精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                    )
                    if match:
                        results.append((link, title))
                        break
                else:
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

class Zhidian3gPosition(PositionSpider):
    """
    """
    name = u'指效应用中心'
    domain = "app.zhidian3g.cn"
    token = 'Android'
    search_url = "http://app.zhidian3g.cn/appSoftware_search_list.shtml?d=%(time)s&appName=%(app_name)s&page.pageNo=1&isFirstSearch=false"
    base_xpath = "//table[@class='app_list_table']/tr/td"
    link_xpath = "child::div[@class='app_list_table_box']/div[@class='app_list_table_title']/a"
    info_xpath = "child::div[@class='app_list_table_box']/div[@class='app_list_table_info']"

    def position(self):
        results = []
        import time
        time = time.strftime("%a %b %d %Y %H:%M:%S %Z", time.localtime())
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % {'time': time, 'app_name': quote_app}
        print url
        etree = self.get_elemtree(url, ignore=True)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        print len(items)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            info_elem = item.xpath(self.info_xpath)[0]
            info = info_elem.text_content().strip()
            if self.app_name in title and self.token in info:
                print title
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

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
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % quote_app
        etree = self.get_elemtree(url, ignore=True)
        #etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.attrib['title'].strip()
            print title
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

class MaopaokePosition(PositionSpider):
    """
    """
    name = u'冒泡客'
    domain = "www.maopaoke.com"
    search_url = (
        "http://www.maopaoke.com/open/default/search"
        "?category=0&sub_category=&size=&filter_price=off&"
        "filter_jingpin=off&sort=published_time&page=1&key=%s"
    )
    base_xpath = "//ul/li"
    link_xpath = "child::div[@class='card']//div[@class='appname']/a"

    def position(self):
        results = []
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % quote_app
        etree = self.get_elemtree(url, ignore=True)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            print title
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class SouyingyongPosition(PositionSpider):
    """
    """
    name = u'搜应用'
    domain = "www.soyingyong.com"
    search_url = "http://www.soyingyong.com/apps/search/%s.html"
    base_xpath = "//ul[@class='card']/li[@class='card-item']"
    link_xpath = "child::div[@class='app-content']/div[@class='detail']/h2/a"

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
                results.append((link, title))
        return results

class BaikcePosition(PositionSpider):
    """
    """
    name = u'APP安卓市场'
    domain = "apps.baikce.cn"
    search_url = "http://apps.baikce.cn/search.aspx?q=%s&s=app"
    base_xpath = "//div[@class='list']/div[@class='top-data']"
    link_xpath = "child::dl/dd[@class='title']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            print title
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class SoftonicPosition(PositionSpider):
    """
    """
    name = u'软件天堂'
    domain = "www.softonic.cn"
    search_url = "http://www.softonic.cn/s/%s:android"
    base_xpath = "//ol[@id='program_list']/li[@class='list-program-item js-listed-program']"
    link_xpath = "child::div[@class='list-program-column-first']/h5/a"
    
    def position(self):
        results = []
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % quote_app
        etree = self.get_elemtree(url, ignore=True)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            print title
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class A280Position(PositionSpider):
    """
    """
    name = u'安卓下载网'
    domain = "www.a280.cn"
    search_url = "http://www.a280.com/?a=search&kw=%s"
    base_xpath = "//div[@class='softlist']/div[@class='one']"
    link_xpath = "child::div[@class='rtxt']/div[@class='softname']/a"
    
    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            print title
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class MeizumiPosition(PositionSpider):
    """
    """
    name = u'魅族迷'
    domain = "www.meizumi.com"
    search_url = "http://www.meizumi.com/search?q=%s"
    base_xpath = "//div[@class='list']/ul/li"
    link_xpath = "child::div[@class='info']/h4/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            print title
            if self.app_name in title:
                link = elem.attrib['href']
                results.append((link, title))
        return results

class CncrkPosition(PositionSpider):
    """
    """
    name = u'起点下载'
    domain = "www.cncrk.com"
    charset = 'gb2312'
    android_token = 'Android'
    search_url = "http://www.cncrk.com/search.asp?keyword=%s&stype=ResName&x=0&y=0"
    base_xpath = "//div[@class='results']/ul/li"
    link_xpath = "child::span[@class='softname']/a[@class='top']"
    token_xpath = "child::span[@class='softname']/a[1]/text()"
        
    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            token = item.xpath(self.token_xpath)
            if self.app_name in title and self.android_token in token:
                print title, token
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class ZerosjPosition(PositionSpider):
    """
    """
    name = u'零点安卓手机软件'
    domain = "www.zerosj.com"
    charset = 'gb2312'
    search_url = "http://www.zerosj.com/search/index.php"
    base_xpath = "//td[@width='556']/table[@class='tablebordercss']/tr[2]/td[@valign='top']/table"
    link_xpath = "child::tr[1]/td/table/tr/td[1]/a"

    def position(self):
        results = []
        data = {'show': 1, 'keyboard': self.app_name.encode(self.charset), 'Submit': '搜索'}
        etree = self.send_request(data=data)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        print len(items)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class AppdhPosition(PositionSpider):
    """
    """
    name = u'app导航'
    domain = "www.appdh.com"
    search_url = "http://www.appdh.com/keyword/?s=%s"
    base_xpath = "//div[@class='clearfix light_line pt_20 pb_20']"
    link_xpath = "child::div[@class='grid_8']/p/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                print title
                link = elem.attrib['href']
                results.append((link, title))
        return results

class ItopdogPosition(PositionSpider):
    """
    """
    name = u'软件盒子'
    domain = "www.itopdog.cn"
    search_url = "http://www.itopdog.cn/home.php?type=az&ct=home&ac=search&q=%s"    #type=az表示安卓
    base_xpath = "//div[@class=' panel-list-imgbrief']/dl"
    link_xpath = "child::dd/strong[@class='name']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                print title
                link = elem.attrib['href']
                results.append((link, title))
        return results

class MogustorePosition(PositionSpider):
    """
    """
    name = u'蘑菇市场'
    domain = "www.mogustore.cn"
    search_url = "http://www.mogustore.com/search.html"
    base_xpath = "//div[@class='pro_box app_list app_list_b']/ul/li"
    link_xpath = "child::div[@class='title']/h2/a"

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
                print title
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class LeidianPosition(PositionSpider):
    """
    """
    name = u'雷电手机搜索'
    domain = "www.leidian.com"
    search_url = "http://www.leidian.com/s?q=%s&ie=utf-8&t=&src=shouji_www"
    base_xpath = "//ul[@class='mod-soft-list']/li[@class='clearfix']"
    link_xpath = "child::div[@class='mod-soft-info']/h2/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                print title
                link = elem.attrib['href']
                results.append((link, title))
        return results

class Position2265(PositionSpider):
    """
    """
    name = u'2265安卓游戏'
    domain = "www.2265.com"
    search_url = "http://www.2265.com/sea_%s.html"
    base_xpath = "//div[@class='listbox10']/div[@class='tcm']/ul/li"
    link_xpath = "child::div[@class='rtxtinfo']/div[@class='c']/dl/dt/span[1]/a[1]"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            if self.app_name in title:
                print title
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class sz1001Position(PositionSpider):
    """
    """
    name = u'1001下载乐园'
    domain = "www.sz1001.net"
    charset = 'gb2312'
    token = 'Android'
    token1 = u'安卓'
    search_url = "http://www.sz1001.net/query.asp?q=%s&x=0&y=0"
    base_xpath = "//div[@id='results']/ul"
    link_xpath = "child::li[@class='softname']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            title = title.split(u' . ')[1]
            if self.app_name in title and self.token in title or self.token1 in title:
                print title
                link = self.normalize_url(self.search_url, elem.attrib['href'])
                results.append((link, title))
        return results

class XdownsPosition(PositionSpider):
    """
    """
    name = u'绿盟'
    domain = "www.xdowns.com"
    charset = 'gb2312'
    token = 'Android'
    search_url = "http://tag.xdowns.com/tag.asp?keyword=%s"
    base_xpath = "//div[@id='searchpageTitle']"
    content_xpath = "following::div[@id='searchpageName'][1]/a"
    link_xpath = "child::span/a[@class='showtopic']"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #获取搜索结果title和链接
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            title = elem.text_content().strip()
            content_elem = item.xpath(self.content_xpath)[0]
            content = content_elem.text_content().strip()
            if self.app_name in title and self.token in content:
                print title
                link = elem.attrib['href']
                results.append((link, title))
        return results

if __name__ == "__main__":
    m163 = Sj91Position(
       u'忍者',
       is_accurate=True,
       has_orm=False,
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    print m163.run()
