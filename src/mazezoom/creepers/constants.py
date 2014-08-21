# -*- coding:utf-8 -*-
import os

USER_AGENTS = [
   ("Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) "
    "Gecko/20071127 Firefox/2.0.0.11"),
   ("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) "
     "Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"),
    'Opera/9.25 (Windows NT 5.1; U; en)',
]


MAX_RETRY_TIMES = 3

DEFAULT_CHARSET = 'utf-8'

APP_DIR = os.path.abspath(os.path.dirname(__file__)) 

POSITION_APP_DIR = os.path.join(APP_DIR, 'position')

CHANNAL_APP_DIR = os.path.join(APP_DIR, 'channel')

