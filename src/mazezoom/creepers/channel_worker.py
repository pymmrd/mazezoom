# -*- coding:utf-8 -*-

#Author: zoug
#Email: b.zougang@gmail.com
#Date: 2014/08/18

#StdLib imports
import time

#Project imports
from channel import *
from constants import CHANNEL_TASK_KEY
from base import ChannelSpider
from backend import RedisBackend

INTERUPT = 1


def worker():
    backend = RedisBackend()
    while 1:
        task = backend.accept(CHANNEL_TASK_KEY)
        if task is not None:
            appname, appid, clsname = task
            cls = ChannelSpider.get(clsname, None)
            if cls is not None:
                instance = cls()
                instance.run()
        time.sleep(INTERUPT)

if __name__ == "__main__":
    worker()
