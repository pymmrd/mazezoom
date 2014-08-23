# -*- coding:utf-8 -*-
#Author: zoug
#Email:b.zougang@gmail.com
#Date:2014/08/23


"""
渠道下载次数,版本信息等抓取任务调度进程, 目前采用多进程方式进行任务执行.
为了简单方便分布式，采用单独脚本进行管理
"""

#StdLib imports
import time
import subprocess


INTERRUPT = 0.5
PROCESS_LIMIT = 5
CHANNEL_CMD = "python channel_worker.py"


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
    schedule(CHANNEL_CMD)
