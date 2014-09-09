# -*- coding:utf-8 -*-
from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=u'公司名字'
    )

    tel = models.CharField(
        max_length=20,
        verbose_name=u'座机'
    )

    mobile = models.CharField(
        max_length=11,
        verbose_name=u'手机'
    )

    contact_user = models.CharField(
        max_length=100,
        verbose_name='联系人'
    )

    remark = models.TextField(
        blank=True,
        verbose_name=u'备注'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'company'


class Category(models.Model):
    """
    渠道和App类型
    """
    title = models.CharField(
        u'标题',
        max_length=50,
        db_index=True,
        unique=True
    )

    slug = models.SlugField(
        u"标题(拼音)",
        max_length=50,
        db_index=True
    )

    parent = models.ForeignKey(
        'self',
        related_name='children',
        verbose_name=u'父分类',
        null=True,
        blank=True
    )

    ancestors = models.ManyToManyField(
        'self',
        symmetrical=False,
        editable=False,
        related_name="descendants",
        db_index=True,
        verbose_name=u'子分类'
    )

    level = models.IntegerField(
        verbose_name=u'等级',
        blank=True,
        default=0,
        db_index=True,
        editable=False
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = u"分类"
        db_table = 'category'
        ordering = ['slug']

    def path(self, seq=" > ", field="title"):
        path = [
            o[field]
            for o in self.ancestors.all().order_by('level').values(field)
        ]
        path.extend([getattr(self, field)])
        return seq.join(path)

    def _flatten(self, L):
        """
        Taken from a python newsgroup post
        """
        if not isinstance(L, list):
            return [L]
        if L == []:
            return L
        return self._flatten(L[0]) + self._flatten(L[1:])

    def _recurse_for_children(self, node, only_active=False):
        children = []
        children.append(node)
        for child in node.children.active():
            if child != self:
                children_list = self._recurse_for_children(
                    child,
                    only_active=only_active
                )
                children.append(children_list)
        return children

    def get_active_children(self, include_self=False):
        """
        Gets a list of all of the children
        categories which have active products.
        """
        return self.get_all_children(
            only_active=True,
            include_self=include_self
        )

    def get_all_children(self, only_active=False, include_self=False):
        """
        Gets a list of all of the children categories.
        """
        children_list = self._recurse_for_children(
            self,
            only_active=only_active
        )
        if include_self:
            ix = 0
        else:
            ix = 1
        flat_list = self._flatten(children_list[ix:])
        return flat_list

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p)
            if p != self:
                more = self._recurse_for_parents(p)
                p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def parents(self):
        return self._recurse_for_parents(self)

    def get_active_children_pk(self, include_self=False):
        children = self.get_active_children(include_self)
        childs = [obj.pk for obj in children]
        return childs

    @classmethod
    def top_level(self, *args, **kw):
        return self.objects.filter(
            is_active=True,
            parent__isnull=True,
            *args,
            **kw
        )

    def save(self, ancestors=None):
        if ancestors is None:
            ancestors = []
        if self.parent and self.id:
            assert self.parent not in self.descendants.all(), "prevent loop reference"

        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super(self.__class__, self).save()
        self.ancestors.clear()
        if self.parent:
            if not ancestors:
                ancestors = list(self.parent.ancestors.all())
                ancestors.extend([self.parent])
            self.ancestors.add(*ancestors)
        childs_ancestors = ancestors.extend([self, ])
        for child in self.children.all():
            child.save(ancestors=childs_ancestors)

    def __unicode__(self):
        return self.path()


class Channel(models.Model):
    """
    渠道
    """
    name = models.CharField(max_length=80)
    domain = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s--%s' % (self.name, self.domain)


class Application(models.Model):
    """
    应用
    DROP TABLE IF EXISTS `app_info`;
    CREATE TABLE `app_info` (
  `APP_UUID` varchar(36) NOT NULL DEFAULT '',
  `APP_MD5` varchar(32) NOT NULL,
  `APP_NAME` varchar(50) DEFAULT NULL,
  `APP_VERSION` varchar(50) DEFAULT NULL,
  `APP_USER` varchar(25) DEFAULT NULL,
  `FILE_NAME` varchar(100) NOT NULL,
  `APP_STATE` int(3) NOT NULL,
  `TASK_ID` varchar(36) DEFAULT NULL,
  `creat_time` date DEFAULT NULL,
  PRIMARY KEY (`APP_UUID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    """
    app_uuid = models.CharField(max_length=36, primary_key=True)
    app_md5 = models.CharField(max_length=32)
    app_name = models.CharField(max_length=50, null=True)
    app_version = models.CharField(max_length=50)
    app_user = models.CharField(max_length=25)
    file_name = models.CharField(max_length=100)
    app_state = models.IntegerField()
    task_id = models.CharField(max_length=36)
    creat_time = models.DateField()
    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        verbose_name=u'公司',
    )

    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        verbose_name=u'类别',
    )

    class Meta:
        db_table = 'app_info'

    def __unicode__(self):
        return self.app_name


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

    md5sum = models.CharField(
        max_length=64,
        verbose_name=u'md5值'
    )

    download_times = models.IntegerField(
        verbose_name=u'下载次数',
        default=0
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建日期'
    )

    status = models.IntegerField(
        default=UNCERTAIN,
        choices=AUDIT_CHOICES,
        verbose_name=u'状态',
    )

    class Meta:
        db_table = 'appversion'

    def __unicode__(self):
        return '%s---%s' % (self.app, self.version)


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
        help_text=u'当爬虫精确匹配时设置此属性为True')

    class Meta:
        db_table = 'channel'

    def __unicode__(self):
        return '%s--->%s' % (self.app.name, self.url)
