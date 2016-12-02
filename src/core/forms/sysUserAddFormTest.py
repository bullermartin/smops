# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: sysUserAddFormTest.py
@time: 2016/7/15 13:47
"""
from django import forms
from core.UserProfile import *

class sysUserAddFormTest(forms.Form):
    '''
        定义一个用于系统用户信息的表单
    '''
    username = ''
    # userAllowedAll = []
    userList = []

    user_id = forms.IntegerField(required=True,
                            widget=forms.Select(choices=userList),
                            error_messages={
                            'required':u'所有者不能为空',
                        })
    def __init__(self, username,*args,**kwargs):
        super(sysUserAddFormTest, self).__init__(*args,**kwargs)
        # sysUserAddFormTest.username = username
        userAllowedAll = []
        if username == 'admin':
            self.userAllowedAll = UserProfile.objects.all()
        else:
            self.userAllowedAll = UserProfile.objects.filter(username=username)
        __userList = []
        for u in self.userAllowedAll:
            tempUser = (u.id, u.name)
            __userList.append(tempUser)
        self.userList = tuple(__userList)

        self.user_id.widget = forms.Select(choices=(('1',1),('2',2)))