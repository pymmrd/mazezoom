# -*- coding:utf-8 -*-

from position import *
from channel import *
from searchposition import *
from base import PositionSpider, ChannelSpider

INTERRUPT = 0.5
PROCESS_LIMIT = 2
POSITION_CMD = "python position_worker.py" 
CHANNEL_CMD  = "python channel_worker.py"


position_sites = PositionSpider.subclass
channel_sites = ChannelSpider.subclass

def schedule():
    count = 0
    all_process = []
    cmd_list = []
    while 1:
        if len(all_process) < PROCESS_LIMIT:
            try:
                cmd = cmd_list.pop(count)
            except IndexError:
                break
            else:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                all_process.append(p)
        for index, process in enumerate(all_process):
            if process.poll() is not None:
                all_process.pop(index)
        time.sleep(INTERRUPT)

