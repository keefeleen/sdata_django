# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import os

import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# 用于包含图片的模型获取图片存储路径
from DjangoUeditor.models import UEditorField
from sdata.settings import logger


# 定义 Economics 对象:
class Economics(models.Model):

    # 表的结构:
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(verbose_name=u'年份')
    # 公司名称
    g1012 = models.TextField(verbose_name=u'公司名称')
    # 工业总产值
    g1911 = models.IntegerField(verbose_name=u'工业总产值', blank=True)
    # 企业人数
    g2515 = models.IntegerField(verbose_name=u'企业人数', blank=True)
    # 本年应付工资总额
    g2417 = models.IntegerField(verbose_name=u'本年应付工资总额', blank=True)
    # 地级市
    g1111_1 = models.TextField(verbose_name=u'地级市')
    # 流动资产
    g2111 = models.IntegerField(verbose_name=u'流动资产', blank=True)
    # 固定资产
    g2116 = models.IntegerField(verbose_name=u'固定资产', blank=True)
    # 行业代码
    g1411 = models.IntegerField(verbose_name=u'行业代码')
    # 行业名称
    g141101 = models.TextField(verbose_name=u'行业名称')
    # 登记注册类型
    g1511 = models.IntegerField(verbose_name=u'登记注册类型')
    # 统计出的土地使用面积预留字段
    g99999 = models.FloatField(verbose_name=u'土地使用面积', blank=True)
    # 是否标记为重要企业样例对象
    important = models.BooleanField(default=False, verbose_name=u'样本')

    class Meta:
        db_table = 'economics'
        verbose_name = u'工业企业经济数据'
        verbose_name_plural = u'经济数据'

    def __unicode__(self):
        return self.g1012


# 定义 EconomicsFields 对象:
class EconomicsFields(models.Model):

    # 表的结构:
    id = models.IntegerField(primary_key=True)
    gid = models.CharField(max_length=11)
    gid_zh = models.TextField()
    field_type = models.CharField(max_length=11)

    class Meta:
        db_table = 'economics_fields'
        verbose_name = u'工业企业经济数据字段'
        verbose_name_plural = u'经济数据字段'

    def __unicode__(self):
        return self.gid_zh
