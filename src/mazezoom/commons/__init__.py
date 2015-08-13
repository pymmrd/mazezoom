# -*- coding: utf-8 -*-
# Author: zougang
# Email: zougang@nagapt.com
# Date: 2015/02/04
# Copyright by NAGA Inc.

# StdLib imports
import os
import sys
import uuid
import math
import subprocess
from datetime import datetime, timedelta

# ThirdParty imports
import shortuuid

# Django Core imports
from django.conf import settings
from django.http import Http404


def unique_uuid():
    return str(uuid.uuid1())


def unique_suid():
    return shortuuid.uuid()


def get_today():
    return datetime.today()


def yesterday_and_tomorrow(d=None):
    if not d:
        today = get_today()
    else:
        today = d
    today = datetime(
        today.year,
        today.month,
        today.day
    )
    yesterday = today + timedelta(days=-1)
    tomorrow = today + timedelta(days=1)
    return yesterday, tomorrow


def date_path(prefix):
    today = get_today()
    date_dir = '%s/%s/%s/%s' % (
        prefix,
        today.strftime('%Y'),
        today.strftime('%m'),
        today.strftime('%d')
    )
    return date_dir


def protect_unique_path(taskid, prefix='protect'):
    date_subdir = date_path(prefix)
    protect_path = os.path.join(
        settings.MEDIA_ROOT,
        date_subdir,
        taskid,
    )
    if not os.path.exists(protect_path):
        os.makedirs(protect_path)
    return protect_path


def storage_path(filename, prefix='apkLogo'):
    date_subdir = date_path(prefix)
    sub_path = os.path.join(date_subdir, filename)
    date_dir = os.path.join(settings.MEDIA_ROOT, date_subdir)
    file_path = os.path.join(settings.MEDIA_ROOT, sub_path)
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    return file_path, sub_path


def get_filename(rawname):
    """
    具有文件后缀的文件名
    """
    _, ext = os.path.splitext(rawname)
    name = unique_uuid()
    if ext:
        name = '%s%s' % (
            name,
            ext
        )
    return name


def call_subprocess(cmd):
    linux_os = 'linux2'
    platform = sys.platform
    if platform == linux_os:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            close_fds=True,
        )
    else:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
    communicate = p.communicate()
    messages = communicate[0]
    return messages


def call_subprocess_returncode(cmd):
    linux_os = 'linux2'
    platform = sys.platform
    if platform == linux_os:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
            close_fds=True,
        )
    else:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
    communicate = p.communicate()
    messages = communicate[0]
    returncode = p.returncode
    return messages, returncode


def update_check_progress(created_date):
    """
    根据时间更新进度
    """
    now = datetime.now()
    stime = created_date
    delta = now - stime
    diff = int(math.ceil(float(delta.seconds)/20))

    if diff > 90:
        diff = 90

    progress = diff
    return progress


def getseo_object(page_index):
    from gandalf.models import SEO
    """
    获得seo对象
    """
    seo_index = page_index
    seo_object = SEO.objects.filter(
        page=seo_index,
    )
    return seo_object
