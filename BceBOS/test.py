#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: gxs
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: dingjianfeng@light2cloud.com
@software: AWS-DJF
@file: test.py
@ide: PyCharm
@time: 2020/7/23 13:55
@desc：
"""
# import os
# import sys
# import platform
#
# def set_config():
#     sys_para = sys.argv
#     print(sys_para)
#     file_path = os.path.split(sys_para[0])[0]
#     gui = False
#     if platform.uname()[0] == 'Windows':  # Win默认打开
#         gui = True
#     if platform.uname()[0] == 'Linux':  # Linux 默认关闭
#         gui = False
#     if '--gui' in sys.argv:  # 指定 gui 模式
#         gui = True
#     if '--nogui' in sys.argv:  # 带 nogui 就覆盖前面Win打开要求
#         gui = False
#
# b= set_config()
# print(b)
#
# print
import datetime

file_time0 = datetime.datetime.now().isoformat()
file_time = datetime.datetime.now().isoformat().replace(':', '-')[:19]

print(file_time0)
print(file_time)