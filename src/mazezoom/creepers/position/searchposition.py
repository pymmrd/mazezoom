# -*- coding:utf-8 -*-

#Author:chenyu
#Date:2014/08/24
#Email:chenyuxxgl@126.com

import re
import json
import time

if __name__ == '__main__':
    import os
    import sys
    current_path = os.path.abspath(os.path.dirname(__file__))
    creepers_path = os.path.abspath(os.path.dirname(current_path))
    sys.path.append(creepers_path)
from base import PositionSpider


class HiapkPosition(PositionSpider):
    """
    下载次数：否(搜索页面3.92千万热度)
    备选：    热度/评分次数
    位置：    信息页
    """
    name = u'安卓市场'
    domain = "apk.hiapk.com"
    search_url = "http://apk.hiapk.com/search?key=%s"
    xpath = "//span[@class='list_title font12']/a"
    down_xpath = "//a[@class='link_btn']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            detail = self.get_elemtree(link)
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(link, down_link)
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
            else:
                results.append((link, title))
        return results


class GfanPosition(PositionSpider):
    """
    下载次数：否
    备选：    评分次数
    位置：    信息页
    """
    name = u'机锋市场'
    domain = "apk.gfan.com"
    search_url = "http://apk.gfan.com/search?q=%s"
    xpath = "//span[@class='apphot-tit']/a"
    down_xpath = "//a[@id='computerLoad']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
            if self.app_name in title:
                if self.is_accurate:    # 精确匹配
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
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
    name = u'安卓下载'
    domain = "apk.91.com"
    search_url = "http://apk.91.com/soft/android/search/1_5_0_0_%s"
    search_url1 = "http://apk.91.com/game/android/search/1_5_%s"
    xpath = "//div[@class='zoom']/h4/a"
    down_xpath = "//a[@class='s_btn s_btn4']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(
            self.app_name,
            url=self.search_url1
        )
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(
                self.search_url,
                item.attrib['href']
            )
            title = item.text_content()
            if self.app_name in title:
                if self.is_accurate:    # 精确匹配

                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(
                            self.search_url,
                            down_link
                        )

                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
            else:
                results.append((link, title))
        return results


class It168Position(PositionSpider):
    """
    下载次数：是(d)
    位置：    信息页
    搜索：    结果不区分平台
    """
    name = u'IT168软件下载'
    domain = "down.it168.com"
    charset = 'gb2312'
    suffix = u'.apk'
    search_url = "http://down.it168.com/soft_search.html?keyword=%s"
    xpath = "//div[@class='r3']/ul/li/h3/a"
    down_xpath = "//li[@class='sign11 four_li1']/a/@href"
    android_tokens = ['android', u'安卓版']
    ios_tokens = ['iphone', 'ipad']

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content().strip()
            low_title = title.lower()

            #准确验证andorid
            isbreak = False
            for token in self.ios_tokens:
                if token in low_title:
                    isbreak = True
                    break

            if isbreak:
                continue

            is_android = False
            for token in self.android_tokens:
                if token in low_title:
                    is_android = True
                    break

            if is_android:
                if self.is_accurate:  # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class QQPosition(PositionSpider):
    """
    下载次数：是(d, s)
    位置：    信息页
    搜索：    Json,Ajax,目前搜索结果只能取到前10个
    """
    name = u'应用宝'
    domain = "sj.qq.com"
    search_url = (
        "http://sj.qq.com/myapp/"
        "searchAjax.htm?kw=%s&pns=&sid="
    )
    detail_url = (
        "http://sj.qq.com/myapp/"
        "detail.htm?apkName=%s"
    )
    down_xpath = (
        "//div[@class='det-ins-btn-box']/"
        "a[@class='det-down-btn']/@data-apkurl"
    )

    def position(self):
        results = []
        quote_app = self.quote_args(self.app_name)
        url = self.search_url % quote_app
        content = self.get_content(url)
        output = json.loads(content)
        appList = output.get('obj', {}).get('appDetails', [])
        for app in appList:
            link = self.detail_url % app.get('pkgName', '')
            title = app.get('appName', '')
            #downcount = app['appDownCount']
            if self.app_name in title:
                if self.is_accurate:  # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results


