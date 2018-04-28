# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
import os

VERBOSE_APP_NAME = u"数据库"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class DatabaseConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME
