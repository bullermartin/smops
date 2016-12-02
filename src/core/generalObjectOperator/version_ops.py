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
from core.generalObjectOperator.sshconnect import sshConnect
from core.models import sys_user, business, host, publish_event, business_host
from smops.sysConfig import *
from core.UserProfile import *
from api.getPage import *
from smops.sysConfig import *
import json

@requireLoginForbidden
def versionOperator(request):
    '''
        处理版本相关操作
    '''

    # 获取待发布版本列表
    if request.GET.get('ac') == 'list':
        data = {}
        if request.method == 'POST':
            try:
                businessId = int(request.GET.get('id'))
            except:
                data['code'] = '1'
                data['error'] = '请勿提交非法请求'
                return HttpResponse(json.dumps(data))
            try:
                businessObj = business.objects.get(id=businessId)
                # data['current_ver'] = businessObj.version.current_version
                data['current_ver'] = businessObj.current_version
                hostList = []
                for h in businessObj.host.all():
                    # 排除当前运行版本与业务版本一致的主机
                    # if business_host.objects.get(business=businessObj,host=h).current_version == businessObj.current_version:
                    #     continue
                    hostList.append({'id':h.id, 'name':h.name})
                data['hostlist'] = hostList
                svnHostObj = businessObj.svn_user.host
                if svnHostObj.status != 0:
                    data['code'] = '1'
                    data['error'] = '该业务所在SVN服务器暂时无法使用'
                    return HttpResponse(json.dumps(data))
                svnuserObj = businessObj.svn_user
                for h in businessObj.host.all():
                    if h.status == 0:
                        sysuserList = sys_user.objects.filter(user=request.user, host=h)
                        if len(sysuserList) == 0:
                            data['code'] = '1'
                            data['error'] = '请为业务主机('+h.name+')配置系统用户'
                            return HttpResponse(json.dumps(data))
                            break
                        ssh = sshConnect(host=h.ipaddr, port=h.port, username=sysuserList[0].username, \
                                         password=sysuserList[0].password)
                        ssh.excute('svn list --username '+svnuserObj.username+' --password '+svnuserObj.password \
                                   +' --non-interactive svn://'+svnHostObj.ipaddr+businessObj.svn_dir)
                        if len(ssh.stderr) > 0:
                            data['code'] = '1'
                            data['error'] = '连接'+h.name+'获取'+businessObj.name+'业务版本列表失败'
                            return HttpResponse(json.dumps(data))
                            break
                        else:
                            data['code'] = '0'
                            data['error'] = '连接'+str(h.name)+'获取'+str(businessObj.name)+'业务版本列表成功'
                            data['verlist'] = []
                            temp = ssh.stdout
                            temp = temp[::-1]
                            for i in range(len(temp)):
                                temp[i] = temp[i].strip()
                                if businessObj.current_version == temp[i][:-1] or len(data['verlist']) == int(sysConfig['maxVersionNum']):
                                    data['verlist'].append({'id':i+1, 'ver':temp[i][:-1]})
                                    break
                                else:
                                    data['verlist'].append({'id':i+1, 'ver':temp[i][:-1]})
                            versionSort(data['verlist'])
                            ssh.close()
                            # if len(data['verlist']) == 0:
                            #     data['verlist'].append({'id':0, 'ver':'当前已经是最新版本'})  # 当前已经是最新版本
                            return HttpResponse(json.dumps(data))
                            break
            except Exception as e:
                print(e)
                data['code'] = '1'
                data['error'] = '获取SVN服务器信息失败'
                return HttpResponse(json.dumps(data))

    # 获取待回滚版本列表
    if request.GET.get('ac') == 'rlist':
        data = {}
        if request.method == 'POST':
            try:
                businessId = int(request.GET.get('id'))
            except:
                data['code'] = '1'
                data['error'] = '请勿提交非法请求'
                return HttpResponse(json.dumps(data))
            try:
                businessObj = business.objects.get(id=businessId)
                # data['current_ver'] = businessObj.version.current_version
                data['current_ver'] = businessObj.current_version
                hostList = []
                for h in businessObj.host.all():
                    # 排除当前运行版本与业务版本一致的主机
                    # if business_host.objects.get(business=businessObj,host=h).current_version == businessObj.current_version:
                    #     continue
                    hostList.append({'id':h.id, 'name':h.name})
                data['hostlist'] = hostList
                svnHostObj = businessObj.svn_user.host
                if svnHostObj.status != 0:
                    data['code'] = '1'
                    data['error'] = '该业务所在SVN服务器暂时无法使用'
                    return HttpResponse(json.dumps(data))
                svnuserObj = businessObj.svn_user
                for h in businessObj.host.all():
                    if h.status == 0:
                        sysuserList = sys_user.objects.filter(user=request.user, host=h)
                        ssh = sshConnect(host=h.ipaddr, port=h.port, username=sysuserList[0].username, \
                                         password=sysuserList[0].password)
                        ssh.excute('svn list --username '+svnuserObj.username+' --password '+svnuserObj.password \
                                   +' --non-interactive svn://'+svnHostObj.ipaddr+businessObj.svn_dir)
                        if len(ssh.stderr) > 0:
                            data['code'] = '1'
                            data['error'] = '连接'+h.name+'获取'+businessObj.name+'业务版本列表失败'
                        else:
                            data['code'] = '0'
                            data['error'] = '连接'+str(h.name)+'获取'+str(businessObj.name)+'业务版本列表成功'
                            data['verlist'] = []
                            temp = ssh.stdout
                            temp = temp[::-1]
                            flag = False
                            for i in range(len(temp)):
                                temp[i] = temp[i].strip()
                                if businessObj.current_version == temp[i][:-1]:
                                    temp[i] = temp[i].strip()
                                    flag = True
                                    data['verlist'] = []
                                    for j in range(i,len(temp)):
                                        temp[j] = temp[j].strip()
                                        data['verlist'].append({'id':j+1, 'ver':temp[j][:-1]})
                                        if j == int(sysConfig['maxVersionNum']):
                                            break
                                    break
                                else:
                                    data['verlist'].append({'id':i+1, 'ver':temp[i][:-1]})
                            if not flag:
                                data['verlist'] = data['verlist'][:int(sysConfig['maxVersionNum'])]
                            ssh.close()
                            if len(data['verlist']) == 0:
                                data['verlist'].append({'id':0, 'ver':'当前已经是最新版本'})  # 当前已经是最新版本
                            # data['verlist'] = getPage(list=data['verlist'][::-1], page=1, num=5)
                            return HttpResponse(json.dumps(data))
                            break
            except Exception as e:
                print(e)
                data['code'] = '1'
                data['error'] = '获取SVN服务器信息失败'
                return HttpResponse(json.dumps(data))

    # 发布或回滚版本
    if request.GET.get('ac') == 'publish' or request.GET.get('ac') == 'rollback':
        if request.method == 'POST':
            data = {}
            try:
                for k, v in json.loads(request.POST['data']).items():
                    data[k] = v
                if len(data['new_ver'].strip()) == 0:
                    raise
                businessObj = business.objects.get(id=int(data['business']))
                # 判断用户提交目录是否合法
                flag = False
                for d in sysConfig['allowedBusinessDir']:
                    if d in businessObj.directory:
                        flag = True
                        break
                if not flag:
                    data['code'] = '1'
                    data['error'] = '请确认业务根目录是否正确'
                    return HttpResponse(json.dumps(data))
                svnuserObj = businessObj.svn_user
                svnHostObj = svnuserObj.host
                publish_eventDict = {
                    'operator':request.user.name,
                    'ipaddr':request.META['REMOTE_ADDR'],
                    'original_ver':'',
                    'current_ver':businessObj.current_version,
                    'rollback_ver':'',
                    'status':'',
                    'desc':data['desc'],
                    'result':''
                }
                hostList = []
                for i in data['hostlist']:
                    h = host.objects.get(id=int(i),status=0)
                    sysuser = sys_user.objects.get(host=h)
                    hostList.append({'host':h, 'sysuser':sysuser,'svnuser':svnuserObj})
            except:
                data['code'] = '1'
                data['error'] = '请勿提交非法请求'
                return HttpResponse(json.dumps(data))
            data['result'] = []
            for h in hostList:
                ssh = sshConnect(host=h['host'].ipaddr, port=h['host'].port, \
                                 username=h['sysuser'].username, password=h['sysuser'].password)
                # 这里应该验证用户提交过来的数据是否有效,如data['new_ver']是否为空或者在svn中是否存在或者业务目录是否为/根目录
                ssh.excute('svn export --username '+svnuserObj.username+' --password '+svnuserObj.password \
                           + ' --non-interactive --force svn://'+ svnHostObj.ipaddr+businessObj.svn_dir \
                           + data['new_ver']+'/ '+businessObj.directory)
                businesshost = business_host.objects.get(business=businessObj, host=h['host'])
                # 发布失败
                if len(ssh.stderr) > 0:
                    h['code'] = '1'
                    h['error'] = ssh.stderr
                    publish_eventDict['original_ver'] = businessObj.current_version
                    publish_eventDict['status'] = '1'
                    publish_eventDict['result'] = h['error']
                    data['result'].append({'hname':h['host'].name,'bname':businessObj.name,'oversion':publish_eventDict['original_ver'],'cversion':businesshost.current_version,'code':h['code'],'error':h['error']})
                    ssh.excute('chown -R '+businessObj.running_user+'.'+businessObj.running_user+' '+businessObj.directory)
                    publish_event.objects.create(**publish_eventDict)
                    ssh.close()
                    continue
                # 发布成功
                else:
                    ssh.excute('chown -R '+businessObj.running_user+'.'+businessObj.running_user+' '+businessObj.directory)
                    h['code'] = '0'
                    if len(ssh.stderr) > 0:
                        if request.GET.get('ac') == 'publish':
                            h['result'] = str(h['host'].name)+' 发布成功,但权限修改失败'
                        else:
                            h['result'] = str(h['host'].name)+' 回滚成功,但权限修改失败'
                    else:
                        if request.GET.get('ac') == 'publish':
                            h['result'] = str(h['host'].name)+' 发布成功'
                        else:
                            h['result'] = str(h['host'].name)+' 回滚成功'
                    publish_eventDict['original_ver'] = businessObj.current_version
                    businesshost.current_version = data['new_ver']
                    businesshost.save()
                    data['result'].append({'hname':h['host'].name,'bname':businessObj.name,'oversion':publish_eventDict['original_ver'],'cversion':businesshost.current_version,'code':h['code'],'result':h['result']})
                    if request.GET.get('ac') == 'publish':
                        publish_eventDict['current_ver'] = data['new_ver']
                    else:
                        publish_eventDict['current_ver'] = data['new_ver']
                        publish_eventDict['rollback_ver'] = data['new_ver']
                    publish_eventDict['status'] = '0'
                    for r in h['result']:
                        publish_eventDict['result'] += r
                    publish_event.objects.create(**publish_eventDict)
                ssh.close()
            # 这里应该判断什么情况下才属于发布成功
            count = 0
            for h in data['result']:
                if h['code'] == '0':
                    count += 1
            if count > 0:
                businessObj.current_version = data['new_ver']
                businessObj.save()
            return render(request, 'pages/publishresult.html',{'data':data})

