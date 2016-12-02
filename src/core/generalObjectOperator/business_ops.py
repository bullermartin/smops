# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: host_ops.py
@time: 2016/6/6 17:21
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from core.decorators import requireLoginForbidden
from core.forms.businessAddForm import businessAddForm
from core.forms.businessEditForm import businessEditForm
from core.models import business, business_host
from smops.sysConfig import *
import re
import json

@requireLoginForbidden
def businessOperator(request):
    '''
        处理业务项目相关操作
    '''

    # 处理添加业务操作
    if request.GET.get('ac') == 'add':
        if request.method == 'GET':
            businessAddFormObj = businessAddForm()
            return render(request, 'pages/businessadd.html', {'businessAddFormObj':businessAddFormObj})

        if request.method == 'POST':
            data = {}
            # 点击添加按钮操作
            businessAddFormObj = businessAddForm(request.POST or None)
            if businessAddFormObj.is_valid():
                businessObj = business()
                businessObj.name = businessAddFormObj.clean()['name']
                businessObj.directory = re.sub(r"\\", '/', businessAddFormObj.clean()['directory'])
                businessObj.directory = re.sub(r'/+', '/', businessObj.directory)
                # 判断用户提交目录是否合法
                flag = False
                for d in sysConfig['allowedBusinessDir']:
                    if businessObj.directory.startswith(d):
                        if businessObj.directory[0] == '/' and len(businessObj.directory) > 1:
                            if businessObj.directory[-1] != '/':
                                businessObj.directory += '/'
                            flag = True
                        break
                if not flag:
                    data['code'] = '1'
                    data['error'] = '请确认业务根目录是否正确'
                    return HttpResponse(json.dumps(data))

                # 判断用户提交SVN目录是否合法
                businessObj.svn_dir = re.sub(r"\\", '/', businessAddFormObj.clean()['svn_dir'])
                businessObj.svn_dir = re.sub(r'/+', '/', businessObj.svn_dir)
                if businessObj.svn_dir[0] == '/':
                    if businessObj.svn_dir[-1] != '/':
                        businessObj.svn_dir += '/'
                else:
                    data['code'] = '1'
                    data['error'] = '请确认SVN目录是否正确'
                    return HttpResponse(json.dumps(data))

                businessObj.running_user = businessAddFormObj.clean()['running_user']
                businessObj.svn_user = businessAddFormObj.clean()['svn_user']
                businessObj.status = businessAddFormObj.clean()['status']
                try:
                    businessObj.save()  #这里必须先保存之后才能添加ManyToMany字段
                except:
                    data['code'] = '1'
                    data['error'] = '添加业务失败！'
                    return HttpResponse(json.dumps(data))
                for h in businessAddFormObj.clean()['host']:
                    business_host.objects.create(business=businessObj, host=h, current_version=businessObj.current_version)
                    # businessObj.host.add(h)
                return HttpResponseRedirect('/')
            else:
                # return HttpResponse('添加业务失败！')
                # return HttpResponse(businessAddFormObj.errors)
                return render(request, 'pages/businessadd.html', {'error':businessAddFormObj.errors})

    # 处理修改业务操作
    if request.GET.get('ac') == 'edit':
        # 处理点击编辑按钮的操作
        if request.method == 'GET':
            try:
                if request.GET.get('id').strip() == '':
                    raise
                businessObj = business.objects.get(id=int(request.GET.get('id').strip()))
            except:
                return HttpResponse('请勿提交非法请求')
            businessObjDict = {
                'name':businessObj.name,
                'status':businessObj.status,
                'directory':businessObj.directory,
                'svn_dir':businessObj.svn_dir,
                'running_user':businessObj.running_user,
                'svn_user':businessObj.svn_user,
                'host':businessObj.host.all(),
            }
            businessEditFormObj = businessEditForm(businessObjDict)
            return render(request, 'pages/businessdetail.html', {'businessEditFormObj':businessEditFormObj, 'bid':businessObj.id})

        # 处理点击保存按钮的操作
        if request.method == 'POST':
            data = {}
            try:
                if request.GET.get('id').strip() == None:
                    raise
                businessObj = business.objects.get(id=int(request.GET.get('id').strip()))
            except:
                return HttpResponse('请勿提交非法请求！')
            businessEditFormObj = businessEditForm(request.POST or None)
            if businessEditFormObj.is_valid():
                businessObj.name =  businessEditFormObj.clean()['name']
                businessObj.status =  businessEditFormObj.clean()['status']
                businessObj.directory = re.sub(r"\\", '/', businessEditFormObj.clean()['directory'])
                businessObj.directory = re.sub(r'/+', '/', businessObj.directory)
                # 判断用户提交目录是否合法
                flag = False
                for d in sysConfig['allowedBusinessDir']:
                    if businessObj.directory.startswith(d):
                        if businessObj.directory[0] == '/' and len(businessObj.directory) > 1:
                            if businessObj.directory[-1] != '/':
                                businessObj.directory += '/'
                            flag = True
                        break
                if not flag:
                    data['code'] = '1'
                    data['error'] = '请确认业务根目录是否正确'
                    return HttpResponse(json.dumps(data))

                # 判断用户提交SVN目录是否合法
                businessObj.svn_dir = re.sub(r"\\", '/', businessEditFormObj.clean()['svn_dir'])
                businessObj.svn_dir = re.sub(r'/+', '/', businessObj.svn_dir)
                if businessObj.svn_dir[0] == '/':
                    if businessObj.svn_dir[-1] != '/':
                        businessObj.svn_dir += '/'
                else:
                    data['code'] = '1'
                    data['error'] = '请确认SVN目录是否正确'
                    return HttpResponse(json.dumps(data))

                businessObj.running_user =  businessEditFormObj.clean()['running_user']
                businessObj.svn_user =  businessEditFormObj.clean()['svn_user']
                for bh in businessObj.host.all():
                    business_host.objects.filter(host=bh).delete()
                for h in businessEditFormObj.clean()['host']:
                    business_host.objects.create(business=businessObj, host=h, current_version=businessObj.current_version)
                businessObj.save()
                return HttpResponseRedirect('/')
            else:
                data['code'] = '1'
                data['error'] = businessEditFormObj.errors
                return HttpResponse(json.dumps(data))

    # 处理主机删除操作
    if request.GET.get('ac') == 'delete':
        data = {}
        if request.user.username == 'admin':
            try:
                if request.GET.get('id').strip() == None:
                    raise
                businessObj = business.objects.get(id=int(request.GET.get('id').strip()))
                for b in business_host.objects.filter(business=businessObj):
                    b.delete()
                businessObj.delete()
                data['code'] = '0'
                data['result'] = '删除成功！'
                return HttpResponse(json.dumps(data))
            except Exception as e:
                data['code'] = '1'
                data['error'] = e
                return HttpResponse(json.dumps(data))
        else:
            data['code'] = '1'
            data['error'] = '请勿提交非法请求'
            return HttpResponse(json.dumps(data))