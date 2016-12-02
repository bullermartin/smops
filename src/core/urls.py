# -#- coding=utf-8 -*-
"""tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from core.views import index, userLogin, userLogout, register
from core.generalobject_ops import *

urlpatterns = [
    url(r'^$', index),
    url(r'^login/$', userLogin),
    url(r'^logout/$', userLogout),
    url(r'^reg/$', register),

    # 用户管理
    url(r'^detail/user/$', userOperator, name='userdetail'),
    url(r'^detail/sysuser/$', sysUserOperator, name='sysuserdetail'),
    url(r'^detail/svnuser/$', svnUserOperator, name='svnuserdetail'),

    # 主机管理
    url(r'^detail/host/$', hostOperator, name='hostdetail'),

    # 白名单管理
    url(r'^detail/whitelist/$', whiteListOperator, name='whitelist'),

    # 版本管理
    url(r'^detail/version/$', versionOperator, name='versiondetail'),

    # 业务管理
    url(r'^detail/business/$', businessOperator, name='businessdetail'),

    # 模块管理
    url(r'^detail/module/$', moduleOperator, name='moduledetail'),

    # 其他

]
