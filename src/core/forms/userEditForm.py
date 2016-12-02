# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: userEditForm.py
@time: 2016/5/27 11:54
"""

from django import forms

class userEditForm(forms.Form):
    '''
        定义一个用于用户信息修改的表单
    '''

    statusList = (
            (0, u'正常'),
            (1, u'关闭')
    )

    name = forms.CharField(required=True,
                                min_length=3,
                                max_length=20,
                                error_messages={
                                'required':u'姓名不能为空',
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为20',
                            })
    password1 = forms.CharField(required=False,
                                min_length=3,
                                max_length=20,
                                widget=forms.PasswordInput,
                                error_messages={
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为20',
                            })
    password2 = forms.CharField(required=False,
                                min_length=3,
                                max_length=20,
                                widget=forms.PasswordInput(),
                                error_messages={
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为20',
                            })
    email = forms.EmailField(required=True,
                            min_length=3,
                            max_length=30,
                            error_messages={
                                'required':u'邮箱地址不能为空',
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为30',
                            })

    status = forms.IntegerField(required=True,
                                widget=forms.Select(choices=statusList),
                                error_messages={
                                    'required': u'用户状态不能为空',
                                })

    desc = forms.CharField(required=False,
                            max_length=255,
                            widget=forms.Textarea,
                            error_messages={
                                'max_length':u'最大长度为255',
                            })

