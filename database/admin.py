#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from web.models import Product, Category, Banner, Page, News, Message, BrandShow
from django.utils.safestring import mark_safe


class CommonAdmin(admin.ModelAdmin):
    # 默认排序
    ordering = ('id',)
