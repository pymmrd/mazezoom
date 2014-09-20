# -*- coding:utf-8 -*-
#Author: zoug
#Email: b.zougang@gmail.com
#Date: 2014/08/18

#StdLib imports
import time

#Project imports
from position import *
from base import PositionSpider
from constants import POSITION_TASK_KEY
from backend import RedisBackend

INTERUPT = 1


def worker():
    backend = RedisBackend()
    while 1:
        task = backend.accept(POSITION_TASK_KEY)
        if task is not None:
            app_uuid, appname, version, chksum, clsname = task
            cls = PositionSpider.get(clsname, None)
            if cls is not None:
                instance = cls(
                    appname,
                    app_uuid=app_uuid,
                    version=version,
                    chskum=chksum
                )
                instance.run()
        time.sleep(INTERUPT)

if __name__ == "__main__":
    worker()
