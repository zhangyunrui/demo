#!/bin/env python
# -*- coding:utf-8 -*-

import os
import re

# 获取路径
wd = os.getcwd()
# ls
dir_list = os.listdir(wd)

# 遍历文件夹
for d in dir_list:
    # 每个文件夹检查status，若status不是up-to-date，则更新
    try:
        os.chdir(d)
        git_status = os.popen('git status').read()
        if not re.search(r'up-to-date', git_status):
            print os.popen('git pull git@github.com:zhangyunrui/%s.git' % d).read()
        else:
            print '%s is up-to-date' % d
        os.chdir('..')
    except Exception as e:
        print str(e)


# todo 改成协程
