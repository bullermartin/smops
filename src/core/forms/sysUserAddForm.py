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
from core.UserProfile import *

class sysUserAddForm(forms.Form):
    '''
        定义一个用于系统用户信息的表单
    '''

    # userList = []
    # for u in UserProfile.objects.all():
    #     tempUser = (u.id,u.name)
    #     userList.append(tempUser)
    # userList = tuple(userList)

    # hostList = []
    # for h in host.objects.all():
    #     tempHost = (h.id,h.name)
    #     hostList.append(tempHost)
    # hostList = tuple(hostList)

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

    # host_id = forms.IntegerField(required=True,
    #                             widget=forms.Select(choices=hostList),
    #                             error_messages={
    #                             'required':u'主机不能为空',
    #                         })
    host_id = forms.ModelChoiceField(required=True,
                                     queryset=host.objects.all(),
                                     error_messages={
                                         'required':u'主机不能为空',
                                     })

    # user_id = forms.CharField(required=True,
    #                             widget=forms.Select(choices=userList),
    #                             error_messages={
    #                             'required':u'所有者不能为空',
    #                         })
