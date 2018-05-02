#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin
from django import forms

# Register your models here.
from django.db.models import Q

from database.models import Economics, EconomicsFields
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from sdata.settings import logger

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

from datetime import datetime
DEFAULT_START_YEAR = 1990
DEFAULT_END_YEAR = datetime.now().year

editable_fields = {
    'industrial_output': EconomicsFields.objects.filter(gid_zh=u'工业总产值（不变价、新规定）').first().gid,
    'staff_total_avg': EconomicsFields.objects.filter(gid_zh=u'全部职工（从业人员平均人数）').first().gid,
}


class IndustrialOutputSearch(forms.Form):
    operator_options = (
        ('', _("--")),
        ('gt', _("大于")),
        ('lt', _("小于"))
    )

    # 工业总产值过滤，IndustrialOutputSearch，以下简写为 ios
    ios_operator = forms.ChoiceField(label=_("工业总产值"), choices=operator_options, required=False)
    ios_amount = forms.CharField(label='', required=False)
    time_start = forms.IntegerField(label='年份从', required=False)
    time_end = forms.IntegerField(label='到', required=False)


class CommonAdmin(admin.ModelAdmin):
    # 默认排序
    ordering = ('id',)


class EconomicsAdmin(admin.ModelAdmin):

    # 定义admin总览里每行的显示信息，外键用特殊方法返回
    list_display = tuple(['year'] + sorted([v for k, v in focus_fields.iteritems()]))
    list_editable = tuple(sorted([v for k, v in editable_fields.iteritems()]))

    list_filter = tuple([focus_fields['city'], focus_fields['industry'], focus_fields['industry_code']])
    list_display_links = tuple([focus_fields['comp']])

    # 传入的需要是列表，设定过滤列表
    # list_filter = ('',)

    advanced_search_form = IndustrialOutputSearch(initial={'trs_start': DEFAULT_START_YEAR, 'trs_end': DEFAULT_END_YEAR})

    other_search_fields = {}

    # 定义搜索框以哪些字段可以搜索，例如username是在user表中，就用user__username的形式，这里需要注意下，不能直接用user表名，要用字段名，表名__字段名
    search_fields = ('year', 'g1012', 'g1111_1', 'g1411', 'g141101', 'g1511',)

    # 默认排序
    ordering = ('id', 'year')

    def lookup_allowed(self, lookup, value):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(EconomicsAdmin, self).lookup_allowed(lookup, value)

    def get_queryset(self, request):
        qs = super(EconomicsAdmin, self).get_queryset(request)
        # probably there is a better way to extract this value this is just
        # an example and depends on the type of the form field

        # 同时指定比较符号和数值时，过滤工业总产值
        ios_operator_value = self.other_search_fields.get("ios_operator", [""])[0]
        ios_amount_value = self.other_search_fields.get("ios_amount", [""])[0]
        time_start = self.other_search_fields.get("time_start", [DEFAULT_START_YEAR])[0]
        time_end = self.other_search_fields.get("time_end", [DEFAULT_END_YEAR])[0]
        if ios_operator_value and ios_amount_value:
            if ios_operator_value == 'gt':
                qs = qs.filter(g1911__gt=ios_amount_value, year__gte=time_start, year__lte=time_end)
            else:
                qs = qs.filter(g1911__lt=ios_amount_value, year__gte=time_start, year__lte=time_end)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):
        # we need to reset on every request otherwise it will survive and we
        # don't want that
        self.other_search_fields = {}
        # we now need to remove the elements coming from the form
        # and save in the other_search_fields dict but it's not allowed
        # to do that in place so we need to temporary enable mutability ( I don't think
        # it will cause any complicance but maybe someone more exeprienced on how
        # QueryDict works could explain it better)
        request.GET._mutable = True

        for key in self.advanced_search_form.fields.keys():
            try:
                temp = request.GET.pop(key)
            except KeyError:
                pass  # there is no field of the form in the dict so we don't remove it
            else:
                if temp != ['']:  # there is a field but it's empty so it's useless
                    self.other_search_fields[key] = temp

        request.GET_mutable = False

        self.advanced_search_form = IndustrialOutputSearch(initial={
            'ios_operator': self.other_search_fields.get("ios_operator", [""])[0],
            'ios_amount': self.other_search_fields.get("ios_amount", [""])[0],
            'time_start': self.other_search_fields.get("time_start", [DEFAULT_START_YEAR])[0],
            'time_end': self.other_search_fields.get("time_end", [DEFAULT_END_YEAR])[0]
        })

        extra_context = {
            'asf': self.advanced_search_form,
        }

        return super(EconomicsAdmin, self).changelist_view(request, extra_context=extra_context)


admin.site.register(Economics, EconomicsAdmin)
admin.site.register(EconomicsFields, CommonAdmin)
