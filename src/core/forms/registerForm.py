# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: loginForm.py
@time: 2016/5/25 16:52
"""

from django import forms

class registerForm(forms.Form):
    '''
        定义一个用于用户登录的表单
    '''

    username = forms.CharField(required=True, error_messages={
                                'required':u'用户名不能为空',
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为10',
                            })
    name = forms.CharField(required=True,min_length=2, max_length=10, error_messages={
                                'required':u'用户名不能为空',
                                'min_length':u'最小长度为2',
                                'max_length':u'最大长度为10',
                            })
    password = forms.CharField(required=True, error_messages={
                                'required':u'用户名不能为空',
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为10',
                            })
    email = forms.EmailField(required=False,min_length=3, max_length=30, error_messages={
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为30',
                            })

    status = 0

