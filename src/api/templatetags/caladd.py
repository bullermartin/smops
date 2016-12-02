# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: caladd.py
@time: 2016/4/27 16:11
"""

from django import template

register = template.Library()
def caladd(value, arg):
    try:
        value = int(value)
        arg = int(arg)
        return value + arg
    except:
        return 'error'

register.filter(caladd)  #注册过滤器
