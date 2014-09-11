# -*- coding:utf-8 -*-

from cloudeye.document import AppDetail, AppDailyDownload
from cloudeye.models import (Channel, ChannelLink, Application, AppVersion)


class ORMManager(object):

    def get_or_create_channel(self, name, domain, *args, **kwargs):
        channel, is_created = Channel.objects.get_or_create(
            name=name,
            domain=domain,
            defaults=kwargs
        )
        return channel, is_created

    def get_or_create_appversion(self, app, version, md5sum, *args, **kwargs):
        appversion, is_created = AppVersion.objects.get_or_create(
            app=app,
            version=version,
            md5sum=md5sum,
            defaults=kwargs,
        )
        return appversion, is_created

    def create_debug_app(self, app_uuid, md5sum, app_name,
                         app_version, app_user='3', filename='1',
                         app_state=1, task_id='1'):
        app = Application(
            app_uuid=app_uuid,
            app_md5=md5sum,
            app_name=app_name,
            app_version=app_version,
            app_user=app_user,
            file_name=filename,
            app_state=app_state,
            task_id=task_id,
        )
        app.save()
        return app

    def get_app(self, app_uuid):
        try:
            app = Application.objects.get(app_uuid=app_uuid)
        except Application.DoesNotExist:
            app = None
        return app

    def get_or_create_channellink(self, app, app_version,
                                  checksum, *args, **kwargs):
        link, is_created = ChannelLink.objects.get_or_create(
            app=app,
            app_version=app_version,
            checksum=checksum,
            defaults=kwargs
        )
        return link, is_created

    def create_appdetail(self, app_uuid, version, *args, **kwargs):
        try:
            detail = AppDetail.objects.get(app_uuid, app_version=version)
        except AppDetail.DoesNotExist:
            detail = AppDetail()
            detail.app_uuid = app_uuid
            detail.app_version = version

        for key, value in kwargs.iteritems():
            setattr(detail, key, value)
        detail.save()

    def create_dailydownload(self, app_uuid, app_version, *args, **kwargs):
        try:
            dailydownload = AppDailyDownload.objects.get(app_uuid, app_version)
        except AppDailyDownload.DoesNotExist:
            dailydownload = AppDailyDownload()
            dailydownload.app_uuid = app_uuid
            dailydownload.app_version = app_version

        for key, value in kwargs.iteritems():
            setattr(dailydownload, key, value)
        dailydownload.save()
