# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: getpage.py
@time: 2016/4/27 16:11
"""

from django import template

register = template.Library()
def tolist(current, max):
    try:
        current = int(current)
        max = int(max)
        li = []
        if max < 8:
            for i in range(max):
                li.append(i+1)
        else:
            if current <= 4:
                li = [1,2,3,4,5,6,7]
            else:
                if max - current <= 3:
                    li = [max-6, max-5, max-4, max-3, max-2, max-1, max]
                else:
                    li = [current-3,current-2, current-1,current, current+1, current+2, current+3]

        # if current <= 4:
        #     if max < 8:
        #         for i in range(max):
        #             li.append(i+1)
        #     else:
        #         if max - current <= 3:
        #             li = [max-6, max-5, max-4, max-3, max-2, max-1, max]
        #         else:
        #               for i in range(7):
        #                   li.append(i+1)
        # else:
        #     if max < 8:
        #         for i in range(max):
        #             li.append(i+1)
        #     else:
        #         if max - current <= 3:
        #             li = [max-6, max-5, max-4, max-3, max-2, max-1, max]
        #         else:
        #             li = [current-3,current-2, current-1,current, current+1, current+2, current+3]
        return li
    except:
        return 'error'



register.filter(tolist)  #注册过滤器
