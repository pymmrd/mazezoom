# -*- coding:utf-8 -*-
"""
    渠道检测任务daemon进程, 主要作用于监听渠道任务，分发渠道
    到'postion_task',任务队列中。
    此daemon进程用supervisord进行管理
"""

#StdLib imports
import time

#Project imports
from position import *
from base import PositionSpider
from backend import RedisBackend
from constants import POSITION_DISPATCH_KEY, POSITION_TASK_KEY


INTERUPT = 2


def dispatcher():
    """
    task:[id, appname, name]
    """
    backend = RedisBackend()
    while 1:
        #接受扫描任务
        task = backend.accept(POSITION_DISPATCH_KEY)
        if task is not None:
            #装饰并分发扫描任务到worker队列
            for item in PositionSpider.subclass.iterkeys():
                task.append(item)
                backend.send(POSITION_TASK_KEY, task)
        #添加CPU中端时间
        time.sleep(INTERUPT)


if __name__ == "__main__":
    dispatcher()
