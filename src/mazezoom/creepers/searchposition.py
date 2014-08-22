# -*- coding:utf-8 -*-

import json
from base import PositionSpider

class HaipkPosition(PositionSpider):
    domain = "apk.haipk.com"
    search_url = "http://apk.hiapk.com/search?key=%s"
    xpath = "//span[@class='list_title font12']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class GfanPosition(PositionSpider):
    """
    下载次数：否
    备选：    评分次数
    位置：    信息页
    """
    domain = "apk.gfan.com"
    search_url = "http://apk.gfan.com/search?q=%s"
    xpath = "//span[@class='apphot-tit']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class Apk91Position(PositionSpider):
    """
    下载次数：否
    备选：    好评差评次数
    位置：    信息页
    搜索：    分类搜索
    """
    domain = "apk.gfan.com"
    search_url = "http://apk.91.com/soft/android/search/1_5_0_0_%s"
    search_url1 = "http://apk.91.com/game/android/search/1_5_%s"
    xpath = "//div[@class='zoom']/h4/a"

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

class AngeeksPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "apk.angeeks.com"
    charset = 'gb2312'
    search_url = "http://apk.angeeks.com/search?keywords=%s&x=0&y=0"
    xpath = "//div[@class='info']/a"

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

class It168Position(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    结果不区分平台
    """
    domain = "down.it168.com"
    charset = 'gb2312'
    search_url = "http://down.it168.com/soft_search.html?keyword=%s"
    xpath = "//div[@class='r3']/ul/li/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class PcHomePosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    搜索：    不区分平台
    """
    domain = "download.pchome.net"
    #charset = 'gbk'
    search_url = "http://download.pchome.net/search-%s---0-1.html"
    xpath = "//div[@class='tit']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class QQPosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    Json,Ajax,目前搜索结果只能取到前10个
    """
    domain = "sj.qq.com"
    search_url = "http://sj.qq.com/myapp/searchAjax.htm?kw=%s&pns=&sid="
    detail_url = "http://sj.qq.com/myapp/detail.htm?apkName=%s"

    def run(self, appname):
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
            results.append((link, title))
            print link, title
        return results

class MumayiPosition(PositionSpider):
    """
    下载次数：是
    位置：    列表页
    """
    domain = "android.mumayi.com"
    search_url = "http://s.mumayi.com/index.php?q=%s"
    xpath = "//ul[@class='applist']//h3[@class='hidden']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

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

class DuotePosition(PositionSpider):
    """
    下载次数：是(人气)
    位置：    信息页
    """
    domain = "www.duote.com"
    charset = 'gb2312'
    search_url = "http://www.duote.com/searchPhone.php?searchType=&so=%s"
    xpath = "//div[@class='list_item']/div[@class='tit_area']/span[@class='name']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class ImobilePosition(PositionSpider):
    """
    下载次数：是
    位置：    信息页
    """
    domain = "www.imobile.com.cn"
    search_url = "http://app.imobile.com.cn/android/search/%s.html"
    xpath = "//ul[@class='ranking_list']/li/div[@class='ico']/h3/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
        return results

class Shop985Position(PositionSpider):
    """
    搜索结果没有区分平台
    """
    domain = "d.958shop.com"
    charset = 'gb2312'
    search_url = "http://d.958shop.com/search/?keywords=%s&cn=soft"
    xpath = "//span[@class='t_name01']/a[@class='b_f']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class LiqucnPosition(PositionSpider):
    """
    根据Cookie或者referer来区别用户手机系统
    """
    domain = "www.liqucn.com"
    android_referer = 'http://os-android.liqucn.com/'
    search_url = "http://search.liqucn.com/download/%s"
    xpath = "//li[@class='appli_info']/a"

    def run(self, appname):
        results = []
        headers = {'Referer': self.android_referer}
        etree = self.send_request(appname, headers=headers)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            results.append((link, title))
        return results

class CrskyPosition(PositionSpider):
    """
    搜索结果比页面展示条目要少
    """
    domain = "www.crsky.com"
    charset = 'gb2312'
    search_url = "http://sj.crsky.com/query.aspx?keyword=%s&type=android"
    xpath = "//div[@class='right']//a"

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

class DPosition(PositionSpider):
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
    应用、游戏、资讯、壁纸、主题使用不同二级域名
    列表页与结果页下载次数不一致
    """
    domain = "www.androidcn.com"
    search_url = "http://down.androidcn.com/search/q/%s"
    xpath = "//div[@class='app-info']/h2/a"

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

class ApkcnPosition(PositionSpider):
    domain = "www.apkcn.com"
    search_url = "http://www.apkcn.com/search/"
    xpath = "//div[@class='box']/div[@class='post indexpost']/h3/a"

    def run(self, appname):
        results = []
        data = {'keyword': appname.encode(self.charset), 'select': 'all'}
        etree = self.send_request(data=data)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class SohoPosition(PositionSpider):
    domain = "download.sohu.com"
    search_url = "http://download.sohu.com/search?words=%s"
    xpath = "//div[@class='yylb_box']/div[@class='yylb_main']/p[@class='yylb_title']/strong/a"

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

class ShoujiPosition(PositionSpider):
    """
    应用和游戏分类搜索，域名不同，无下载次数
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

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        etree2 = self.send_request(appname, url=self.search_url1)
        items = etree.xpath(self.xpath)
        items2 = etree2.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        for item in items2:
            link = self.normalize_url(self.search_url1, item.attrib['href'])
            title = item.text_content()
            results.append((link, title))
            print link, title
        return results

class Mobile1Position(PositionSpider):
    """
    json返回数据
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
    xpath = "//div[@class='title']/strong/a"

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

class EoemarketPosition(PositionSpider):
    domain = "www.eoemarket.com"
    search_url = "http://www.eoemarket.com/search_.html?keyword=%s&pageNum=1"
    xpath = "//ol[@class='RlistName']/li[1]/span/a"

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

class ApkolPosition(PositionSpider):
    """
    结果页打开慢，安装次数
    """
    domain = "www.apkol.com"
    search_url = "http://www.apkol.com/search?keyword=%s"
    xpath = "//div[@class='listbox ty']/div[@class='yl_pic']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.attrib['title']
            results.append((link, title))
            print link, title
        return results

class BkillPosition(PositionSpider):
    domain = "www.bkill.com"
    charset = 'gb2312'
    search_url = "http://www.bkill.com/d/search.php?mod=do&n=1"
    xpath = "//div[@class='clsList']/dl/dt/a"

    def run(self, appname):
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
            results.append((link, title))
            print link, title
        return results

class AibalaPosition(PositionSpider):
    """
    关注数，列表页与结果页不一致
    """
    domain = "www.aibala.com"
    search_url = "http://www.aibala.com/android-search-1-0-0-%s-1-1"
    xpath = "//ul[@class='block']/li//div[@class='tabRightTL']/a"

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

class VmallPosition(PositionSpider):
    """
    华为开发者联盟-->华为应用市场
    """
    domain = "app.vmall.com"
    search_url = "http://app.vmall.com/search/%s"
    xpath = "//div[@class='list-game-app dotline-btn nofloat']/div[@class='game-info  whole']/h4[@class='title']/a"

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

class YruanPosition(PositionSpider):
    """
    搜索结果不区分平台
    """
    domain = "www.yruan.com"
    search_url = "http://www.yruan.com/search.php?keyword=%s"
    xpath = "//span[@class='item_name']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link,title
            results.append((link, title))
        return results

class AnzowPosition(PositionSpider):
    """
    无下载量
    """
    domain = "www.anzow.com"
    search_url = "http://www.anzow.com/Search.shtml?stype=anzow&q=%s"
    xpath = "//div[@class='box boxsbg']//dd[@class='down_title']/h2/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link,title
            results.append((link, title))
        return results

class Xz7Position(PositionSpider):
    """
    无下载量
    """
    domain = "www.7xz.com"
    search_url = "http://www.7xz.com/search?q=%s"
    xpath = "//a[@class='a2']"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = self.normalize_url(self.search_url, item.attrib['href'])
            title = item.text_content()
            print link,title
            results.append((link, title))
        return results

class WandoujiaPosition(PositionSpider):
    """
    安装次数
    """
    domain = "www.wandoujia.com"
    search_url = "http://www.wandoujia.com/search?key=%s"
    xpath = "//ul[@id='j-search-list']/li[@class='card']/div[@class='app-desc']/a"

    def run(self, appname):
        results = []
        etree = self.send_request(appname)
        items = etree.xpath(self.xpath)
        for item in items:
            link = item.attrib['href']
            title = item.text_content()
            print link,title
            results.append((link, title))
        return results

class Android159Position(PositionSpider):
    """
    机客网安卓市场
    应用和游戏分类搜索
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
    应用、游戏、主题、壁纸分类搜索，无下载量，列表页不区分平台，结果页包含多种平台下载地址
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
    搜索结果不区分平台，无下载量
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
    搜索结果不区分平台，类别，杂乱
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
    #haipk = HaipkPosition()
    #print haipk.run(u'微信')

    #gfan = GfanPosition()
    #print gfan.run(u'微信')

    #apk91 = Apk91Position()
    #print apk91.run(u'微信')

    #angeeks = AngeeksPosition()
    #print angeeks.run(u'刀塔')
    
    #it168 = It168Position()
    #print it168.run(u'微信')

    #pchome = PcHomePosition()
    #print pchome.run(u'微信')

    #qq = QQPosition()
    #print qq.run(u'网易')

    #mumayi = MumayiPosition()
    #print mumayi.run(u'微信')

    #skycn = SkycnPosition()
    #print skycn.run(u'微信')
  
    #zol = ZolPosition()
    #print zol.run(u'网易')

    #sina = SinaPosition()
    #print sina.run(u'新浪')

    #duote = DuotePosition()
    #print duote.run(u'网易')

    #imobile = ImobilePosition()
    #print imobile.run(u'微信')

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

    #crsky = CrskyPosition()
    #print crsky.run(u'腾讯')
 
    #d = DPosition()
    #print d.run(u'网易')

    #androidcn = AndroidcnPosition()
    #print androidcn.run(u'腾讯')

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

    #xz7 = Xz7Position()
    #print xz7.run(u'腾讯')

    #wandoujia = WandoujiaPosition()
    #print wandoujia.run(u'网易')

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
