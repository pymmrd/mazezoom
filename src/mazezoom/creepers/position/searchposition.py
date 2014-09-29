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
    #abstract = True

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


class ApkcnPosition(PositionSpider):
    """
    下载次数：否
    备选：    无
    搜索：    post
    """
    #error 下载页面打不开
    name = u'安奇网'
    domain = "www.apkcn.com"
    search_url = "http://www.apkcn.com/search/"
    xpath = "//div[@class='box']/div[@class='post indexpost']/h3/a"
    down_xpath = "//div[@class='imginfo']/p[2]/a/@href"
    #abstract = True

    def position(self):
        results = []
        data = {'keyword': self.app_name.encode(self.charset), 'select': 'phone'}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
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
    #abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
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
    #abstract = True
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
    down_xpath = "//span[@class='adown']/strong/a/@href"

    def collect_link(self, source, items): 
        elems = []
        for item in items:
            link = self.normalize_url(source, item.attrib['href'])
            title = item.text_content().strip()
            if self.app_name in title:
                elems.append((link, title))
        return elems

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        etree2 = self.send_request(self.app_name, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        elems = self.collect_link(self.search_url, items)
        elems.extend(self.collect_link(self.search_url1, items2))
        if self.is_accurate:    #精确匹配
            for item in elems:
                link = item[0]
                title = item[1]
                detail = self.get_elemtree(link)
                down_link = detail.xpath(self.down_xpath)
                if down_link:
                    for dlink in down_link:
                        match = self.verify_app(down_link=dlink, chksum=self.chksum)
                        if match:
                            results.append((link, title))
        else:
            results = elems
        return results

#页面下载403
class Mobile1Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    json返回数据
    """
    #abstract = True
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
        return results

class OnlineDownPosition(PositionSpider):
    """
    下载次数：否
    备选：    人气数
    位置：    信息页
    排行列表页有下载量，搜索列表页无，结果页无
    """
    #abstract = True
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
            detail = self.get_elemtree(link)
            pagedown_link = detail.xpath(self.pagedown_xpath)[0]
            pagedown_link = self.normalize_url(link, pagedown_link)
            downdetail = self.get_elemtree(pagedown_link)
            down_link = downdetail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
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
    #abstract = True

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
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
    #abstract = True
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
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
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
    #abstract = True
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
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[-1]
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
    #abstract = True
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
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)[0]
            r = re.compile("window.location.href='(.+)';return false;")
            down_link = r.search(down_link)
            down_link = down_link.group(1)
            if down_link:
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


class VmallPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    华为开发者联盟-->华为应用市场
    """
    name = u'华为应用市场'
    domain = "app.vmall.com"
    search_url = "http://app.vmall.com/search/%s"
    base_xpath = "//div[@class='list-game-app dotline-btn nofloat']/div[@class='game-info whole']"
    #down_xpath = "//a[@class='mkapp-btn mab-download']/@onclick"
    down_xpath = "child::div[@class='app-btn']/a/@onclick"
    link_xpath = "child::h4/a"

    def position(self):
        results = []
        etree = self.send_request(self.app_name)
        items = etree.xpath(self.base_xpath)
        for item in items:
            elem = item.xpath(self.link_xpath)[0]
            link = elem.attrib['href']
            title = item.text_content().strip()
            #detail = self.get_elemtree(link)
            if self.app_name in title:
                if self.is_accurate:    #精确匹配
                    down_link_raw = item.xpath(self.down_xpath)[0]
                    if down_link_raw:
                        down_link_raw = down_link_raw[0]
                        regx = re.compile("'(http://appdl\.hicloud\.com/[^']+)'")
                        down_link = regx.search(down_link_raw)
                        down_link = down_link.group(1)
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

class YruanPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索:     搜索结果不区分平台
    """
    #abstract = True
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
                detail = self.get_elemtree(link)
                pagedown_link = detail.xpath(self.down_xpath)[0]
                if pagedown_link is not None:
                    r = re.compile("id=([0-9]+)&")
                    soft_id = r.search(pagedown_link)
                    soft_id = soft_id.group(1)
                    down_link = "http://www.yruan.com/down.php?id=%s" % soft_id
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
    下载次数：有
    """
    #abstract = True
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
            detail = self.get_elemtree(link)
            down_link = detail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
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
    #abstract = True
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
            detail = self.get_elemtree(link)
            pagedown_link = detail.xpath(self.pagedown_xpath)[0]
            downdetail = self.get_elemtree(pagedown_link)
            down_link = downdetail.xpath(self.down_xpath)
            if down_link:
                down_link = down_link[0]
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
    #abstract = True
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
        return results

#error 下载页面乱码，无正常内容显示
class MuzisoftPosition(PositionSpider):
    """
    网站做得很烂，页面经常有错误
    """
    #abstract = True
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
        return results

if __name__ == "__main__":
    androidcn = AndroidcnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #androidcn.run()
    apkcn = ApkcnPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #apkcn.run()
    soho = SohoPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    #soho.run()
    shouji = ShoujiPosition(
        u'水果忍者',
        app_uuid=1,
        version='1.9.5',
        chksum='d603edae8be8b91ef6e17b2bf3b45eac'
    )
    shouji.run()
    '''
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
