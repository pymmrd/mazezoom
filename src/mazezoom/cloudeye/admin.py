# -*- coding:utf-8 -*-

#Django Core imports
from django.contrib import admin

#Project imports
from cloudeye.models import (Application, Company, Category,
                             AppVersion, Channel, ChannelLink)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'parent', 'level', 'is_active')
    search_fields = ['title']
    list_filter = ["is_active"]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel', 'mobile', 'is_active')
    search_fields = ["name"]
    list_filter = ["is_active"]


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'creat_time', ) 
    search_fields = ('app_name', )


class ChannelInlineAdmin(admin.TabularInline):
    model = Channel


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'md5sum', 'created_date',)
    search_fields = ('md5sum',)
    inlines = [ChannelInlineAdmin,]


class ChannelLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(AppVersion, AppVersionAdmin)
admin.site.register(ChannelLink, ChannelLinkAdmin)

