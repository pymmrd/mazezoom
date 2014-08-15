# -*- coding:utf-8 -*-

#Django Core imports
from django.contrib import admin

#Project imports
from cloudeye.models import (App, Company, Category,
                             AppVersion, Channel)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'parent', 'level', 'is_active')
    search_fields = ['title']
    list_filter = ["is_active"]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel', 'mobile', 'is_active')
    search_fields = ["name"]
    list_filter = ["is_active"]


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'category', 'created_date', 'is_active') 
    search_fields = ('name', )
    raw_id_fields = ('company', 'category',)


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'md5sum', 'created_date', 'is_active')
    search_fields = ('md5sum',)
    list_filter = ["is_active"]
    inlines = [ChannelInlineAdmin,]


class ChannelInlineAdmin(admin.TabularInline):
    model = Channel
