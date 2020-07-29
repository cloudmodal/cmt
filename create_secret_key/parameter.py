#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from create_secret_key.key import HandleCredentials


def get_arg():
    """获取参数"""
    arg = argparse.ArgumentParser(add_help=False)
    arg.argument_default=argparse.SUPPRESS
    arg.prog = 'CMT'
    # arg.usage = '%(prog)s [options]'
    arg.usage = 'python [options]'
    arg.description = 'This is a Convenient Migration Tool'

    # 添加参数
    arg.add_argument('-V', '--version', action='version', version='%(prog)s 1.0')
    arg.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    arg.add_argument('-cp', '--copy',help='Copy files [source... directory]', type=str, nargs=2, metavar='PATH',
                     dest='copy')
    arg.add_argument('-d', '--download',help='Download file [source... directory]', type=str, nargs=2,
                     metavar='PATH', dest='download')

    arg.add_argument('-configure', help='Set Up Your Credentials', nargs='?', const='cmt', dest='config')

    return arg.parse_args()


def use_fun():
    try:
        arg = get_arg()
        arg = vars(arg)
        # print(arg)
        # print(type(arg))

        if 'copy' in arg:
            # TODO:待填充
            pass
            # copy_source_fun(arg[0])

        elif 'download' in arg:
            # TODO:待填充
            pass
            # down_source_fun(arg[0], arg[1])

        elif 'config' in arg:
            if arg['config'] == 'cmt':
                # 生成文件 .cmt/credentials
                handle = HandleCredentials()
                handle.handle_main()

            elif arg['config'] == 'all':
                print('Configure AWS Credentials...' + '* '*24)
                os.system('aws configure')
                print('Configure ALI Credentials...' + '* '*24)
                os.system('aliyun configure')

            elif arg['config'] == 'aws':
                os.system('aws configure')

            elif arg['config'] == 'ali':
                os.system('aliyun configure')

            elif arg['config'] == 'baidu':
                pass
            elif arg['config'] == 'tencent':
                pass

    except Exception as e:
        print(__file__)
        print(e)