def versionSort(data):
    versionList = []
    for v in data:
        versionList.append(v['ver'])
    # versionList = ['1.2.3','33.231.99', '3.2.1', '33.232.998', '33.232.999', '1.3.3', '11.2.9', '1.2.2', '33.231.100']
    try:
        for i in range(len(versionList)-1):  # 对版本号进行冒泡排序
            for j in range(i+1,len(versionList)):
                if int(versionList[i].split('.')[0]) < int(versionList[j].split('.')[0]):
                    t = versionList[i]
                    versionList[i] = versionList[j]
                    versionList[j] = t
                    continue
                if int(versionList[i].split('.')[0]) == int(versionList[j].split('.')[0]):
                    if int(versionList[i].split('.')[1]) < int(versionList[j].split('.')[1]):
                        t = versionList[i]
                        versionList[i] = versionList[j]
                        versionList[j] = t
                        continue
                    if int(versionList[i].split('.')[1]) == int(versionList[j].split('.')[1]):
                        if int(versionList[i].split('.')[2]) < int(versionList[j].split('.')[2]):
                            t = versionList[i]
                            versionList[i] = versionList[j]
                            versionList[j] = t
                            continue
    except:
        return data
    for i in range(len(data)):
        data[i]['ver'] = versionList[i]
    return data


