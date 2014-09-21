# -*- coding:utf-8 -*-

"""
MONGODB 数据存储scheme
"""
from datetime import datetime
from mongoengine import *


class AppDetail(Document):
    app_version = IntField(
        verbose_name=u'App 版本主键唯一ID'
    )

    app_uuid = StringField(
        verbose_name=u'APP uuid'
    )

    human_version = StringField(
        verbose_name=u'版本'
    )

    size = StringField(
        verbose_name='大小'
    )

    language = StringField(
        verbose_name=u'语言'
    )

    authorize = StringField(
        verbose_name=u'授权'
    )

    update_time = StringField(
        verbose_name=u'更新时间',
        help_text=u'页面上抓取的更新时间'
    )

    env = StringField(
        verbose_name=u'运行环境'
    )

    company = StringField(
        verbose_name=u'开发公司'
    )

    category = StringField(
        verbose_name=u'类别'
    )

    modify_time = DateTimeField(
        verbose_name=u'修改时间',
        help_text=u'爬虫修改时间',
        default=datetime.now,
    )


class AppDailyDownload(Document):
    app_uuid = StringField(
        verbose_name=u'app唯一主键uuid'
    )

    app_version = IntField(
        verbose_name=u'版本主键唯一ID'
    )

    channel_link = IntField(
        verbose_name=u'渠道链接ID',
        help_text=u'渠道链接的主键ID'
    )

    channel = IntField(
        verbose_name=u'渠道',
        help_text=u'渠道站点的主键ID'
    )

    channel_name = StringField(
        verbose_name=u'渠道名字'
    )

    download_times = IntField(
        verbose_name=u'当日下载次数'
    )

    delta_times = IntField(
        verbose_name=u'增量下载次数'
    )

    created_date = DateTimeField(
        verbose_name=u'抓取时间'
	auto_now=True
    )
