# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: user_ops.py
@time: 2016/5/27 11:31
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from core.decorators import requireLogin
from core.forms.userEditForm import userEditForm
from core.forms.userAddForm import userAddForm
from core.UserProfile import *
import json

# 所有的数据库操作应该添加对应日志记录
@requireLogin
def userOperator(request):
    '''
        处理运维用户信息相关操作
    '''
    # 处理添加用户操作
    if request.GET.get('ac') == 'add':
        data = {}
        if request.method == 'GET':
            userFormObj =userAddForm()
            return render(request, 'pages/useradd.html', {'userFormObj':userFormObj})
        elif request.method == 'POST':
            userFormObj =userAddForm(request.POST or None)
            if userFormObj.is_valid():
                userObj = UserProfile()
                userObj.name = userFormObj.clean()['name'].strip()
                userObj.username = userFormObj.clean()['username'].strip()
                if userFormObj.clean()['password1'].strip() == userFormObj.clean()['password2'].strip() and len(userFormObj.clean()['password1'].strip()) > 0:
                    userObj.set_password(userFormObj.clean()['password1'].strip())
                else:
                    data['code'] = '1'
                    data['error'] = '两次输入密码不一致'
                    return HttpResponse(json.dumps(data))
                userObj.email = userFormObj.clean()['email'].strip()
                userObj.status = userFormObj.clean()['status']
                userObj.desc = userFormObj.clean()['desc']
                userObj.save()
                return HttpResponseRedirect('/')
            else:
                data['code'] = '1'
                data['error'] = userFormObj.errors
                return HttpResponse(json.dumps(data))

    # 处理用户信息修改相关操作
    if request.GET.get('ac') == 'edit':
        if request.method == 'GET':
            data = {}
            # admin可以修改所有用户信息，其他运维用户只能修改自己的信息
            try:
                if not request.GET.get('id'):
                    userObj = UserProfile.objects.get(id=request.user.id)
                elif request.user.username == 'admin':
                    userObj = UserProfile.objects.get(id=request.GET.get('id'))
                elif int(request.GET.get('id')) == request.user.id:
                    userObj = UserProfile.objects.get(id=request.user.id)
                else:
                    raise
            except:
                data['code'] = '1'
                data['error'] = '请勿提交非法请求'
                return HttpResponse(json.dumps(data))
            userObjDic = {
                'name':userObj.name,
                'password1':'',
                'password2':'',
                'email':userObj.email,
                'status':userObj.status,
                'desc':userObj.desc,
            }
            userEditFormObj = userEditForm(userObjDic)
            username = userObj.username
            return render(request, 'pages/userdetail.html', {'userFormObj': userEditFormObj, 'username':username})
        elif request.method == 'POST':
            data = {}
            # 这里应该增加权限认证
            userEditFormObj = userEditForm(request.POST or None)
            if userEditFormObj.is_valid():
                try:
                    if request.user.username == 'admin':
                        userObj = UserProfile.objects.get(username=request.POST.get('username'))
                    elif request.POST.get('username') != request.user.username:
                        raise
                    else:
                        userObj = UserProfile.objects.get(username=request.POST.get('username').strip())

                    userObj.name = userEditFormObj.clean()['name'].strip()
                    if userEditFormObj.clean()['password1'].strip() != '' \
                    and userEditFormObj.clean()['password1'].strip() == userEditFormObj.clean()['password2'].strip():
                        userObj.set_password(userEditFormObj.clean()['password1'].strip())
                    userObj.email = userEditFormObj.clean()['email'].strip()
                    userObj.status = userEditFormObj.clean()['status']
                    userObj.desc = userEditFormObj.clean()['desc'].strip()
                    userObj.save()
                    return HttpResponseRedirect('/')
                except Exception as e:
                    data['code'] = '1'
                    data['error'] = '请勿提交非法请求'
                    return HttpResponse(json.dumps(data))
            else:
                print(userEditFormObj.errors)
                data['code'] = '1'
                data['error'] = userEditFormObj.errors
                return HttpResponse(json.dumps(data))

    # 处理用户删除操作
    if request.GET.get('ac') == 'delete':
        if request.method == 'POST':
            data = {}
            # 只有管理员admin才有权限删除用户
            if request.user.username == 'admin':
                try:
                    uid = int(request.GET.get('id'))
                    if uid == request.user.id:
                        raise
                    userObj = UserProfile.objects.get(id=uid)
                    userObj.delete()
                    data['code'] = '0'
                    data['result'] = u'删除成功'
                    return HttpResponseRedirect('/')
                except Exception as e:
                    print(e)
                    data['code'] = '1'
                    data['error'] = u'请勿提交非法请求'
                    return HttpResponse(json.dumps(data))
            else:
                data['code'] = '1'
                data['error'] = u'您没有权限执行删除操作'
                return HttpResponse(json.dumps(data))

