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
from core.models import host, svn_user

class businessEditForm(forms.Form):
    '''
        定义一个用于添加业务的表单
    '''
    statusList = (
        (0, u'正常'),
        (1, u'停止'),
    )

    name = forms.CharField(required=True,
                           min_length=3,
                            max_length=20,
                            widget=forms.TextInput(),
                            error_messages={
                                'required':u'业务名不能为空',
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为20',
                            })
    status = forms.IntegerField(required=True,
                            widget=forms.Select(choices=statusList),
                            error_messages={
                                'required':u'状态不能为空',
                            })
    directory = forms.CharField(required=True,
                            min_length=1,
                            max_length=255,
                            error_messages={
                                'required':u'业务目录不能为空',
                                'max_length':u'最大长度为255',
                            })
    svn_dir = forms.CharField(required=True,
                            min_length=1,
                            max_length=255,
                            error_messages={
                                'required':u'SVN目录不能为空',
                                'max_length':u'最大长度为255',
                            })
    running_user = forms.CharField(required=True,
                                    min_length=3,
                                    max_length=20,
                                    error_messages={
                                        'required':u'运行账户不能为空',
                                        'min_length':u'最小长度为3',
                                        'max_length':u'最大长度为20',
                                    })
    svn_user = forms.ModelChoiceField (required=True,
                                        queryset=svn_user.objects.all(),
                                        widget=forms.Select(attrs={'style':"width:135px",}),
                                        error_messages={
                                            'required':u'SVN账户不能为空',
                                    })
    host = forms.ModelMultipleChoiceField(required=True,
                                          widget=forms.SelectMultiple(attrs={'size':8, 'style':"width:150px"}),
                                          queryset=host.objects.all(),
                                          error_messages = {
                                              'required':u'主机不能为空',
                                          })