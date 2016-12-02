# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: svnuser_ops.py
@time: 2016/6/3 17:06
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from core.decorators import requireLogin
from core.forms.svnUserAddForm import svnUserAddForm
from core.forms.svnUserEditForm import svnUserEditForm
from core.models import svn_user
from core.UserProfile import *


@requireLogin
def svnUserOperator(request):
    if request.GET.get('ac') == 'add':
        if request.method == 'GET':
            svnUserFormObj = svnUserAddForm()
            return render(request, 'pages/svnuseradd.html', {'svnUserFormObj':svnUserFormObj})

        elif request.method == 'POST':
            # 处理点击保存按钮
            svnUserFormObj = svnUserAddForm(request.POST or None)
            if svnUserFormObj.is_valid():
                svnUserObj = svn_user()
                svnUserObj.name = svnUserFormObj.clean()['name']
                svnUserObj.username = svnUserFormObj.clean()['username']
                svnUserObj.password = svnUserFormObj.clean()['password']
                svnUserObj.host_id = svnUserFormObj.clean()['host_id'].id
                print(svnUserFormObj.clean()['host_id'], type(svnUserFormObj.clean()['host_id']))
                try:
                    svnUserObj.save()
                    return HttpResponseRedirect('/')
                except Exception as e:
                    print(e)
                    return HttpResponse('添加失败！')
            else:
                return HttpResponse(svnUserFormObj.errors)
        else:
            return HttpResponseRedirect('/')

    if request.GET.get('ac') == 'edit':
        if request.method == 'GET':
            if request.GET.get('id') != '':
                try:
                    svnUserObj = svn_user.objects.get(id=request.GET.get('id'))
                except:
                    return HttpResponse('找不到您提交的用户！')
                sysUserDict = {
                    'name':svnUserObj.name,
                    'username':svnUserObj.username,
                    'password':'',
                    'host_id':svnUserObj.host_id,
                }
                svnUserFormObj = svnUserEditForm(sysUserDict)
                return render(request, 'pages/svnuserdetail.html', {'svnUserFormObj':svnUserFormObj, 'svid':svnUserObj.id})
            else:
                return HttpResponse('请勿提交非法操作！')
        elif request.method == 'POST':
            if request.GET.get('id') != '':
                svnUserFormObj = svnUserEditForm(request.POST or None)
                if svnUserFormObj.is_valid():
                    try:
                        svnUserObj = svn_user.objects.get(id=request.GET.get('id'))
                    except:
                        return HttpResponse('请勿提交非法请求')
                    svnUserObj.name = svnUserFormObj.clean()['name']
                    svnUserObj.username = svnUserFormObj.clean()['username']
                    if len(svnUserFormObj.clean()['password'].strip()) != 0:
                        svnUserObj.password = svnUserFormObj.clean()['password'].strip()
                    svnUserObj.host_id = svnUserFormObj.clean()['host_id']
                    svnUserObj.save()
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse(svnUserFormObj.errors)

    if request.GET.get('ac') == 'delete':
        if request.method == 'GET':
            if request.GET.get('id').strip() != '':
                try:
                    svnUserObj = svn_user.objects.get(id=int(request.GET.get('id')))
                    svnUserObj.delete()
                    return HttpResponse('删除成功')
                except:
                    return HttpResponse('请勿提交非法请求')
            else:
                return HttpResponse('请勿提交非法请求')