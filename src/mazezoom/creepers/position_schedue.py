# -*- coding:utf-8 -*-

#Author: zoug
#Email:b.zougang@gmail.com
#Date:2014/08/23


"""
渠道检测任务调度进程, 目前采用多进程方式进行任务执行
"""

#StdLib imports
import os
import time
import subprocess

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
WORKER_PATH = os.path.join(CURRENT_PATH, 'position_worker.py') 


INTERRUPT = 0.5
PROCESS_LIMIT = 5
POSITION_CMD = "python %s" % WORKER_PATH


def schedule(cmd):
    all_process = []
    while 1:
        if len(all_process) < PROCESS_LIMIT:
            p = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE
            )
            all_process.append(p)
        for index, process in enumerate(all_process):
            if process.poll() is not None:
                all_process.pop(index)
        time.sleep(INTERRUPT)


if __name__ == "__main__":
    schedule(POSITION_CMD)
