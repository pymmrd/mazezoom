# -*- coding:utf-8 -*-

from creepers.utils import datetime_range, get_yesterday
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

    def populate_channel_for_app(self, appversion, channel):
        appversion.channel.add(channel)

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
            version=app_version,
            checksum=checksum,
            defaults=kwargs
        )
        return link, is_created

    def get_or_create_appdetail(self, app_uuid, version, *args, **kwargs):
        detail, is_created = AppDetail.objects.get_or_create(
            app_uuid=app_uuid,
            app_version=version,
            **kwargs
        )
        #for key, value in kwargs.iteritems():
        #    setattr(detail, key, value)
        #detail.save()
        return detail, is_created

    def get_yesterday_dtimes(self, clink):
        yesterday = get_yesterday()
        start_date, end_date = datetime_range(yesterday)
        try:
            daily = AppDailyDownload.objects.get(
                channel_link=clink,
                created_date__gte=start_date,
                created_date__lt=end_date
            )
        except AppDailyDownload.DoesNotExist:
            download_times = 0
        else:
            download_times = daily.download_times
        return download_times

    def create_or_update_dailydownload(self, channellink, download_times, *args, **kwargs):
        start_date, end_date = datetime_range()
        yesterday_times = self.get_yesterday_dtimes(channellink)
        try:
            daily = AppDailyDownload.objects.get(
                channel_link=channellink,
                created_date__gte=start_date,
                created_date__lt=end_date
            )
        except AppDailyDownload.DoesNotExist:
            daily = AppDailyDownload()
        daily.channel_link = channellink
        daily.download_times = download_times
        daily.delta_times = download_times - yesterday_times
        for key, value in kwargs.iteritems():
            setattr(daily, key, value)
        daily.save()
