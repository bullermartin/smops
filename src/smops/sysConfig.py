# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: sysConfig.py
@time: 2016/7/4 16:49
"""

sysConfig = {
    'perPageNum':10,
    'whiteListBusiness':'Admin',
    'whiteListPort':'80',
    'iptablesSplit':'White-List',   #这个字符串必须同时包含在whitelistStart和whitelistEnd中
    'whitelistStart':'White-List-Start',
    'whitelistEnd':'White-List-End',
    'maxVersionNum':5,  # 发布和回滚版本时的显示的最大版本数量
    'allowedBusinessDir':['/home/data','/data','/usr/local/nginx'],
}