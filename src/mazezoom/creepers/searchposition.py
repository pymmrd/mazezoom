# -*- coding:utf-8 -*-

#Author:chenyu
#Date:2014/08/24
#Email:chenyuxxgl@126.com

import re
import json
import time
from base import PositionSpider

class HiapkPosition(PositionSpider):
    """
    下载次数：否
    备选：    热度/评分次数
    位置：    信息页
    """
    domain = "apk.hiapk.com"
    search_url = "http://apk.hiapk.com/search?key=%s"
    xpath = "//span[@class='list_title font12']/a"
    down_xpath = "//a[@class='link_btn']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]
            down_link = self.normalize_url(link, down_link)

            if is_accurate:    #精确匹配
                match = self.verify_app(
                    down_link=down_link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results

#
class GfanPosition(PositionSpider):
    """
    下载次数：否
    备选：    评分次数
    位置：    信息页
    """
    domain = "apk.gfan.com"
    search_url = "http://apk.gfan.com/search?q=%s"
    xpath = "//span[@class='apphot-tit']/a"
    down_xpath = "//a[@id='computerLoad']/@href"
    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]

            if is_accurate:    #精确匹配
                match = self.verify_app(
                    down_link=down_link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results

class Apk91Position(PositionSpider):
    """
    下载次数：是（文字）
    位置：    信息页
    搜索：    分类搜索
    极少数detail页里没有down_link
    """
    domain = "apk.gfan.com"
    search_url = "http://apk.91.com/soft/android/search/1_5_0_0_%s"
    search_url1 = "http://apk.91.com/game/android/search/1_5_%s"
    xpath = "//div[@class='zoom']/h4/a"
    down_xpath = "//a[@class='s_btn s_btn4']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            down_link = None
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
            try:
                down_link = detail.xpath(self.down_xpath)[0]
                down_link = self.normalize_url(self.search_url, down_link)
            except:
                pass

            print link, title
            print down_link

            if down_link is not None:
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        print "----------"
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class AngeeksPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "apk.angeeks.com"
    charset = 'gb2312'
    search_url = "http://apk.angeeks.com/search?keywords=%s&x=0&y=0"
    base_xpath = "//ul[@id='mybou']/li/dl/dd"
    link_xpath = "child::div[@class='info']/a/@href"
    title_xpath = "child::div[@class='info']/a/text()"
    down_xpath = "child::div[@class='dowl']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.base_xpath)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.xpath(self.link_xpath)[0]
            )
            title = item.xpath(self.title_xpath)[0]
            down_link = item.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                down_link = self.normalize_url(self.search_url, down_link)
            if is_accurate:    # 精确匹配
                match = self.verify_app(
                    down_link=down_link,
                    chksum=chksum
                )
                if match:
                    results.append((link, title))
            else:
                results.append((link, title))
        return results

