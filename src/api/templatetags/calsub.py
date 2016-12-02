# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: calsub.py
@time: 2016/4/27 16:11
"""

from django import template

register = template.Library()
def calsub(value, arg):
    try:
        arg = int(arg)
        value = int(value)
        return value - arg
    except:
        return 'error'

register.filter(calsub)  #注册过滤器
