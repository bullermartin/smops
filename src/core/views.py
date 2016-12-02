# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from core.forms import loginForm, registerForm
from core.models import module
from core.UserProfile import *

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        moduleList = getModuleList(request)
        return render(request, 'index.html', {'moduleList': moduleList})
        # return render_to_response( 'index.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def userLogin(request):
    '''
        用户登录处理函数
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        user_form = loginForm.loginForm()
        if request.method == 'GET':
            return render(request, 'login.html', {'loginForm': user_form})
        else:
            userFormObj = loginForm.loginForm(request.POST or None)
            if userFormObj.is_valid():
                username = userFormObj.clean()['username']
                password = userFormObj.clean()['password']
                userObj = authenticate(username=username, password=password)
                if userObj is not None:
                    if userObj.status == 0:
                        login(request, userObj)
                    else:
                        error_msg = '用户名已失效！'
                        return render(request, 'login.html', {'loginForm': user_form, 'error_msg': error_msg})
                    # request.session.set_expiry(7200)
                    return HttpResponseRedirect('/')
                else:
                    error_msg = '用户名或密码错误！'
                    return render(request, 'login.html', {'loginForm': user_form, 'error_msg': error_msg})
            else:
                error_msg = '请输入用户名和密码！'
                return render(request, 'login.html', {'loginForm': user_form, 'error_msg': error_msg})

def userLogout(request):
    '''
    用户注销处理函数
    '''
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        import UserProfile
        userObj = registerForm.registerForm()
        if request.method == 'GET':
            return render(request,'register.html', {'userObj':userObj})
        else:
            userObj = registerForm.registerForm(request.POST or None)
            if userObj.is_valid():
                newUser = UserProfile.UserProfile()
                newUser.username = userObj.clean()['username'].strip()
                newUser.set_password(userObj.clean()['password'].strip())
                newUser.status = userObj.status
                newUser.name = userObj.clean()['name'].strip()
                newUser.email = userObj.clean()['email'].strip()
                newUser.save()
                return HttpResponse('ok')
            else:
                return HttpResponseRedirect('/reg/')


def getModuleList(request):
    moduleList = []
    user = UserProfile.objects.get(id=request.user.id)
    for m in user.module_set.all():
        if m.parent != 0:
            continue
        temp = {}
        if m.parent == 0:
            temp['name'] = m.name
            temp['desc'] = m.desc
            temp['child'] = []
            childModules = user.module_set.all().filter(parent=m.id)
            if len(childModules) == 0:
                continue
            for c in childModules:
                t={}
                t['name'] = c.name
                t['desc'] = c.desc
                temp['child'].append(t)
                # print (c.id)
            moduleList.append(temp)
    return moduleList