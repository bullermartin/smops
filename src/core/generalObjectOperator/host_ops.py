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
from core.forms.hostAddForm import hostAddForm
from core.models import host
from smops.sysConfig import *
from api.getPage import getPage
import json

@requireLoginForbidden
def hostOperator(request):
    '''
        处理主机相关操作
    '''

    # 处理添加主机操作
    if request.GET.get('ac') == 'add':
        if request.method == 'GET':
            hostAddFormObj = hostAddForm()
            return render(request, 'pages/hostadd.html', {'hostAddFormObj':hostAddFormObj})
        if request.method == 'POST':
            # 点击添加按钮操作
            hostAddFormObj = hostAddForm(request.POST or None)
            if hostAddFormObj.is_valid():
                hostObj = host()
                hostObj.name = hostAddFormObj.clean()['name']
                hostObj.desc = hostAddFormObj.clean()['desc']
                hostObj.ipaddr = hostAddFormObj.clean()['ipaddr']
                if hostAddFormObj.clean()['prefix']:
                    hostObj.prefix = hostAddFormObj.clean()['prefix']
                else:
                    hostObj.prefix = 32
                if hostAddFormObj.clean()['port']:
                    hostObj.port = hostAddFormObj.clean()['port']
                else:
                    hostObj.port = 22
                hostObj.status = hostAddFormObj.clean()['status']
                hostObj.save()
                return HttpResponseRedirect('/')
            else:
                # return HttpResponse('添加主机失败！')
                return HttpResponse(hostAddFormObj.errors)

    if request.GET.get('ac') == 'edit':
        # 处理点击编辑按钮的操作
        if request.method == 'GET':
            try:
                if request.GET.get('id').strip() == '':
                    raise
                hostObj = host.objects.get(id=int(request.GET.get('id').strip()))
            except:
                return HttpResponse('请勿提交非法请求')
            hostObjDict = {
                'name':hostObj.name,
                'desc':hostObj.desc,
                'ipaddr':hostObj.ipaddr,
                'prefix':hostObj.prefix,
                'port':hostObj.port,
                'status':hostObj.status,
            }
            hostEditFormObj = hostAddForm(hostObjDict)
            return render(request, 'pages/hostdetail.html', {'hostEditFormObj':hostEditFormObj, 'hid':hostObj.id})

        # 处理用户提交的主机信息
        if request.method == 'POST':
            try:
                if request.GET.get('id').strip() == None:
                    raise
                hostObj = host.objects.get(id=int(request.GET.get('id').strip().strip()))
            except:
                return HttpResponse('请勿提交非法请求！')
            hostEditFormObj = hostAddForm(request.POST or None)
            if hostEditFormObj.is_valid():
                hostObj.name = hostEditFormObj.clean()['name']
                hostObj.desc = hostEditFormObj.clean()['desc']
                hostObj.ipaddr = hostEditFormObj.clean()['ipaddr']
                hostObj.prefix = hostEditFormObj.clean()['prefix']
                hostObj.port = hostEditFormObj.clean()['port']
                hostObj.status = hostEditFormObj.clean()['status']
                try:
                    hostObj.save()
                    return HttpResponseRedirect('/')
                except:
                    return HttpResponse('修改失败')
            else:
                return HttpResponse(hostEditFormObj.errors)

    # 处理主机删除操作
    if request.GET.get('ac') == 'delete':
        try:
            if request.GET.get('id').strip() == None:
                raise
            hostObj = host.objects.get(id=int(request.GET.get('id').strip()))
            hostObj.delete()
            return HttpResponse('删除成功！')
        except Exception as e:
            return HttpResponse(e)

    # 处理主机搜索操作
    if request.GET.get('ac') == 'search':
        data = {}
        if request.GET.get('kw') == '':
            return HttpResponse('请勿提交非法请求！')
        kw = request.GET.get('kw').lower()
        hostObj = {}
        hostList = []
        for h in host.objects.all():
            if kw in h.name.lower() or kw in h.ipaddr or kw in h.desc:
                hostObj['id'] = h.id
                hostObj['name'] = h.name
                hostObj['ipaddr'] = h.ipaddr
                hostObj['prefix'] = h.prefix
                hostObj['port'] = h.port
                hostObj['status'] = h.status
                hostObj['desc'] = h.desc
                hostObj['add_time'] = h.add_time
                hostObj['modify_time'] = h.modify_time
                hostList.append(hostObj)
                hostObj = {}
        if len(hostList) == 0:
            data['code'] = '1'
            data['error'] = '找不到匹配的主机'
            return HttpResponse(json.dumps(data))
        hostList = getPage(hostList,page=1,num=sysConfig['perPageNum'])
        return render(request, 'pages/hostlist.html', {'hostList':hostList, })
