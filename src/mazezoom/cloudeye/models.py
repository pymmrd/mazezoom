# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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


class Application(models.Model):
    """
    应用
    """
    name = models.CharField(
        max_length=255,
        verbose_name=u'App名字'
    )
    
    user = models.ForeignKey(
        User,
        verbose_name='用户'
    )
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

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'创建日期',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=u'是否激活',
    )

    class Meta:
        db_table = 'application'

    def __unicode__(self):
        return self.name


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

    app = models.ForeignKey(
        Application,
        verbose_name=u'App'
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

    version = models.ForeignKey(
        AppVersion,
        verbose_name=u'版本'
        blank=True,
        null=True
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


    class Meta:
        db_table = 'channel'


    def __unicode__(self):
        return '%s--->%s' % (self.app.name, self.url)