class It168Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    结果不区分平台
    """
    domain = "down.it168.com"
    charset = 'gb2312'
    suffix = u'.apk'
    search_url = "http://down.it168.com/soft_search.html?keyword=%s"
    xpath = "//div[@class='r3']/ul/li/h3/a"
    down_xpath = "//li[@class='sign11 four_li1']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]
            if down_link.endswith(self.suffix):
                print title, down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class PcHomePosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    不区分平台
    从detail页进入download页，通过onclick获取真实down_link
    """
    domain = "download.pchome.net"
    #charset = 'gbk'
    search_url = "http://download.pchome.net/search-%s---0-1.html"
    xpath = "//div[@class='tit']/a"
    pagedown_xpath = "//div[@class='dl-con-left']//div[@class='dl-info-btn']/a/@href"
    os_token = 'Android'
    value_xpath = "//div[@class='dl-info-con']/ul/li/text()|//div[@class='dl-info-con']/ul/li/a/text()"
    down_xpath = "//dl[@class='clearfix']/dd[last()]/a/@onclick"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            detail = self.get_elemtree(link)
            values = detail.xpath(self.value_xpath)
            pagedown_link = detail.xpath(self.pagedown_xpath)[0]
            if self.os_token in values:
                print link , title
                downdetail = self.get_elemtree(pagedown_link)
                onclick = downdetail.xpath(self.down_xpath)[0]
                r = re.compile("windowOpen\('([^']+)'\);")
                onclick_content = r.search(onclick)
                down_link = onclick_content.group(1)
                print down_link

                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class QQPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    Json,Ajax,目前搜索结果只能取到前10个
    """
    domain = "sj.qq.com"
    search_url = "http://sj.qq.com/myapp/searchAjax.htm?kw=%s&pns=&sid="
    detail_url = "http://sj.qq.com/myapp/detail.htm?apkName=%s"
    down_xpath = "//div[@class='det-ins-btn-box']/a[@class='det-down-btn']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        quote_app = self.quote_args(appname)
        url = self.search_url % quote_app
        content = self.get_content(url)
        output = json.loads(content)    #output['obj']['appDetails'][0].keys()
        appList = output['obj']['appDetails']
        for app in appList:
            link = self.detail_url % app['pkgName']
            title = app['appName']
            #downcount = app['appDownCount']
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]
            if down_link:
                print link, title, down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class MumayiPosition(PositionSpider):
    """
    下载次数：是
    位置：    列表页
    """
    domain = "android.mumayi.com"
    search_url = "http://s.mumayi.com/index.php?q=%s"
    xpath = "//ul[@class='applist']//h3[@class='hidden']/a"
    times_xpath = "//ul[@class='appattr hidden']/li[@class='num']/text()"
    down_xpath = "//a[@class='download fl']/@href"

    def download_times(self, title):
        """
        下载次数：1620467次
        """
        seperator = u'下载次数：'
        etree = self.send_request(title)
        item = etree.xpath(self.times_xpath)
        times = None
        if item:
            item = item[0]
            print item
            try:
                times = item.split(seperator)[-1] 
                print times
            except (TypeError, IndexError, ValueError):
                pass
        return times

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print link, title
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#安卓频道跳转到百度手机助手
class SkycnPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "www.skycn.com"
    search_url = "http://shouji.baidu.com/s?wd=%s&data_type=app&from=as"
    xpath = "//a[@class='app-name']"
    down_xpath = "//div[@class='area-download']/a[@class='apk']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print link, title
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class ZolPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "sj.zol.com.cn"
    charset = 'gbk'
    search_url = "http://xiazai.zol.com.cn/search?wd=%s&type=1"
    xpath = "//ul[@class='results-text']/li[@class='item']/div[@class='item-header clearfix']/a"
    down_xpath = "//ul[@class='download-items']/li[@class='item'][1]/a[@class='downLoad-button androidDown-button']/@onclick"
    token = 'sj'

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            results.append((link, title))
            detail = self.get_elemtree(link)
            onclick = detail.xpath(self.down_xpath)[0]
            r = re.compile("corpsoft\('([^']+)','1'\)")
            onclick_content = r.search(onclick)
            down_link = onclick_content.group(1)
            down_link = self.normalize_url(link, down_link)
            print down_link

            if self.token in link:
                if is_accurate:    #精确匹配
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}
                    match = self.download_app(down_link, headers=headers)
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))

        return results

#error js生成下载链接，token未取到
class PcOnlinePosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "dl.pconline.com.cn"
    charset = 'gb2312'
    search_url = ("http://ks.pconline.com.cn/download.shtml"
                 "?q=%s"
                 "&downloadType=Android%%CF%%C2%%D4%%D8")    # %%表示%
    xpath = "//a[@class='aTitle']"
    down_xpath = "//a[@class='btn sbDownload']/@tempurl"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        data = {}
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath) #js根据token计算真实的下载地址
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error js生成下载链接，有超时时间设置
class SinaPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "tech.sina.com.cn"
    charset = 'gb2312'
    search_url = "http://down.tech.sina.com.cn/3gsoft/iframelist.php?classid=0&keyword=%s&tag=&osid=4"
    xpath = "//div[@class='b_txt']/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

#error onclick动态生成下载链接
class DuotePosition(PositionSpider):
    """
    下载次数：是(人气)
    位置：    信息页
    """
    domain = "www.duote.com"
    charset = 'gb2312'
    search_url = "http://www.duote.com/searchPhone.php?searchType=&so=%s"
    xpath = "//div[@class='list_item']/div[@class='tit_area']/span[@class='name']/a"
    down_xpath = "//div[@class='btn_trig'][1]/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath) 
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#下载文件量超过23M，连接会被断开
class ImobilePosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "www.imobile.com.cn"
    search_url = "http://app.imobile.com.cn/android/search/%s.html"
    xpath = "//ul[@class='ranking_list']/li/div[@class='ico']/h3/a"
    down_xpath = "//div[@class='download_install']/a[@class='download']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error 下载页面打不开
class ApkzuPosition(PositionSpider):
    """
    下载次数：是(人气)
    位置：    信息页
    """
    domain = "www.apkzu.com"
    charset = 'gb2312'
    search_url = "http://www.apkzu.com/search.asp?k=%s&c=1"
    search_url1 = "http://www.apkzu.com/search.asp?k=%s&c=2"
    xpath = "//div[@class='recList']/div[@class='recSinW btmLine1']/dl/dt/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class NduoaPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "www.nduoa.com"
    search_url = "http://www.nduoa.com/search?q=%s"
    xpath = "//ul[@class='apklist clearfix']//div[@class='name']/a"
    title_xpath = "child::span[1]/text()"
    down_xpath = "//a[@id='BDTJDownload']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.xpath(self.title_xpath)[0]
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                down_link = self.normalize_url(self.search_url, down_link)
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class Android115Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "www.155.cn"
    charset = 'gb2312'
    search_url = "http://android.155.cn/search.php?kw=%s&index=soft"
    xpath = "//ul[@class='gmc-c']/li/strong/a"
    down_xpath = "//div[@class='c1_bot']/a[@class='down']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                down_link = self.normalize_url(self.search_url, down_link)
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error 下载页面跳转过多
class Shop985Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    分类搜索，搜索结果没有区分平台
    """
    domain = "d.958shop.com"
    charset = 'gb2312'
    search_url = "http://d.958shop.com/search/?keywords=%s&cn=soft"
    #search_url1 = "http://d.958shop.com/search/?keywords=%s&cn=game"    #游戏下载页面跳转3次
    xpath = "//span[@class='t_name01']/a[@class='b_f']"
    os_token = 'Android'
    platform_xpath = "//table[@class='m_word']/tr[6]/td/a/text()"
    #info_xpath = "child::td//text()"
    down_xpath = "//div[@class='todown1']/a[1]/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        #etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        #items2 = etree2.xpath(self.xpath)
        #items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            detail = self.get_elemtree(link)
            platform = detail.xpath(self.platform_xpath)[0]
            if self.os_token in platform:
                #print platform
                print link, title,"--------------------------"
                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]
                    if down_link == '#goto_download':
                        down_url = link+down_link
                        down_page = self.get_elemtree(down_url)
                        down_xpath = "//dd[@class='down_u']/a/@href"
                        down_link = down_page.xpath(down_xpath)[0]

                    else:
                        down_link = down_link
                    print down_link

                    if is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=chksum
                        )
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results