class MumayiPosition(PositionSpider):
    """
    下载次数：是(S)
    位置：    列表页
    """
    name = u'木蚂蚁应用市场'
    domain = "android.mumayi.com"
    search_url = "http://s.mumayi.com/index.php?q=%s"
    xpath = "//ul[@class='applist']//h3[@class='hidden']/a"
    times_xpath = (
        "//ul[@class='appattr hidden']/"
        "li[@class='num']/text()"
    )
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
            try:
                times = item.split(seperator)[-1]
            except (TypeError, IndexError, ValueError):
                pass
        return times

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.attrib['title']
            if self.app_name in title.lower():
                if self.is_accurate:    # 精确匹配
                    detail = self.get_elemtree(link)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class ZolPosition(PositionSpider):
    """
    多版本现象
    下载次数：是
    位置：    信息页
    """
    name = u'ZOL手机应用'
    domain = "sj.zol.com.cn"
    charset = 'gbk'
    search_url = "http://xiazai.zol.com.cn/search?wd=%s&type=1"
    xpath = (
        "//ul[@class='results-text']/li[@class='item']/"
        "div[@class='item-header clearfix']/a"
    )
    down_xpath = (
        #"//ul[@class='download-items']/li[@class='item'][1]"
        "//a[@class='downLoad-button androidDown-button']/@href"
    )
    token = 'sj.zol.com.cn'
    iphone_token = ['iphone', 'ipad']

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            low_title = title.lower()
            if self.token in link and self.app_name in title:
                is_continue = False
                for itoken in self.iphone_token:
                    if itoken in low_title:
                        is_countinue = True
                        break
                if is_continue:
                    continue
                if self.is_accurate:
                    detail = self.get_elemtree(link)
                    #onclick = detail.xpath(self.down_xpath)[0]
                    #r = re.compile("corpsoft\('([^']+)','\d+'\)")
                    #onclick_content = r.search(onclick)
                    #down_link = onclick_content.group(1)
                    down_link = detail.xpath(self.down_xpath)
                    if down_link:
                        down_link = down_link[0]
                        down_link = self.normalize_url(link, down_link)
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
                else:
                    results.append((link, title))
        return results


class PcOnlinePosition(PositionSpider):
    """
    下载次数：是(s,d)
    位置：    信息页
    """
    name = u'太平洋电脑网'
    domain = "dl.pconline.com.cn"
    charset = 'gb2312'
    search_url = ("http://ks.pconline.com.cn/download.shtml"
                 "?q=%s"
                 "&downloadType=Android%%CF%%C2%%D4%%D8")    # %%表示%
    xpath = "//a[@class='aTitle']"
    down_xpath = "//a[@class='btn sbDownload']/@tempurl"

    def get_pid(self, url):
        pid_url = url.rsplit('/', 1)
        pid = pid_url[-1].split('.')[0]
        return pid

    def get_token(self, url):
        token = None
        token_url = "http://dlc2.pconline.com.cn/dltoken/%s_genLink.js"
        pid = self.get_pid(url)
        token_url = token_url % pid
        content = self.send_request(url=token_url, tree=False)
        regx = re.compile('\((?P<token>.+)\)')
        match = regx.search(content.strip())
        if match is not None:
            token = match.group('token')
        return token

    def download_link(self, url):
        down_link = None
        token = self.get_token(url)
        if token is not None:
            detail = self.get_elemtree(url)
            dlink = detail.xpath(self.down_xpath)
            if dlink:
                dlink = dlink[0]
                print dlink
                items = dlink.rsplit('/', 1)
                down_link = '%s/%s/%s' % (items[0], token, items[1]) 
        return down_link

    def position(self):
        results = []
        data = {}
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            if self.app_name in title: 
                if self.is_accurate:    #精确匹配
                    headers = {'Host': self.domain, 'Referer': link}
                    self.update_request_headers(headers)
                    down_link = self.download_link(link)
                    if down_link:
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
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
    name = u'新浪科技'
    domain = "tech.sina.com.cn"
    charset = 'gb2312'
    search_url = "http://down.tech.sina.com.cn/3gsoft/iframelist.php?classid=0&keyword=%s&tag=&osid=4"
    xpath = "//div[@class='b_txt']/h3/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
    name = u'2345软件大全'
    domain = "www.duote.com"
    charset = 'gb2312'
    search_url = "http://www.duote.com/searchPhone.php?searchType=&so=%s"
    xpath = "//div[@class='list_item']/div[@class='tit_area']/span[@class='name']/a"
    down_xpath = "//div[@class='btn_trig'][1]/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'手机之家'
    domain = "www.imobile.com.cn"
    search_url = "http://app.imobile.com.cn/android/search/%s.html"
    xpath = "//ul[@class='ranking_list']/li/div[@class='ico']/h3/a"
    down_xpath = "//div[@class='download_install']/a[@class='download']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'安族网'
    domain = "www.apkzu.com"
    charset = 'gb2312'
    search_url = "http://www.apkzu.com/search.asp?k=%s&c=1"
    search_url1 = "http://www.apkzu.com/search.asp?k=%s&c=2"
    xpath = "//div[@class='recList']/div[@class='recSinW btmLine1']/dl/dt/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
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
    name = u'N多网'
    domain = "www.nduoa.com"
    search_url = "http://www.nduoa.com/search?q=%s"
    xpath = "//ul[@class='apklist clearfix']//div[@class='name']/a"
    title_xpath = "child::span[1]/text()"
    down_xpath = "//a[@id='BDTJDownload']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'手游天下'
    domain = "www.155.cn"
    charset = 'gb2312'
    search_url = "http://android.155.cn/search.php?kw=%s&index=soft"
    xpath = "//ul[@class='gmc-c']/li/strong/a"
    down_xpath = "//a[@class='down']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error 下载页面跳转过多
