# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: whitelist_ops.py
@time: 2016/7/5 19:27
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from core.decorators import requireLoginForbidden
from core.models import host, whitelist_event, business
from core.generalObjectOperator.sshconnect import sshConnect
from smops.sysConfig import *
from api.getPage import getPage
import logging
import json
import re

logger = logging.getLogger(__name__)

@requireLoginForbidden
def whiteListOperator(request):
    # 处理白名单相关所有操作
    if request.method == 'POST':
        # 从主机获取白名单列表
        if request.GET.get('ac') == 'list':
            data = getWhiteList(request)
            try:
                if request.GET.get('page'):
                    page = int(request.GET.get('page'))
                else:
                    page = 1
                data['whitelist'] = getPage(data['whitelist'], page, sysConfig['perPageNum'])
                businessObj = business.objects.get(name=sysConfig['whiteListBusiness'].lower())
                hostList = businessObj.host.all()
                return render(request, 'pages/whitelist_content.html', {'data': data, 'hostList': hostList})
            except:
                data['code'] = 1
                data['error'] = '请勿提交非法请求'
                return HttpResponse(json.dumps(data))

        # 处理添加白名单操作
        if request.GET.get('ac') == 'add':
            # 检查系统配置中白名单起止字符串及分割字符串是否配置正确
            if sysConfig['whitelistStart'] == sysConfig['whitelistEnd'] \
                    or sysConfig['iptablesSplit'] not in sysConfig['whitelistStart'] \
                    or sysConfig['iptablesSplit'] not in sysConfig['whitelistEnd']:
                data = {}
                data['code'] = '1'
                data['error'] = '系统白名单配置错误，请检查！'
                return HttpResponse(json.dumps(data))
            try:
                data = request.POST.get('data')
                data = json.loads(data)
                if len(data['desc'].strip()) == 0:
                    data['code'] = '1'
                    data['error'] = '描述不能为空'
                    return HttpResponse(json.dumps(data))
                data['ipaddr'] = re.sub(r"\\",'/',data['ipaddr'])
                data['ipaddr'] = re.sub('/+','/',data['ipaddr'])
                if not ipRuleCheck(data['ipaddr']):
                    return HttpResponse(json.dumps({'code':1, 'error':'IP地址不合法'}))
                whiteList = getWhiteList(request)
                if whiteList['code'] != '0':
                    return HttpResponse(json.dumps(data))
                for i in whiteList['whitelist']:
                    # 这里暂时只判断IP而不判断子网号
                    if data['ipaddr'].split('/')[0] == i['ip'].split('/')[0]:
                        data['code'] = '1'
                        data['error'] = '白名单IP地址已经存在'
                        return HttpResponse(json.dumps(data))
                result = insertWhiteIP(request, data)
                return HttpResponse(json.dumps(result))
            except:
                return HttpResponse(json.dumps({'code':1, 'error':'请勿提交非法请求'}))

def connectHost(request,data={}):
    try:
        hid = request.GET.get('id')
        hostObj = host.objects.get(id=hid)
        data['current'] = hostObj.name
        data['hid'] = hostObj.id
        su = hostObj.sys_user_set.get(user=request.user.id)
    except:
        data['code'] = '1'
        data['error'] = '请勿提交非法请求'
        return data
    try:
        ssh = sshConnect(host=hostObj.ipaddr, port=hostObj.port, username=su.username, password=su.password)
        return ssh
    except:
        data['code'] = '1'
        data['error'] = ssh.stderr
        ssh.close()
        return data

