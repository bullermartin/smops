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

class whitelistAddForm(forms.Form):
    '''
        定义一个用于添加白名单的表单
    '''
    ipaddr = forms.GenericIPAddressField(required=True,
                                        protocol='ipv4',
                                        error_messages={
                                            'required':u'IP地址不能为空',
                                            'protocol':u'IP地址不合法，仅支持ipv4',
                                        })
    prefix = forms.IntegerField(required=False,
                                min_value=1,
                                max_value=24,
                                error_messages={
                                    'min_value':u'掩码不合法',
                                    'max_value':u'掩码不合法',
                                })
    desc = forms.CharField(required=True,
                            min_length=1,
                            max_length=255,
                            error_messages={
                                'required':u'描述不能为空',
                                'min_length':u'最小长度为1',
                                'max_length':u'最大长度为255',
                            })

