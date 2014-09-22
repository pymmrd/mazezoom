# -*- coding:utf-8 -*-

from datetime import datetime, timedelta

def get_yesterday(d=None):
    if d is None:
        d = datetime.now()
    yesterday = d - timedelta(days=1)
    return yesterday

def datetime_range(d=None):
    if d is None:
        today = datetime.now()
        start_date = datetime(
            today.year,
            today.month,
            today.day
        )
    else:
        start_date = datetime(
            d.year,
            d.month,
            d.day
        )
    end_date = start_date + timedelta(days=1)
    return start_date, end_date
