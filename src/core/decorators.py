# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: decorators.py
@time: 2016/5/26 14:06
"""
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, FieldDoesNotExist

def requireLogin(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return wrapper

def requireLoginForbidden(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper

def requireModulePermission(func):
    def wrapper(request, *args, **kwargs):
        from core.models import module
        from django.contrib.auth import logout
        try:
            moduleObj = module.objects.get(name=request.GET.get('ac'))
            cu = moduleObj.user.get(username=request.user.username)
            if not cu:
                logout(request)
                return HttpResponseRedirect('/login')
            else:
                return func(request, *args, **kwargs)
        except Exception as e:
            return HttpResponseRedirect('/')
    return wrapper