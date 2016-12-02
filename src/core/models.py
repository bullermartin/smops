# -*- coding:utf-8 -*-
from django.db import models
from core.UserProfile import *

class host(models.Model):
    '''
        主机模型
    '''
    name = models.CharField(max_length=20, null=False, unique=True, verbose_name='主机名')
    desc = models.CharField(max_length=255, null=True, verbose_name='描述')
    ipaddr = models.GenericIPAddressField(protocol='ipv4',null=False, verbose_name='IP地址')
    prefix = models.IntegerField(null=False, default=32, verbose_name='网络位')
    port = models.IntegerField(null=False, default=22, verbose_name='端口')
    status = models.IntegerField(null=False, verbose_name='状态')
    add_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='添加时间')
    modify_time = models.DateTimeField(null=False, auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '主机'

    def __str__(self):
        return self.name

class sys_user(models.Model):
    '''
        系统用户模型
    '''
    username = models.CharField(max_length=20, null=False, verbose_name='用户名')
    password = models.CharField(max_length=20, null=False, verbose_name='密码')
    host = models.ForeignKey('host')
    user = models.ForeignKey(UserProfile)

    class Meta:
        verbose_name = '系统用户'
        unique_together = (('host', 'user'),)

    def __str__(self):
        return '系统用户'

class whitelist_event(models.Model):
    '''
        白名单事件模型
    '''
    operator = models.CharField(max_length=20,null=False, verbose_name='操作者')
    ipaddr = models.GenericIPAddressField(protocol='ipv4',null=False,verbose_name='IP地址')
    prefix = models.IntegerField(null=False, default=32, verbose_name='网络位')
    status = models.IntegerField(null=False, verbose_name='状态')
    src_ip = models.GenericIPAddressField(protocol='ipv4',null=False,verbose_name='来源IP')
    datetime = models.DateTimeField(null=False, auto_now=True, verbose_name='时间')
    operation = models.CharField(max_length=10,null=False, verbose_name='操作')
    desc = models.CharField(max_length=255,null=False, verbose_name='描述')

    class Meta:
        verbose_name = '白名单操作'

    def __str__(self):
        return self.ipaddr

class svn_user(models.Model):
    '''
        SVN账号模型
    '''
    name = models.CharField(max_length=20, null=False, unique=True, verbose_name='名称')
    host = models.ForeignKey('host')
    username = models.CharField(max_length=20, null=False, verbose_name='用户名')
    password = models.CharField(max_length=20, null=False, verbose_name='密码')
    class Meta:
        verbose_name = 'SVN账户'
        unique_together = (('host', 'username'),)

    def __str__(self):
        return self.name


class business(models.Model):
    '''
        业务模型
    '''
    name = models.CharField(max_length=20, null=False, unique=True, verbose_name='业务名')
    status = models.IntegerField(null=False, verbose_name='状态')
    start_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间')
    directory = models.CharField(max_length=255, null=False, verbose_name='业务目录')
    svn_dir = models.CharField(max_length=255, null=False, verbose_name='SVN目录')
    running_user = models.CharField(max_length=20, null=False, verbose_name='运行账户')
    current_version = models.CharField(max_length=100, null=False, default='1', verbose_name='当前版本')
    svn_user = models.ForeignKey(svn_user)
    host = models.ManyToManyField('host', through='business_host')

    class Meta:
        verbose_name = '业务'
        unique_together = (('svn_user','name'),)

    def __str__(self):
        return self.name


class business_host(models.Model):
    '''
        主机对应业务版本关系模型
    '''
    business = models.ForeignKey('business')
    host = models.ForeignKey('host')
    current_version = models.CharField(max_length=100, null=False, verbose_name='当前版本')

class module(models.Model):
    '''
        功能模块模型
    '''
    name = models.CharField(max_length=20, null=False, unique=True, verbose_name='名称')
    desc = models.CharField(max_length=255, null=True, verbose_name='描述')
    user = models.ManyToManyField(UserProfile)
    parent = models.IntegerField(null=True, default=0, verbose_name='父模块')

    class Meta:
        verbose_name = '功能模块'

    def __str__(self):
        return self.name

class publish_event(models.Model):
    '''
        版本发布事件模型
    '''
    operator = models.CharField(max_length=20, null=False, verbose_name='操作者')
    ipaddr = models.GenericIPAddressField(protocol='ipv4', null=False, verbose_name='来源IP')
    datetime = models.DateTimeField(auto_now_add=True, null=False, verbose_name='时间')
    original_ver = models.CharField(max_length=100, null=False, verbose_name='上一个版本')
    current_ver = models.CharField(max_length=100, null=False, verbose_name='当前版本')
    rollback_ver = models.CharField(max_length=100, null=True, verbose_name='回滚版本')
    status = models.IntegerField(null=False, verbose_name='状态')
    desc = models.CharField(max_length=255, null=False, verbose_name='描述')
    result = models.CharField(max_length=255, null=True, verbose_name='发布结果')
    class Meta:
        verbose_name = '版本发布事件'

    def __str__(self):
        return self.current_ver

