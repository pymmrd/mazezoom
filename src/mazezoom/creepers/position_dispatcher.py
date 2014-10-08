# -*- coding:utf-8 -*-
"""
    渠道检测任务daemon进程, 主要作用于监听渠道任务，分发渠道
    到'postion_task',任务队列中。
    此daemon进程用supervisord进行管理
"""

#StdLib imports
import time
import json
import logging

#Project imports
from position import *
from base import PositionSpider
from django.conf import settings
from backend import RedisBackend
from constants import POSITION_DISPATCH_KEY, POSITION_TASK_KEY


INTERUPT = 2

logger = logging.getLogger(settings.POSITION_DISPATCH_LOG_TYPE)




def dispatcher():
    """
    task:[app_uuid, appname, version, chksum]
    """
    backend = RedisBackend()
    while 1:
        #接受扫描任务
        rawtask = backend.accept(POSITION_DISPATCH_KEY)
        if rawtask:
            msg = 'Task:%s' % rawtask.decode('utf-8')
            logger.info(msg)
            task = rawtask.split(',')
            appname = task[1].decode(settings.DEFAULT_CHARSET)
            task[1] = appname
            if task is not None:
                #装饰并分发扫描任务到worker队列
                #[app_uuid, appname, version, chksum, clsname]
                for item in PositionSpider.subclass.iterkeys():
                    real_task = task[:]
                    real_task.append(item)
                    dumptask = json.dumps(real_task)
                    backend.send(POSITION_TASK_KEY, dumptask)
        #添加CPU中端时间
        time.sleep(INTERUPT)


if __name__ == "__main__":
    dispatcher()