def getWhiteList(request):
    data = {}
    ssh = connectHost(request, data)
    # 当连接失败时ssh为字典
    if type(ssh) is dict:
        return ssh
    ssh.excute('cat /etc/sysconfig/iptables')
    if len(ssh.stderr) > 0:
        data['code'] = '1'
        data['error'] = ssh.stderr
        ssh.close()
        return data
    iptables = ssh.stdout
    for i in range(len(ssh.stdout)):
        iptables[i] = iptables[i].strip()
    flag = False
    whiteList = []
    # return HttpResponse(json.dumps(iptables))
    # print(iptables[18].strip())
    for i in range(len(iptables)):
        iptables[i] = iptables[i].strip()
        if iptables[i].strip() == '':
            continue
        if sysConfig['whitelistStart'] in iptables[i]:
            flag = True
            continue
        elif sysConfig['whitelistEnd'] in iptables[i]:
            flag = False
            break
        if flag and iptables[i][0] == '#':
            continue
        if flag:
            temp = iptables[i].split()
            if '/' in temp[3]:
                ip = temp[3]
            else:
                ip = temp[3] + '/32'
            if iptables[i-1][0] == '#' and iptables[i-1].strip() != '' \
                    and sysConfig['iptablesSplit'] not in iptables[i-1]:
                desc = iptables[i-1].split('#')[-1]
            else:
                desc = ''
            whiteList.append({'ip':ip, 'desc':desc})
    data['code'] = '0'
    data['result'] = '获取白名单成功'
    data['whitelist'] = whiteList[::-1]
    ssh.close()
    return data

def ipRuleCheck(ip):
    if len(ip.split('/')) >2:
        return False
    if not re.search(r'^((([1-9]?|1\d)\d|2([0-4]\d|5[0-5]))\.){3}(([1-9]?|1\d)\d|2([0-4]\d|5[0-5]))$', ip.split('/')[0]):
        return False
    if len(ip.split('/')) == 2 and int(ip.split('/')[1]) not in range(1, 33):
        return False
    excludeRule = ['^127\.','^0', '^192\.168', '^169\.254', '^10\.', '^198\.18', '^198\.19']
    for r in excludeRule:
        # print(re.search(r, ip))
        if re.search(r, ip):
            # print (r)
            return False
    # 判断ip是否属于 172.16~172.31, 224~255开头
    if int(ip.split('.')[0]) > 223 and int(ip.split('.')[0]) <= 255:
        return False
    if ip.split('.')[0] == '172':
        if int(ip.split('.')[1]) > 15 and int(ip.split('.')[1]) < 32:
            return False
    return True

def insertWhiteIP(request, data):
    ssh = connectHost(request, data)
    # 当连接失败时ssh为字典
    if type(ssh) is dict:
        return ssh
    ssh.excute('cat /etc/sysconfig/iptables')
    if len(ssh.stderr) > 0:
        data['code'] = '1'
        data['error'] = ssh.stderr
        ssh.close()
        return data
    iptables = ssh.stdout
    for i in range(len(iptables)):
        iptables[i] = iptables[i].strip()
    # iptables = iptables.split('\n')
    # pos = ''
    # for i in range(len(iptables)):
    #     if sysConfig['whitelistEnd'] in iptables[i]:
    #         # 找到白名单结束标志位后退出循环
    #         pos = i
    #         break
    desc = '#' + data['desc'] + ' ' + data['ipaddr']
    ipaddr = '-A INPUT -s '+data['ipaddr']+' -p tcp -m tcp --dport 80 -j ACCEPT'
    ssh.excute('sed -i "/White-List-End/i\\'+ desc +'" /etc/sysconfig/iptables')
    if len(ssh.stderr) > 0:
        data['code'] = '1'
        data['error'] = ssh.stderr
        ssh.close()
        return data
    ssh.excute('sed -i "/White-List-End/i\\'+ ipaddr +'" /etc/sysconfig/iptables')
    if len(ssh.stderr) > 0:
        data['code'] = '1'
        data['error'] = ssh.stderr
        ssh.close()
        return data
    ssh.excute('service iptables reload')
    if len(ssh.stderr) > 0:
        data['code'] = '1'
        data['error'] = ssh.stderr
        ssh.close()
        return data
    data['code'] = '0'
    data['result'] = '添加成功'
    ssh.close()
    # 记录添加日志
    try:
        whitelist_event.objects.create(operator=request.user.name,
                                        ipaddr=data['ipaddr'].split('/')[0],
                                        operation='添加',
                                        status='0',
                                        src_ip=request.META['REMOTE_ADDR'],
                                        desc=data['desc'],)
    except Exception as e:
        print(e)
    return data
