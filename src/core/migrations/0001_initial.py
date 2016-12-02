# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 18:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='姓名')),
                ('email', models.EmailField(blank=True, max_length=30, null=True, unique=True, verbose_name='邮箱')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('status', models.BooleanField(default=0, verbose_name='状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='业务名')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('directory', models.CharField(max_length=255, verbose_name='业务目录')),
                ('svn_dir', models.CharField(max_length=255, verbose_name='SVN目录')),
                ('running_user', models.CharField(max_length=20, verbose_name='运行账户')),
                ('current_version', models.CharField(default='1', max_length=100, verbose_name='当前版本')),
            ],
            options={
                'verbose_name': '业务',
            },
        ),
        migrations.CreateModel(
            name='business_host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_version', models.CharField(max_length=100, verbose_name='当前版本')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.business')),
            ],
        ),
        migrations.CreateModel(
            name='host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='主机名')),
                ('desc', models.CharField(max_length=255, null=True, verbose_name='描述')),
                ('ipaddr', models.GenericIPAddressField(protocol='ipv4', verbose_name='IP地址')),
                ('prefix', models.IntegerField(default=32, verbose_name='网络位')),
                ('port', models.IntegerField(default=22, verbose_name='端口')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '主机',
            },
        ),
        migrations.CreateModel(
            name='module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('desc', models.CharField(max_length=255, null=True, verbose_name='描述')),
                ('parent', models.IntegerField(default=0, null=True, verbose_name='父模块')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '功能模块',
            },
        ),
        migrations.CreateModel(
            name='publish_event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(max_length=20, verbose_name='操作者')),
                ('ipaddr', models.GenericIPAddressField(protocol='ipv4', verbose_name='来源IP')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('original_ver', models.CharField(max_length=100, verbose_name='上一个版本')),
                ('current_ver', models.CharField(max_length=100, verbose_name='当前版本')),
                ('rollback_ver', models.CharField(max_length=100, null=True, verbose_name='回滚版本')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('desc', models.CharField(max_length=255, verbose_name='描述')),
                ('result', models.CharField(max_length=255, null=True, verbose_name='发布结果')),
            ],
            options={
                'verbose_name': '版本发布事件',
            },
        ),
        migrations.CreateModel(
            name='svn_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.host')),
            ],
            options={
                'verbose_name': 'SVN账户',
            },
        ),
        migrations.CreateModel(
            name='sys_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.host')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '系统用户',
            },
        ),
        migrations.CreateModel(
            name='whitelist_event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(max_length=20, verbose_name='操作者')),
                ('ipaddr', models.GenericIPAddressField(protocol='ipv4', verbose_name='IP地址')),
                ('prefix', models.IntegerField(default=32, verbose_name='网络位')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('src_ip', models.GenericIPAddressField(protocol='ipv4', verbose_name='来源IP')),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name='时间')),
                ('operation', models.CharField(max_length=10, verbose_name='操作')),
                ('desc', models.CharField(max_length=255, verbose_name='描述')),
            ],
            options={
                'verbose_name': '白名单操作',
            },
        ),
        migrations.AddField(
            model_name='business_host',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.host'),
        ),
        migrations.AddField(
            model_name='business',
            name='host',
            field=models.ManyToManyField(through='core.business_host', to='core.host'),
        ),
        migrations.AddField(
            model_name='business',
            name='svn_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.svn_user'),
        ),
        migrations.AlterUniqueTogether(
            name='sys_user',
            unique_together=set([('host', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='svn_user',
            unique_together=set([('host', 'username')]),
        ),
        migrations.AlterUniqueTogether(
            name='business',
            unique_together=set([('svn_user', 'name')]),
        ),
    ]
