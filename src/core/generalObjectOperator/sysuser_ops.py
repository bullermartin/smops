# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: sysuser_ops.py
@time: 2016/6/3 17:06
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from core.decorators import requireLogin
from core.forms.sysUserAddForm import sysUserAddForm
from core.forms.sysUserEditForm import sysUserEditForm
from core.models import sys_user
from core.UserProfile import *
# from core.forms.sysUserAddFormTest import sysUserAddFormTest

@requireLogin
def sysUserOperator(request):
    if request.GET.get('ac') == 'add':
        if request.method == 'GET':
            # testSUObj = sysUserAddFormTest(request.user.username)
            # return render(request, 'pages/sysuseraddtest.html', {'sysUserFormObj':testSUObj})
            sysUserFormObj = sysUserAddForm()
            if request.user.username == 'admin':
                ownerList = UserProfile.objects.all()
                return render(request, 'pages/sysuseradd.html', {'sysUserFormObj':sysUserFormObj,'ownerList':ownerList})
            else:
                return render(request, 'pages/sysuseradd.html', {'sysUserFormObj':sysUserFormObj})

        elif request.method == 'POST':
            # 处理点击保存按钮
            sysUserFormObj = sysUserAddForm(request.POST or None)
            if sysUserFormObj.is_valid():
                sysUserObj = sys_user()
                sysUserObj.username = sysUserFormObj.clean()['username']
                sysUserObj.password = sysUserFormObj.clean()['password']
                sysUserObj.host = sysUserFormObj.clean()['host_id']
                if request.user.username == 'admin':
                    try:
                        u = UserProfile.objects.get(id=int(request.POST.get('owner')))
                        sysUserObj.user_id = u.id
                    except:
                        return HttpResponse('添加失败！')
                else:
                    sysUserObj.user_id = request.user.id
                try:
                    sysUserObj.save()
                    return HttpResponseRedirect('/')
                except Exception as e:
                    return HttpResponse('添加失败！')
            else:
                return HttpResponse(sysUserFormObj.errors)
        else:
            return HttpResponseRedirect('/')


    if request.GET.get('ac') == 'edit':
        if request.method == 'GET':
            if request.GET.get('id') != '':
                try:
                    sysUserObj = sys_user.objects.get(id=request.GET.get('id'))
                except:
                    return HttpResponse('找不到您提交的用户！')
                sysUserDict = {
                    'host_id':sysUserObj.host_id,
                    'username':sysUserObj.username,
                    'password':'',
                    'user_id':sysUserObj.user_id,
                }
                sysUserFormObj = sysUserEditForm(sysUserDict)
                return render(request, 'pages/sysuserdetail.html', {'sysUserFormObj':sysUserFormObj, 'suid':sysUserObj.id})
            else:
                return HttpResponse('请勿提交非法操作！')
        elif request.method == 'POST':
            if request.GET.get('id') != '':
                sysUserFormObj = sysUserEditForm(request.POST or None)
                if sysUserFormObj.is_valid():
                    try:
                        sysUserObj = sys_user.objects.get(id=request.GET.get('id'))
                    except:
                        return HttpResponse('找不到您提交的用户！')
                    sysUserObj.host_id = sysUserFormObj.clean()['host_id']
                    sysUserObj.username = sysUserFormObj.clean()['username']
                    if len(sysUserFormObj.clean()['password'].strip()) != 0:
                        sysUserObj.password = sysUserFormObj.clean()['password'].strip()
                    sysUserObj.user_id = sysUserFormObj.clean()['user_id']
                    sysUserObj.save()
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse(sysUserFormObj.errors)

    if request.GET.get('ac') == 'delete':
        if request.method == 'GET':
            if request.GET.get('id') != '':
                try:
                    sysUserObj = sys_user.objects.get(id=int(request.GET.get('id')))
                    if request.user.username != 'admin' and sysUserObj.user_id != request.user.id:
                        raise
                except:
                    return HttpResponse('请勿提交非法请求')
                sysUserObj.delete()
                return HttpResponse('删除成功')
            else:
                return HttpResponse('请勿提交非法请求')