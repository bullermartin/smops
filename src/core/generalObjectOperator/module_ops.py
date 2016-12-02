# -*- coding:utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Ron
@software: PyCharm
@file: module_ops.py
@time: 2016/7/18 13:19
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from core.decorators import requireLoginForbidden
from core.models import module
from core.UserProfile import *
import json

@requireLoginForbidden
def moduleOperator(request):
    '''
        处理模块管理操作
    '''
    if request.GET.get('ac') == 'modulelist':
        data = {}
        # 处理获取模块列表
        if request.method == 'GET':
            if request.user.username == 'admin':
                try:
                    cu = int(request.GET.get('id'))
                    if cu == 0:
                        data['code'] = '1'
                        data['error'] = '请选择用户'
                        return HttpResponse(json.dumps(data))
                    else:
                        cuObj = UserProfile.objects.get(id=cu)
                        if not cuObj:
                            raise
                    moduleList = module.objects.filter(user=cuObj).exclude(parent=0)
                    data['moduleList'] = []
                    for m in moduleList:
                        data['moduleList'].append({'id':m.id, 'desc':m.desc})
                    availableList = module.objects.exclude(user=cuObj).exclude(parent=0)
                    data['availableList'] = []
                    for m in availableList:
                        data['availableList'].append({'id':m.id, 'desc':m.desc})
                    data['code'] = '0'
                    return HttpResponse(json.dumps(data))
                except:
                    data['code'] = '1'
                    data['error'] = '请勿提交非法请求1'
                    return HttpResponse(json.dumps(data))
            else:
                data['code'] = '1'
                data['error'] = '请勿提交非法请求2'
                return HttpResponse(json.dumps(data))

        # 处理提交的模块权限修改操作
        if request.method == 'POST':
            data = {}
            try:
                cu = int(request.GET.get('id'))
                moduleIdList = json.loads(request.POST.get('moduleList'))
                if cu == 0:
                    data['code'] = '1'
                    data['error'] = '请选择用户'
                    return HttpResponse(json.dumps(data))
                cuObj = UserProfile.objects.get(id=cu)
                if not cuObj:
                    raise
                moduleList = []
                for id in moduleIdList:
                    mObj = module.objects.get(id=id)
                    if not mObj and mObj.parent != 0:
                        raise
                    else:
                        moduleList.append(mObj)
                oldModuleList = module.objects.filter(user=cuObj)
                if request.user.username != 'admin':    # 管理员只能给自己添加模块权限
                    for om in oldModuleList:
                        if om in moduleList:
                            continue
                        elif om.parent != 0:
                            om.user.remove(cuObj)

                for m in moduleList:
                    if m in oldModuleList:
                        continue
                    elif m.parent != 0:
                        m.user.add(cuObj)
                        module.objects.get(id=m.parent).user.add(cuObj)
                data['code'] = '0'
                return HttpResponse(json.dumps(data))
            except:
                data['code'] = '1'
                data['error'] = '请勿提交非法请求'
                return HttpResponse(json.dumps(data))