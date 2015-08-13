# -*- coding:utf-8 -*-
from django.db import models


# Create your models here.
class Channel(models.Model):
    """
    渠道
    """
    name = models.CharField(max_length=80, verbose_name=u'渠道名字')
    domain = models.CharField(max_length=200, verbose_name=u'渠道域名')
    created_date = models.DateTimeField(auto_now=True, verbose_name=u'创建日期')
    is_active = models.BooleanField(default=True, verbose_name=u'是否激活')

    def __unicode__(self):
        return '%s--%s' % (self.name, self.domain)

    class Meta:
        db_table = 'channel'

    def __unicode__(self):
        return self.name


class Application(models.Model):
    #app_uuid = models.CharField(max_length=36, primary_key=True)
    #app_md5 = models.CharField(max_length=32)
    #app_name = models.CharField(max_length=50, null=True)
    #app_version = models.CharField(max_length=50)
    #app_user = models.CharField(max_length=25)
    #file_name = models.CharField(max_length=100)
    #app_state = models.IntegerField()
    #task_id = models.CharField(max_length=36)
    #creat_time = models.DateField(auto_now=True)
    """
    上传的需加固文件
    """
    # 文件mimetype
    ANDROID = 1
    SO = 2
    ZIP = 3
    ANDROID_FILE_TYPE = "application/vnd.android.package-archive"
    ZIP_FILE_TYPE = "application/zip"
    SO_FILE_TYPE = "application/octet-stream"

    MIME_MAP = {
        ANDROID_FILE_TYPE: ANDROID,
        SO_FILE_TYPE: SO,
        ZIP_FILE_TYPE: ZIP,
    }

    MIME_TYPES = (
        (ANDROID, u'Android APK'),
        (SO, u'so文件'),
        (ZIP, u'zip文件'),
    )

    raw_name = models.CharField(
        verbose_name=u'上传文件名',
        max_length=225,
        blank=True,
    )

    name = models.CharField(
        verbose_name=u'名称',
        max_length=225,
        blank=True,
    )

    package_name = models.CharField(
        verbose_name=u'包名',
        max_length=50,
        blank=True,
    )

    version = models.CharField(
        verbose_name=u'版本',
        max_length=15,
        blank=True,
    )

    icon = models.ImageField(
        verbose_name=u'图标',
        upload_to='apkLogo/%Y/%m/%d',
        blank=True
    )

    storage = models.FileField(
        verbose_name=u'存储路径',
        upload_to='apkUpload/%Y/%m/%d/%H/%M',
        max_length=200,
        blank=True
    )

    md5sum = models.CharField(
        verbose_name=u'md5值',
        max_length=32
    )

    size = models.CharField(
        max_length=20,
        verbose_name=u'文件大小',
        blank=True,
    )

    created_date = models.DateTimeField(
        verbose_name=u'创建时间',
        auto_now_add=True
    )

    mime_type = models.IntegerField(
        verbose_name=u'文件类型',
        choices=MIME_TYPES,
        default=ANDROID,
    )

    rsa_md5sum = models.CharField(
        verbose_name=u'RSA值',
        blank=True,
    )

    is_active = models.BooleanField(
        verbose_name=u'是否激活',
        default=True,
    )

    class Meta:
        db_table = 'file'
        verbose_name = u'上传文件'
        verbose_name_plural = u'上传文件'

    def __unicode__(self):
        return '%s--->%s' % (
            self.pk,
            self.name or self.package_name
        )


class AppVersion(models.Model):
    """
    App 版本
    """
    VALID = 1
    INVALID = 2
    UNCERTAIN = 3

    AUDIT_CHOICES = (
        (VALID, u'有效的'),
        (INVALID, u'无效的'),
        (UNCERTAIN, u'不确定'),
    )

    app = models.ForeignKey(
        Application,
        verbose_name=u'App'
    )

    version = models.CharField(
        max_length=50,
        verbose_name=u'版本'
    )

    channel = models.ManyToManyField(Channel,
        blank=True,
        null=True
    )

    md5sum = models.CharField(
        max_length=64,
        verbose_name=u'md5值'
    )

    download_times = models.BigIntegerField(
        verbose_name=u'下载次数',
        default=0
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建日期'
    )

    status = models.IntegerField(
        default=VALID,
        choices=AUDIT_CHOICES,
        verbose_name=u'状态',
    )

    class Meta:
        db_table = 'appversion'

    def __unicode__(self):
        return '%s---%s' % (self.app.app_name, self.version)


class ChannelLink(models.Model):
    """
    App所在渠道地址
    """

    UNCERTAIN = NOBODY = 0
    VALID = ADMIN = 1
    INVALID = SPIDER = 2

    AUDITOR = (
        (ADMIN, u'管理员'),
        (SPIDER, u'爬虫'),
        (NOBODY, u'没有审核'),
    )

    AUDIT_CHOICES = (
        (UNCERTAIN, u'不确定'),
        (VALID, u'有效'),
        (INVALID, u'无效'),
    )

    app = models.ForeignKey(
        Application,
        verbose_name=u'App'
    )

    version = models.ForeignKey(
        AppVersion,
        verbose_name=u'版本',
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'标题',
        help_text=(
            u'app所在渠道链接上的标题，'
            u'保存以供在搜索结果页面获得下载次数'
        )
    )

    channel = models.ForeignKey(
      Channel,
      verbose_name=u'渠道',
    )

    url = models.CharField(
        max_length=255,
        verbose_name=u'地址'
    )

    checksum = models.BigIntegerField(
        db_index=True,
        verbose_name=u'检验值',
        help_text=u'通过binascii的b2a_hex生成的校验值'
    )

    auditor = models.IntegerField(
        choices=AUDITOR,
        default=SPIDER,
        verbose_name=u'审核者',
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建日期',
    )

    status = models.IntegerField(
        default=UNCERTAIN,
        choices=AUDIT_CHOICES,
        verbose_name=u'状态',
    )

    is_accurate = models.BooleanField(
        default=True,
        verbose_name=u'是否精确匹配',
        help_text=u'当爬虫精确匹配时设置此属性为True'
    )

    download_times = models.BigIntegerField(
        blank=True,
        null=True
    )

    is_first = models.BooleanField(
        default=True,
        verbose_name=u'是否第一次入库',
        help_text=u'首次入库链接，进行实时抓取'
    )

    class Meta:
        db_table = 'channellink'

    def __unicode__(self):
        return '%s--->%s' % (self.app.app_name, self.url)
