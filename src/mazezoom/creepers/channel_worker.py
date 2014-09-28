# -*- coding:utf-8 -*-

#Author: zoug
#Email: b.zougang@gmail.com
#Date: 2014/08/18

#StdLib imports
import time
import json

#Project imports
from channel import *
from constants import CHANNEL_TASK_KEY
from base import ChannelSpider
from backend import RedisBackend

INTERUPT = 1


def update_first_status(pk):
    ChannelLink.objects.filter(pk=pk).update(is_first=False)


def worker():
    backend = RedisBackend()
    while 1:
        task = backend.accept(CHANNEL_TASK_KEY)
        if task is not None:
            loadtask = json.loads(task)
            length = len(loadtask)
            if length  == 7:
                #crontab dispatcher
                (channellink, app_uuid, app_version, url,
                    channel, title, clsname) = loadtask 
                is_first = False
            elif length == 8:
                (channellink, app_uuid, app_version, url,
                    channel, title, clsname, is_first) = loadtask 
            cls = ChannelSpider.subclass.get(clsname, None)
            if cls is not None:
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
                    if is_first:
                        update_first_status(channellink)
        time.sleep(INTERUPT)

if __name__ == "__main__":
    worker()
