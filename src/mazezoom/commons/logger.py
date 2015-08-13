# -*- coding:utf-8 -*-
# Author: zougang
# Email: zougang@nagapt.com
# Date: 2015/03/05
# Copyright by NAGA

# StdLib imports
import logging


def logger_constructor(log_file, logname='protect'):
    logger = logging.getLogger(logname)
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        '[%(asctime)s]%(filename)s-%(process)d-%(thread)d-%(lineno)d-%(levelname)8s-"%(message)s"',
        '%Y-%m-%d %a %H:%M:%S'
    )
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger
