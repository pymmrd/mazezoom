# -*- coding:utf-8 -*-

from production import *

try:
    from development import *
except ImportError:
    pass
