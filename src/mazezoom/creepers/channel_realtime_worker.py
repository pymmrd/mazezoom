# -*- coding:utf-8 -*-

import time
from base import ChannelSpider
from channel import *
from cloudeye.models import ChannelLink


REALTIME_WORKER_INTERCEPT = 5 * 60


def update_first_status(pk):
    ChannelLink.objects.filter(pk=pk).update(is_first=False)


def worker():
    subclass = ChannelSpider.subclass
    values = (
        'id', 'app_id', 'version_id',
        'title', 'channel_id', 'url', 'channel__domain'
    )
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
                instance = cls(
                    channellink=channellink,
                    app_uuid=app_uuid,
                    app_version=app_version,
                    url=url,
                    channel=channel,
                    title=title
                )
                try:
                    instance.run()
                except:
                    pass
                else:
                    update_first_status(channellink)
        time.sleep(REALTIME_WORKER_INTERCEPT)


if __name__ == "__main__":
    worker()
