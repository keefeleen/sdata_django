#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.db.models import Q

from database.models import Economics, EconomicsFields
from django.utils.safestring import mark_safe


# 我们只关心如下两个经济学数据中的字段
focus_fields = {
    'comp': EconomicsFields.objects.filter(gid_zh=u'企业名称').first().gid,
    'industrial_output': EconomicsFields.objects.filter(gid_zh=u'工业总产值（不变价、新规定）').first().gid,
    # 2013 年数据缺失
    'staff_total_avg': EconomicsFields.objects.filter(gid_zh=u'全部职工（从业人员平均人数）').first().gid,
    # 'total_salary': EconomicsFields.objects.filter(gid_zh=u'本年应付工资总额').first().gid,
    'city': EconomicsFields.objects.filter(gid_zh=u'hubei_dixian').first().gid,
    # 2013 年数据缺失
    # 'static_assets': EconomicsFields.objects.filter(gid_zh=u'固定资产合计').first().gid,
    # 'circulating_assets': EconomicsFields.objects.filter(gid_zh=u'流动资产合计').first().gid,
    'industry': EconomicsFields.objects.filter(gid_zh=u'hengyeleibie').first().gid,
    'industry_code': EconomicsFields.objects.filter(gid_zh=u'行业类别').first().gid,
    'register_code': EconomicsFields.objects.filter(gid_zh=u'登记注册类型').first().gid,
}

editable_fields = {
    'industrial_output': EconomicsFields.objects.filter(gid_zh=u'工业总产值（不变价、新规定）').first().gid,
    'staff_total_avg': EconomicsFields.objects.filter(gid_zh=u'全部职工（从业人员平均人数）').first().gid,
}


class CommonAdmin(admin.ModelAdmin):
    # 默认排序
    ordering = ('id',)


class EconomicsAdmin(admin.ModelAdmin):

    # 定义admin总览里每行的显示信息，外键用特殊方法返回
    list_display = tuple(['year'] + sorted([v for k, v in focus_fields.iteritems()]))
    list_editable = tuple(sorted([v for k, v in editable_fields.iteritems()]))

    list_filter = tuple([focus_fields['city'], focus_fields['industry'], focus_fields['industry_code']])
    list_display_links = tuple([focus_fields['comp']])
    # 定义搜索框以哪些字段可以搜索，例如username是在user表中，就用user__username的形式，这里需要注意下，不能直接用user表名，要用字段名，表名__字段名
    search_fields = ('year', 'g1012', 'g1111_1', 'g1411', 'g141101', 'g1511')
    # 传入的需要是列表，设定过滤列表
    # list_filter = ('',)

    # 默认排序
    ordering = ('id', 'year')

admin.site.register(Economics, EconomicsAdmin)
admin.site.register(EconomicsFields, CommonAdmin)
