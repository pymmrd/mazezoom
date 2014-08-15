# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'公司名字')

    tel = models.CharField(max_length=20, verbose_name=u'座机')

    mobile = models.CharField(max_length=11, verbose_name=u'手机')

    contact_user = models.CharField(max_length=100, verbose_name='联系人')

    remark = models.TextField(blank=True, verbose_name=u'备注')

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'company'


class Category(models.Model):
    """
    渠道和App类型
    """
    pass


class Application(models.Model):
    """
    应用
    """
    name = models.CharField(max_length=255, verbose_name=u'App名字')

    category = models.ForeignKey(Category, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)


class AppVersion(models.Model):
    """
    App 版本
    """
    app = models.ForeignKey(Application, verbose_name=u'App')

    version = models.CharField(max_length=50, verbose_name=u'版本')

    md5sum = models.CharField(max_length=64, verbose_name=u'md5值')

    created_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'appversion'


class Channel(models.Model):
    """
    渠道
    """
    VALID = 1
    INVALID = 2
    UNCERTAIN = 3
    AUDIT_CHOICES = (
        (VALID, u'有效的'),
        (INVALID, u'无效的'),
        (UNCERTAIN, u'不确定'),
    )

    app = models.ForeignKey(Application, verbose_name=u'App')

    url = models.CharField(max_length=255, verbose_name=u'地址')

    checksum = models.BigIntegerField(verbose_name=u'检验值',
                                      help_text=u'通过binascii的b2a_hex生成的校验值'
                                      )

    version = models.ForeignKey(AppVersion, verbose_name=u'版本')

    status = models.IntegerField(default=UNCERTAIN, choices=AUDIT_CHOICES)
