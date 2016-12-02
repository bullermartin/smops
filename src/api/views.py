# -*- coding:utf-8 -*-
# !/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: api.py
@time: 2016/4/26 10:26
"""
from smops.sysConfig import *
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from core.decorators import requireLogin, requireLoginForbidden, requireModulePermission
from core.models import whitelist_event, business, host, sys_user, svn_user, publish_event, business_host, module
from core.UserProfile import *
from smops.sysConfig import *
from api.getPage import getPage
import sys
import json
import logging

logger = logging.getLogger(__name__)


@requireLoginForbidden
def apiIndex(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        if request.GET.get('ac') == '':
            return HttpResponse(json.dumps({'code':'1', 'error':'请勿提交非法请求！'}))
        ac = 'Get' + request.GET.get('ac').capitalize()
        if hasattr(sys.modules[__name__], ac):
            func = getattr(sys.modules[__name__], ac)
            res = func(request)
            return render(request, res[0], res[1])
        else:
            return HttpResponse(json.dumps({'code':'1', 'error':'请勿提交非法请求2！'}))


@requireModulePermission
def GetWhitelist(request):
    businessObj = business.objects.get(name=sysConfig['whiteListBusiness'].lower())
    hostList = businessObj.host.all()
    return ['pages/whitelist.html', {'hostList':hostList}]


@requireModulePermission
def GetWhitelist_event(request):
    eventList = whitelist_event.objects.all()
    eventList = eventList[::-1]
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    eventList = getPage(eventList, page, sysConfig['perPageNum'])
    # eventList = getPage(page=page, list=eventList, num=sysConfig['pageNum'])
    return ['pages/whitelistevent.html', {'eventList':eventList}]


@requireModulePermission
def GetBusinesslist(request):
    businessList = business.objects.all()
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    businessList = getPage(businessList, page, sysConfig['perPageNum'])
    return ['pages/businesslist.html', {'businessList':businessList}]


@requireModulePermission
def GetHostlist(request):
    hostList = []
    temp = {}
    for h in host.objects.all():
        temp['id'] = h.id
        temp['name'] = h.name
        temp['ipaddr'] = h.ipaddr
        temp['prefix'] = h.prefix
        temp['port'] = h.port
        temp['status'] = h.status
        if not h.desc:
            temp['desc'] = ''
        else:
            temp['desc'] = h.desc
        temp['add_time'] = h.add_time
        temp['modify_time'] = h.modify_time
        hostList.append(temp)
        temp = {}
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    hostList = getPage(hostList, page, sysConfig['perPageNum'])
    return ['pages/hostlist.html', {'hostList':hostList}]


@requireModulePermission
def GetSysuser(request):
    sysuserList = []
    temp = {}
    if request.user.username == 'admin':
        sysuserAllowedList = sys_user.objects.all()
    else:
        sysuserAllowedList = sys_user.objects.filter(user=request.user)
    for su in sysuserAllowedList:
        temp['id'] = su.id
        temp['username'] = su.username
        temp['password'] = '********'
        temp['host_id'] = su.host.name
        temp['user_id'] = su.user.name
        sysuserList.append(temp)
        temp = {}
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    sysuserList = getPage(sysuserList, page, sysConfig['perPageNum'])
    return ['pages/sysuserlist.html', {'sysuserList':sysuserList}]


@requireModulePermission
def GetYwuser(request):
    ywuserList = []
    temp = {}
    for ywu in UserProfile.objects.all():
        temp['id'] = ywu.id
        temp['name'] = ywu.name
        temp['email'] = ywu.email
        temp['status'] = ywu.status
        temp['last_login'] = ywu.last_login
        if not ywu.last_login:
            temp['last_login'] = ''
        if not ywu.desc:
            temp['desc'] = ''
        else:
            temp['desc'] = ywu.desc
        ywuserList.append(temp)
        temp = {}
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    ywuserList = getPage(ywuserList, page, sysConfig['perPageNum'])
    return ['pages/userlist.html', {'ywuserList':ywuserList}]


@requireModulePermission
def GetSvnuser(request):
    svnuserList = []
    temp = {}
    for sv in svn_user.objects.all():
        temp['id'] = sv.id
        temp['name'] = sv.name
        temp['username'] = sv.username
        temp['host'] = sv.host.name
        allBusiness = sv.business_set.all()
        for i in range(len(allBusiness)):
            if i == 0:
                temp['business'] = str(allBusiness[i])
            else:
                temp['business'] = ',' + str(allBusiness[i])
        svnuserList.append(temp)
        temp = {}
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    svnuserList = getPage(svnuserList, page, sysConfig['perPageNum'])
    return ['pages/svnuserlist.html', {'svnuserList':svnuserList}]


@requireModulePermission
def GetVer_publish(request):
    businessList = business.objects.filter(status=0)
    return ['pages/verpublish.html', {'businessList':businessList}]


@requireModulePermission
def GetVer_event(request):
    publishEventList = publish_event.objects.all()[::-1]
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    publishEventList = getPage(publishEventList, page, sysConfig['perPageNum'])
    return ['pages/publishevent.html', {'publishEventList':publishEventList}]


@requireModulePermission
def GetVer_business(request):
    businessList = business.objects.all()
    businesshostList = []
    temp = {}
    for b in businessList:
        temp['business'] = b
        temp['hostlist'] = []
        for h in business_host.objects.filter(business=b):
            temp['hostlist'].append({'name':h.host.name, 'ipaddr':h.host.ipaddr, 'current_version':h.current_version})
        temp['hostnum'] = len(temp['hostlist'])
        businesshostList.append(temp)
        temp = {}
    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
    businesshostList = getPage(businesshostList, page, sysConfig['perPageNum'])
    return ['pages/verbusiness.html', {'businesshostList':businesshostList}]


@requireModulePermission
def GetVer_rollback(request):
    businessList = business.objects.filter(status=0)
    return ['pages/verrollback.html', {'businessList':businessList}]


@requireModulePermission
def GetModulelist(request):
    userList = UserProfile.objects.all()
    moduleList = []
    availableList = []
    return ['pages/modulelist.html', {'userList':userList, 'moduleList':moduleList, 'availableList':availableList}]
