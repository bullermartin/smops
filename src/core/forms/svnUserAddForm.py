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
from core.models import host

class svnUserAddForm(forms.Form):
    '''
        定义一个用于SVN用户信息添加及修改的表单
    '''


    # hostList = []
    # for h in host.objects.all():
    #     tempHost = (h.id,h.name)
    #     hostList.append(tempHost)
    # hostList = tuple(hostList)

    name = forms.CharField(required=True,
                               max_length=20,
                               error_messages={
                                   'required':u'SVN名称不能为空',
                                   'max_length':u'用户名最大长度为20个字符',
                               })

    username = forms.CharField(required=True,
                               max_length=20,
                               error_messages={
                                   'required':u'用户名不能为空',
                                   'max_length':u'用户名最大长度为20个字符',
                               })

    password = forms.CharField(required=True,
                               max_length=30,
                               widget=forms.PasswordInput(),
                               error_messages={
                                   'required':u'密码不能为空',
                                   'max_length':u'密码最大长度为30个字符',
                               })

    host_id = forms.ModelChoiceField(required=True,
                                queryset=host.objects.all(),
                                error_messages={
                                'required':u'主机不能为空',
                            })

    # host_id = forms.CharField(required=True,
    #                             widget=forms.Select(choices=hostList),
    #                             error_messages={
    #                             'required':u'主机不能为空',
    #                         })

