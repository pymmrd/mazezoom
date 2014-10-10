# -*- coding:utf-8 -*-

#StdLib imports
import time
import json

#Project imports
from channel import *
from base import ChannelSpider
from backend import RedisBackend
from cloudeye.models import ChannelLink
from constants import CHANNEL_TASK_KEY


REALTIME_WORKER_INTERCEPT = 5 * 60


def worker():
    subclass = ChannelSpider.subclass
    values = (
        'id', 'app_id', 'version_id',
        'title', 'channel_id', 'url', 'channel__domain'
    )
    is_first = 1
    backend = RedisBackend()
    while 1:
        links = ChannelLink.objects.values(*values).filter(is_first=True)
        for link in links:
            domain = link['channel__domain']
            cls = subclass.get(domain, None)
            if cls is not None:
                channellink = link['id']
                app_uuid = link['app_id']
                app_version = link['version_id']
                title = link['title']
                channel = link['channel_id']
                url = link['url']
                dumptask = json.dumps([
                    channellink, app_uuid, app_version,
                    url, channel, title, domain, is_first
                ])
                backend.send(CHANNEL_TASK_KEY, dumptask)
        time.sleep(REALTIME_WORKER_INTERCEPT)


if __name__ == "__main__":
    worker()