#有连接断开的风险
class LiqucnPosition(PositionSpider):
    """
    下载次数：否
    位置：    信息页
    搜索：    根据Cookie或者referer来区别用户手机系统
    """
    domain = "www.liqucn.com"
    android_referer = 'http://os-android.liqucn.com/'
    search_url = "http://search.liqucn.com/download/%s"
    xpath = "//li[@class='appli_info']/a"
    down_xpath = "//a[@id='content_mobile_href']/@href"
    os_token = 'os-android'

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        headers = {'Referer': self.android_referer}
        etree = self.send_request(appname, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            time.sleep(2)
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if self.os_token in link:
                if down_link:
                    down_link = down_link[0]
                    print down_link
                    if is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=chksum
                        )
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results

#error 下载地址js
class CnmoPosition(PositionSpider):
    """
    下载次数：否
    备选：    赞次数
    位置：    信息页
    """
    domain = "www.cnmo.com"
    charset = 'gb2312'
    search_url = "http://app.cnmo.com/search/c=a&s=%s&p=2&f=1"    #p=2代表Android平台
    xpath = "//ul[@class='ResList']/li/div[@class='Righttitle'][1]/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

#下载速度特慢
class CrskyPosition(PositionSpider):
    """
    下载次数：否
    备选：    访问量
    位置：    信息页
    搜索：    搜索结果比浏览器展示条目要少
    """
    domain = "www.crsky.com"
    charset = 'gb2312'
    search_url = "http://sj.crsky.com/query.aspx?keyword=%s&type=android"
    xpath = "//div[@class='right']//a"
    down_xpath = "//div[@class='btns']/ul/li/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                   'Refererhttp': 'http://sj.crsky.com/query.aspx?keyword=%cd%f8%d2%d7&type=android'}
        etree = self.send_request(appname, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#下载页面js生成
class DPosition(PositionSpider):
    """
    下载次数：是
    位置：    列表页
    """
    domain = "www.d.cn"
    search_url = "http://android.d.cn/search/app/?keyword=%s"
    xpath = "//p[@class='g-name']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class AndroidcnPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    应用、游戏、资讯、壁纸、主题使用不同二级域名
    列表页与结果页下载次数不一致
    """
    domain = "www.androidcn.com"
    search_url = "http://down.androidcn.com/search/q/%s"
    search_url1 = "http://game.androidcn.com/search/q/%s"
    xpath = "//h2/a"
    down_xpath = "//p[@class='dl-add-3']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error 下载页面打不开
class ApkcnPosition(PositionSpider):
    """
    下载次数：否
    备选：    无
    搜索：    post
    """
    domain = "www.apkcn.com"
    search_url = "http://www.apkcn.com/search/"
    xpath = "//div[@class='box']/div[@class='post indexpost']/h3/a"
    down_xpath = "//div[@class='imginfo']/p[2]/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        data = {'keyword': appname.encode(self.charset), 'select': 'phone'}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                down_link = self.normalize_url(link, down_link)
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results


class SohoPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    同 app.sohu.com
    """
    domain = "download.sohu.com"
    search_url = "http://download.sohu.com/search?words=%s"
    xpath = "//div[@class='yylb_box']/div[@class='yylb_main']/p[@class='yylb_title']/strong/a"
    down_xpath = "//div[@class='gy_03 clear']/div[2]/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#下载需要Cookie信息
class ShoujiPosition(PositionSpider):
    """
    下载次数：否
    备选：    评论次数
    位置：    信息页
    搜索：    应用和游戏分类搜索，域名不同
    """
    domain = "soft.shouji.com.cn"
    domain1 = "game.shouji.com.cn"
    search_url = (
        "http://soft.shouji.com.cn/sort/search.jsp"
        "?html=soft"
        "&phone=100060"    #100060代表安卓平台
        "&inputname=soft"
        "&softname=%s"
        "&thsubmit=搜索"
    )
    search_url1 = (
        "http://game.shouji.com.cn/gamelist/list.jsp"
        "?html=soft"
        "&phone=100060"
        "&inputname=game"
        "&gname=%s"
        "&thsubmit=搜索"
    )
    xpath = "//div[@id='bklist']//li[@class='bname']/a"
    down_xpath = "//span[@class='bdown']/a[1]/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                              'Cookie': 'JSESSIONID=abcfXvdIMD3UlhKjxFQGu; Hm_lvt_eaff2b56fe662d8b2be9c4157d8dab61=1409462138; Hm_lpvt_eaff2b56fe662d8b2be9c4157d8dab61=1409463774'}
                    match = self.download_app(down_link, headers=headers)
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        for item in items2:
            link = self.normalize_url(self.search_url1, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                              'Cookie': 'JSESSIONID=abcfXvdIMD3UlhKjxFQGu; Hm_lvt_eaff2b56fe662d8b2be9c4157d8dab61=1409462138; Hm_lpvt_eaff2b56fe662d8b2be9c4157d8dab61=1409463774'}
                    match = self.download_app(down_link, headers=headers)
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#页面下载403
class Mobile1Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    json返回数据
    """
    domain = "www.1mobile.tw"
    search_url = "http://www.1mobile.tw/index.php?c=search.json&keywords=%s&page=1"

    def run(self, appname):
        results = []
        quote_app = self.quote_args(appname)
        url = self.search_url % quote_app
        content = self.get_content(url)
        output = json.loads(content)
        appList = output['appList']
        for app in appList:
            link = app['appLink']
            title = app['appTitle']
            results.append((link, title))
            print link, title
        return results

class OnlineDownPosition(PositionSpider):
    """
    下载次数：否
    备选：    人气数
    位置：    信息页
    排行列表页有下载量，搜索列表页无，结果页无
    """
    domain = "www.onlinedown.net"
    search_url = (
        "http://search.newhua.com/search_list.php"
        "?searchname=%s"
        "&searchsid=6"
        "&app=search"
        "&controller=index"
        "&action=search"
        "&type=news"
    )
    xpath = "//div[@class='title']/strong/a[1]"
    pagedown_xpath = "//a[@class='btn_page']/@href"
    down_xpath = "//div[@class='info']/div[@class='down-menu']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            pagedown_link = detail.xpath(self.pagedown_xpath)[0]
            pagedown_link = self.normalize_url(link, pagedown_link)
            print pagedown_link
            downdetail = self.get_elemtree(pagedown_link)
            down_link = downdetail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error 汉字显示乱码
class EoemarketPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "www.eoemarket.com"
    search_url = "http://www.eoemarket.com/search_.html?keyword=%s&pageNum=1"
    xpath = "//ol[@class='RlistName']/li[1]/span/a"
    down_xpath = "//div[@class='detailsright']/ol/li[1]/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#网站巨慢，detail无法打开
class ApkolPosition(PositionSpider):
    """
    下载次数：否
    备选：    安装次数
    搜索：    信息页打开慢
    """
    domain = "www.apkol.com"
    search_url = "http://www.apkol.com/search?keyword=%s"
    xpath = "//div[@class='listbox ty']/div[@class='yl_pic']/a"
    down_xpath = "//div[@content]/div[@class='cn_btn']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.attrib['title']
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            print down_link
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class BkillPosition(PositionSpider):
    """
    下载次数：否
    备选：    人气
    位置：    信息页
    搜索：    高级搜索
    """
    domain = "www.bkill.com"
    charset = 'gb2312'
    search_url = "http://www.bkill.com/d/search.php?mod=do&n=1"
    xpath = "//div[@class='clsList']/dl/dt/a"
    down_xpath = "//div[@class='down_link_main']/ul/li/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        data = {
            'keyword': appname.encode(self.charset),
            'area': 'name',
            'category': '0',
            'field[condition]': 'Android',
            'order': 'downcount',    #updatetime
            'submit': '搜 索',
            'way': 'DESC'
        }
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[-1]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class AibalaPosition(PositionSpider):
    """
    下载次数：否
    备选：    关注数
    位置：    信息页
    搜索：    列表页与结果页不一致
    """
    domain = "www.aibala.com"
    search_url = "http://www.aibala.com/android-search-1-0-0-%s-1-1"
    xpath = "//ul[@class='block']/li//div[@class='tabRightTL']/a"
    down_xpath = "//div[@class='listMainRightBottomL']/div[@class='RightB1']/a[1]/@onclick"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]
            r = re.compile("window.location.href='(.+)';return false;")
            down_link = r.search(down_link)
            down_link = down_link.group(1)
            if down_link:
                down_link = self.normalize_url(link, down_link)
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results


class VmallPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    华为开发者联盟-->华为应用市场
    """
    domain = "app.vmall.com"
    search_url = "http://app.vmall.com/search/%s"
    xpath = "//div[@class='list-game-app dotline-btn nofloat']/div[@class='game-info  whole']/h4[@class='title']/a"
    down_xpath = "//a[@class='mkapp-btn mab-download']/@onclick"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]
            r = re.compile("'(http://appdl\.hicloud\.com/[^']+)'")
            down_link = r.search(down_link)
            down_link = down_link.group(1)
            print down_link
            if down_link:
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class YruanPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索:     搜索结果不区分平台
    """
    domain = "www.yruan.com"
    search_url = "http://www.yruan.com/search.php?keyword=%s"
    xpath = "//span[@class='item_name']/a"
    token = 'Android'
    down_xpath = "//li[@class='downimg']/div[@class='down_link']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            if self.token in title:
                print link, title
                detail = self.get_elemtree(link)
                pagedown_link = detail.xpath(self.down_xpath)[0]
                if pagedown_link is not None:
                    r = re.compile("id=([0-9]+)&")
                    soft_id = r.search(pagedown_link)
                    soft_id = soft_id.group(1)
                    down_link = "http://www.yruan.com/down.php?id=%s" % soft_id
                    print down_link
                    if is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=chksum
                        )
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results                    

class AnzowPosition(PositionSpider):
    """
    下载次数：否
    """
    domain = "www.anzow.com"
    search_url = "http://www.anzow.com/Search.shtml?stype=anzow&q=%s"
    xpath = "//div[@class='box boxsbg']//dd[@class='down_title']/h2/a"
    down_xpath = "//div[@class='contentdbtn']/a[@class='commentbtn']/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results


class ZhuodownPosition(PositionSpider):
    """
    下载次数：是
    位置:     信息页
    搜索：    高级搜索
    """
    domain = "www.zhuodown.com"
    charset = 'gb2312'
    search_url = (
        "http://www.zhuodown.com/plus/search.php"
        "?typeid=22"
        "&q=%s"
        "&starttime=-1"
        "&channeltype=0" 
        "&orderby=sortrank"
        "&pagesize=20"
        "&kwtype=1"
        "&searchtype=titlekeyword"
        "搜索=搜索"
    )
    xpath = "//div[@class='listbox']/ul[@class='e2']/li/a[2]"
    pagedown_xpath = "//ul[@class='downurllist']/a/@href"
    down_xpath = "//div[@class='advancedsearch']/table/tr[2]/td/li[1]/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link, title
            detail = self.get_elemtree(link)
            pagedown_link = detail.xpath(self.pagedown_xpath)[0]
            downdetail = self.get_elemtree(pagedown_link)
            down_link = downdetail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class Xz7Position(PositionSpider):
    """
    下载次数：否
    """
    domain = "www.7xz.com"
    search_url = "http://www.7xz.com/search?q=%s"
    xpath = "//a[@class='a2']"
    down_xpath = "//div[@class='downloadWrap1']/div[@class='diannao']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link,title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class WandoujiaPosition(PositionSpider):
    """
    下载次数：否
    备选：    安装量
    位置：    信息页
    """
    domain = "www.wandoujia.com"
    search_url = "http://www.wandoujia.com/search?key=%s"
    xpath = "//ul[@id='j-search-list']/li[@class='card']/div[@class='app-desc']/a"
    down_xpath = "//div[@class='download-wp']/a/@href"

    def run(self, appname, chksum=None, is_accurate=True):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link,title
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

class Android159Position(PositionSpider):
    """
    下载次数：是
    位置:     信息页
    搜索：    应用和游戏分类搜索
    机客网安卓市场
    """
    domain = "android.159.com"
    charset = 'gb2312'
    search_url = "http://2013.159.com/appshop/appsoftSearch.aspx?keyword=%s&MobleBrandTypeId=3170&submit=搜索"
    search_url1 = "http://2013.159.com/appshop/appgameSearch.aspx?keyword=%s&MobleBrandTypeId=3170&submit=搜索"
    xpath = "//div[@class='typecontent_title f14 appzp6 flod']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class Position3533(PositionSpider):
    """
    下载次数：否
    搜索：    应用、游戏、主题、壁纸分类搜索，结果页包含多种平台下载地址
    """
    domain = "www.3533.com"
    search_url = "http://search.3533.com/software?keyword=%s"
    search_url1 = "http://search.3533.com/game?keyword=%s"
    xpath = "//div[@class='applist']/ul/li//div[@class='appinfo']/a[@class='apptit']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class MuzisoftPosition(PositionSpider):
    """
    网站做得很烂，页面经常有错误
    """
    domain = "www.muzisoft.com"
    charset = 'gb2312'
    search_url = "http://www.muzisoft.com/plus/search.php?kwtype=0&q=%s&imageField.x=0&imageField.y=0"
    xpath = "//div[@class='searchitem']//dt/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class Position7613(PositionSpider):
    """
    下载次数：否
    搜索:     搜索结果不区分平台，无下载量
    """
    domain = "www.7613.com"
    charset = 'gb2312'
    search_url = "http://www.7613.com/search.asp?keyword=%s"
    xpath = "//table[@id='senfe']/tbody/tr/td[3]//a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class BaicentPosition(PositionSpider):
    """
    下载次数：是
    位置:     信息页
    搜索：    搜索结果不区分平台，类别杂乱，可选高级搜索
    """
    domain = "www.baicent.com"
    charset = 'gb2312'
    search_url = "http://www.baicent.com/plus/search.php?kwtype=0&q=%s&searchtype=title"
    xpath = "//div[@class='resultlist']/ul/li/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results


if __name__ == "__main__":
    #hiapk = HiapkPosition()
    #print hiapk.run(u'微信')

    #gfan = GfanPosition()
    #print gfan.run(u'微信')

    #apk91 = Apk91Position()
    #print apk91.run(u'微信')

    #angeeks = AngeeksPosition()
    #print angeeks.run(u'微信')
    
    #it168 = It168Position()
    #print it168.run(u'微信')

    #pchome = PcHomePosition()
    #print pchome.run(u'微信')

    #qq = QQPosition()
    #print qq.run(u'网易')

    #mumayi = MumayiPosition()
    #print mumayi.run(u'微信')
    #print mumayi.download_times(u'网易新闻 V4.0.1')

    #skycn = SkycnPosition()
    #print skycn.run(u'微信')
  
    #zol = ZolPosition()
    #print zol.run(u'网易')

    #pconline = PcOnlinePosition()
    #print pconline.run(u'腾讯')

    #sina = SinaPosition()
    #print sina.run(u'新浪')

    #duote = DuotePosition()
    #print duote.run(u'网易')

    #imobile = ImobilePosition()
    #print imobile.run(u'网易')

    #apkzu = ApkzuPosition()
    #print apkzu.run(u'网易')

    #nduoa = NduoaPosition()
    #print nduoa.run(u'资讯')

    #android115 = Android115Position()
    #print android115.run(u'网易')

    #shop985 = Shop985Position()
    #print shop985.run(u'网易')

    #liqucn = LiqucnPosition()
    #print liqucn.run(u'腾讯')

    #cnmo = CnmoPosition()
    #print cnmo.run(u'腾讯')

    #crsky = CrskyPosition()
    #print crsky.run(u'网易')
 
    #d = DPosition()
    #print d.run(u'网易')

    #androidcn = AndroidcnPosition()
    #print androidcn.run(u'qq')

    #apkcn = ApkcnPosition()
    #print apkcn.run(u'腾讯')

    #soho = SohoPosition()
    #print soho.run(u'捕鱼')

    #shouji = ShoujiPosition()
    #print shouji.run(u'腾讯')

    #mobile1 = Mobile1Position()
    #print mobile1.run(u'网易')

    #onlinedown = OnlineDownPosition()
    #print onlinedown.run(u'腾讯')

    #eoemarket = EoemarketPosition()
    #print eoemarket.run(u'腾讯')

    #borpor = BorPorPosition()
    #print borpor.run(u'网易')

    #apkol = ApkolPosition()
    #print apkol.run(u'腾讯')

    #bkill = BkillPosition()
    #print bkill.run(u'网易')

    #aibala = AibalaPosition()
    #print aibala.run(u'网易')

    #vmall = VmallPosition()
    #print vmall.run(u'有道')

    #yruan = YruanPosition()
    #print yruan.run(u'网易')

    #anzow = AnzowPosition()
    #print anzow.run(u'网易')

    #zhuodown = ZhuodownPosition()
    #print zhuodown.run(u'网易')

    #xz7 = Xz7Position()
    #print xz7.run(u'腾讯')

    wandoujia = WandoujiaPosition()
    print wandoujia.run(u'网易')

    #android159 = Android159Position()
    #print android159.run(u'qq')

    #p3533 = Position3533()
    #print p3533.run(u'网易')

    #muzisoft = MuzisoftPosition()
    #print muzisoft.run(u'网易')

    #p7613 = Position7613()
    #print p7613.run(u'腾讯')

    #baicent = BaicentPosition()
    #print baicent.run(u'腾讯')