class Shop958Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    分类搜索，搜索结果没有区分平台
    """
    name = u'百信手机下载中心'
    domain = "d.958shop.com"
    charset = 'gb2312'
    search_url = "http://d.958shop.com/search/?keywords=%s&cn=soft"
    #search_url1 = "http://d.958shop.com/search/?keywords=%s&cn=game"    #游戏下载页面跳转3次
    xpath = "//span[@class='t_name01']/a[@class='b_f']"
    os_token = 'Android'
    platform_xpath = "//table[@class='m_word']/tr[6]/td/a/text()"
    #info_xpath = "child::td//text()"
    down_xpath = "//div[@class='todown1']/a[1]/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        #etree2 = self.send_request(self.app_name, url=self.search_url1)
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

                    if self.is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
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
    name = u'历趣'
    domain = "www.liqucn.com"
    android_referer = 'http://os-android.liqucn.com/'
    search_url = "http://search.liqucn.com/download/%s"
    xpath = "//li[@class='appli_info']/a"
    down_xpath = "//a[@id='content_mobile_href']/@href"
    os_token = 'os-android'

    def position(self):
        results = []
        headers = {'Referer': self.android_referer}
        etree = self.send_request(self.app_name, headers=headers)
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
                    if self.is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
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
    name = u'手机中国'
    domain = "www.cnmo.com"
    charset = 'gb2312'
    search_url = "http://app.cnmo.com/search/c=a&s=%s&p=2&f=1"    #p=2代表Android平台
    xpath = "//ul[@class='ResList']/li/div[@class='Righttitle'][1]/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
    name = u'非凡软件站'
    domain = "www.crsky.com"
    charset = 'gb2312'
    search_url = "http://sj.crsky.com/query.aspx?keyword=%s&type=android"
    xpath = "//div[@class='right']//a"
    down_xpath = "//div[@class='btns']/ul/li/a/@href"

    def position(self):
        results = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                   'Refererhttp': 'http://sj.crsky.com/query.aspx?keyword=%cd%f8%d2%d7&type=android'}
        etree = self.send_request(self.app_name, headers=headers)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'当乐网'
    domain = "www.d.cn"
    search_url = "http://android.d.cn/search/app/?keyword=%s"
    xpath = "//p[@class='g-name']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
    name = u'安卓中国'
    domain = "www.androidcn.com"
    search_url = "http://down.androidcn.com/search/q/%s"
    search_url1 = "http://game.androidcn.com/search/q/%s"
    xpath = "//h2/a"
    down_xpath = "//p[@class='dl-add-3']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
                print down_link
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'安奇网'
    domain = "www.apkcn.com"
    search_url = "http://www.apkcn.com/search/"
    xpath = "//div[@class='box']/div[@class='post indexpost']/h3/a"
    down_xpath = "//div[@class='imginfo']/p[2]/a/@href"

    def position(self):
        results = []
        data = {'keyword': self.app_name.encode(self.charset), 'select': 'phone'}
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'搜狐应用中心'
    domain = "download.sohu.com"
    search_url = "http://download.sohu.com/search?words=%s"
    xpath = "//div[@class='yylb_box']/div[@class='yylb_main']/p[@class='yylb_title']/strong/a"
    down_xpath = "//div[@class='gy_03 clear']/div[2]/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'手机乐园'
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

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
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
                if self.is_accurate:    #精确匹配
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
                if self.is_accurate:    #精确匹配
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
    name = u'1Mobile'
    domain = "www.1mobile.tw"
    search_url = "http://www.1mobile.tw/index.php?c=search.json&keywords=%s&page=1"

    def position(self):
        results = []
        quote_app = self.quote_args(self.app_name)
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
    name = u'华军软件园'
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

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'优亿市场'
    domain = "www.eoemarket.com"
    search_url = "http://www.eoemarket.com/search_.html?keyword=%s&pageNum=1"
    xpath = "//ol[@class='RlistName']/li[1]/span/a"
    down_xpath = "//div[@class='detailsright']/ol/li[1]/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'安卓在线'
    domain = "www.apkol.com"
    search_url = "http://www.apkol.com/search?keyword=%s"
    xpath = "//div[@class='listbox ty']/div[@class='yl_pic']/a"
    down_xpath = "//div[@content]/div[@class='cn_btn']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'比克尔下载'
    domain = "www.bkill.com"
    charset = 'gb2312'
    search_url = "http://www.bkill.com/d/search.php?mod=do&n=1"
    xpath = "//div[@class='clsList']/dl/dt/a"
    down_xpath = "//div[@class='down_link_main']/ul/li/a/@href"

    def position(self):
        results = []
        data = {
            'keyword': self.app_name.encode(self.charset),
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'android软件分享社区'
    domain = "www.aibala.com"
    search_url = "http://www.aibala.com/android-search-1-0-0-%s-1-1"
    xpath = "//ul[@class='block']/li//div[@class='tabRightTL']/a"
    down_xpath = "//div[@class='listMainRightBottomL']/div[@class='RightB1']/a[1]/@onclick"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'华为应用市场'
    domain = "app.vmall.com"
    search_url = "http://app.vmall.com/search/%s"
    xpath = "//div[@class='list-game-app dotline-btn nofloat']/div[@class='game-info  whole']/h4[@class='title']/a"
    down_xpath = "//a[@class='mkapp-btn mab-download']/@onclick"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'亿软网'
    domain = "www.yruan.com"
    search_url = "http://www.yruan.com/search.php?keyword=%s"
    xpath = "//span[@class='item_name']/a"
    token = 'Android'
    down_xpath = "//li[@class='downimg']/div[@class='down_link']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                    if self.is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
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
    name = u'安卓软件园'
    domain = "www.anzow.com"
    search_url = "http://www.anzow.com/Search.shtml?stype=anzow&q=%s"
    xpath = "//div[@class='box boxsbg']//dd[@class='down_title']/h2/a"
    down_xpath = "//div[@class='contentdbtn']/a[@class='commentbtn']/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'捉蛋网'
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

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
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
    name = u'豌豆荚'
    domain = "www.wandoujia.com"
    search_url = "http://www.wandoujia.com/search?key=%s"
    xpath = "//ul[@id='j-search-list']/li[@class='card']/div[@class='app-desc']/a"
    down_xpath = "//div[@class='download-wp']/a/@href"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
                if self.is_accurate:    #精确匹配
                    match = self.verify_app(
                        down_link=down_link,
                        chksum=self.chksum
                    )
                    if match:
                        results.append((link, title))
                else:
                    results.append((link, title))
        return results

#error js生成下载链接
class Android159Position(PositionSpider):
    """
    下载次数：是
    位置:     信息页
    搜索：    应用和游戏分类搜索
    机客网安卓市场
    """
    name = u'机客网安卓市场'
    domain = "android.159.com"
    charset = 'gb2312'
    search_url = "http://2013.159.com/appshop/appsoftSearch.aspx?keyword=%s&MobleBrandTypeId=3170&submit=搜索"
    search_url1 = "http://2013.159.com/appshop/appgameSearch.aspx?keyword=%s&MobleBrandTypeId=3170&submit=搜索"
    xpath = "//div[@class='typecontent_title f14 appzp6 flod']/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        items.extend(items2)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

#error 下载页面乱码，无正常内容显示
class MuzisoftPosition(PositionSpider):
    """
    网站做得很烂，页面经常有错误
    """
    name = u'木子ROM'
    domain = "www.muzisoft.com"
    charset = 'gb2312'
    search_url = "http://www.muzisoft.com/plus/search.php?kwtype=0&q=%s&imageField.x=0&imageField.y=0"
    xpath = "//div[@class='searchitem']//dt/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

#error 只能迅雷下载
class Position7613(PositionSpider):
    """
    下载次数：否
    搜索:     搜索结果不区分平台，无下载量
    """
    name = u'软件下吧'
    domain = "www.7613.com"
    charset = 'gb2312'
    search_url = "http://www.7613.com/search.asp?keyword=%s"
    xpath = "//table[@id='senfe']/tbody/tr/td[3]//a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
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
    name = u'百分网'
    domain = "www.baicent.com"
    charset = 'gb2312'
    #search_url = "http://www.baicent.com/plus/search.php?kwtype=0&q=%s&searchtype=title"
    search_url = ("http://www.baicent.com/plus/search.php"
                  "?typeid=304"
                  "&q=%s"
                  "&starttime=-1"
                  "&channeltype=0"
                  "&orderby=sortrank"
                  "&pagesize=20"
                  "&kwtype=1"
                  "&searchtype=titlekeyword"
                  "&搜索=搜索"
                 )
    xpath = "//div[@class='resultlist']/ul/li/h3/a"
    fuzzy_xpath = "//div[@class='viewbox']/div[@class='infolist']/span/text()"
    down_xpath = "//ul[@class='downurllist']/li[1]/a/@href"
    os_token = 'Android'

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
            info = detail.xpath(self.fuzzy_xpath)
            if self.os_token in info:
                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    down_link = down_link[0]
                    down_link = self.normalize_url(link, down_link)
                    if self.is_accurate:    #精确匹配
                        match = self.verify_app(
                            down_link=down_link,
                            chksum=self.chksum
                        )
                        if match:
                            results.append((link, title))
                    else:
                        results.append((link, title))
        return results



if __name__ == "__main__":
    hiapk = HiapkPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #hiapk.run()

    gfan = GfanPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #gfan.run()

    apk91 = Apk91Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #apk91.run()

    it168 = It168Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #it168.run()

    qq = QQPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #qq.run()

    mumayi = MumayiPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #mumayi.run()
    zol = ZolPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #zol.run()

    pconline = PcOnlinePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    pconline.run()

    '''
    sina = SinaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    sina.run()

    duote = DuotePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    duote.run()

    mobile = ImobilePosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    imobile.run()

    apkzu = ApkzuPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    apkzu.run()
    nduoa = NduoaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    nduoa.run()
    android115 = Android115Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    android115.run()
    shop958 = Shop958Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    shop958.run()

    liqucn = LiqucnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    liqucn.run()

    cnmo = CnmoPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    cnmo.run()

    crsky = CrskyPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    crsky.run()
 
    d = DPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    d.run()
    androidcn = AndroidcnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    androidcn.run()
    apkcn = ApkcnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    apkcn.run()
    soho = SohoPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    soho.run()
    下载需要cookie
    shouji = ShoujiPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    shouji.run()
    mobile1 = Mobile1Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    mobile1.run()
    onlinedown = OnlineDownPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    onlinedown.run()
    eoemarket = EoemarketPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    eoemarket.run()
    网站巨慢，detail无法打开
    apkol = ApkolPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    apkol.run()
    bkill = BkillPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    bkill.run()
    aibala = AibalaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    aibala.run()
    vmall = VmallPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    vmall.run()

    yruan = YruanPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    yruan.run()

    anzow = AnzowPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    anzow.run()

    zhuodown = ZhuodownPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    zhuodown.run()

    xz7 = Xz7Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    xz7.run()

    wandoujia = WandoujiaPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    wandoujia.run()

    android159 = Android159Position(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    android159.run()

    p3533 = Position3533(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    p3533.run()

    muzisoft = MuzisoftPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    muzisoft.run()

    p7613 = Position7613(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    p7613.run()

    baicent = BaicentPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    baicent.run()
    '''
