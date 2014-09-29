# -*- coding:utf-8 -*-

#StdLib imports
import json

#Project imports
from channel import *
from base import ChannelSpider
from backend import RedisBackend
from cloudeye.models import ChannelLink
from constants import CHANNEL_TASK_KEY


def dispatcher():
    #S1 取出所有的抓取链接
    values = (
        'id', 'app_id', 'version_id',
        'title', 'channel_id', 'url', 'channel__domain'
    )
    links = ChannelLink.objects.values(*values).all()
    backend = RedisBackend()
    #装饰并分发扫描任务到worker队列
    #[id, app_uuid, version_id, url, channel_id, title, clsname]
    for link in links:
        domain = link['channel__domain']
        cls = ChannelSpider.subclass.get(domain, None)
        if cls is not None:
            channellink = link['id']
            app_uuid = link['app_id']
            app_version = link['version_id']
            title = link['title']
            channel = link['channel_id']
            url = link['url']
            dumptask = json.dumps([
                channellink, app_uuid, app_version,
                url, channel, title, domain
            ])
            backend.send(CHANNEL_TASK_KEY, dumptask)

if __name__ == "__main__":
    dispatcher()
