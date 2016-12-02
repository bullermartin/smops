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

class hostAddForm(forms.Form):
    '''
        定义一个用于添加主机的表单
    '''
    statusList = (
        (0,'运行'),
        (1,'停止')
    )

    name = forms.CharField(required=True,
                           min_length=3,
                            max_length=20,
                            widget=forms.TextInput(),
                            error_messages={
                                'required':u'主机名不能为空',
                                'min_length':u'最小长度为3',
                                'max_length':u'最大长度为20',
                            })
    desc = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'rows':5, 'cols':50}),
                            max_length=255,
                            error_messages={
                                'max_length':u'最大长度为255',
                            })
    ipaddr = forms.GenericIPAddressField(required=True,
                                        protocol='IPv4',
                                        error_messages={
                                            'required':u'缺少IP地址',
                                        })
    prefix = forms.IntegerField(required=False,
                                min_value=1,
                                max_value=32,
                                error_messages={
                                    'min_value':u'掩码不合法',
                                    'min_value':u'掩码不合法',
                                })
    port = forms.IntegerField(required=False,
                            min_value=20,
                            max_value=65535,
                            error_messages={
                                'min_value':u'端口不合法',
                                'max_value':u'端口不合法',
                            })
    status = forms.CharField(required=True,
                            widget=forms.Select(choices=statusList),
                            error_messages={
                                'required':u'状态不能为空',
                            })

