# -*- coding:utf-8 -*-
#!/usr/bin/env python


"""
@version: ??
@author: Ron
@software: PyCharm
@file: UserProfile.py
@time: 2016/5/17 16:35
"""
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserProfileManager(BaseUserManager):
    def create_user(self, username, name, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not name:
            raise ValueError('Users must have an name')
        if not name:
            raise ValueError('Users must have an password')

        user = self.model(
            username=username,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):

    username = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name='用户名')
    name = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name='姓名')
    email = models.EmailField(max_length=30,null=True, blank=True,unique=True,verbose_name='邮箱')
    desc =  models.CharField(null=True, blank=True,max_length=255, verbose_name='描述')
    # password = models.CharField(max_length=20, null=False, blank=False, verbose_name='密码')
    status = models.BooleanField(null=False, blank=False, default=0, verbose_name='状态')
    add_time = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name='创建时间')
    # last_login = models.DateTimeField(null=False, blank=False, auto_now=True, verbose_name='最近登录')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

    def __unicode__(self):
        return self.username

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin