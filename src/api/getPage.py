# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: getPage.py
@time: 2016/4/26 18:10
"""
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
import logging

logger = logging.getLogger(__name__)

# 分页代码
def getPage(list, page, num):
    try:
        page = int(page)
        num = int(num)
        paginator = Paginator(list, num)  #以每页n条记录分页
        #获取第page页的所有对象
        if page > 0:
            content_list = paginator.page(page)
        else:
            content_list = paginator.page(1)
    except Exception as e:
        # logger.error(e)
        return False
    return content_list
