#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import getpass
from create_secret_key.common import Common


class HandleCredentials:

    def __init__(self, resource=None):
        self.resource = resource

    def handle_main(self):
        s = platform.system()

        if s == 'Windows':
            credentials_path = os.path.join(r'C:\Users', getpass.getuser(), '.cmt\credentials')
            file = Common()

            if not file.file_exist(credentials_path):
                os.mkdir(os.path.join(r'C:\Users', getpass.getuser(), '.cmt'))
                self.create_platform_credentials(credentials_path)
            else:
                self.modify_platform_credentials()

        # elif s == 'Linux' or s == 'Darwin':
        #     # /home/username/.cmt
        #     lin = CreateUnixKey()

    def modify_platform_credentials(self):
        print('凭证已存在。。。')
        pass

    # 创建凭证文件
    def create_platform_credentials(self, path):

        # print(os.path.join(os.getcwd(), 'create_secret_key\credentials'))
        try:
            with open(os.path.join(os.getcwd(), 'create_secret_key\credentials'), 'r') as re:
                with open(path, 'w') as wr:
                    sx = re.readlines()

                    for i in sx:
                        if i[:-1] == '[aws default]' or i[:-1] == '[ali default]' \
                                or i[:-1] == '[BceDownloadBasic]':
                            print(i[:-1])
                            wr.write(i[:-1] + '\n')

                        elif i[:-1] == 'Default Output Format [json]: json (Only support json)':
                            print(i[:-1])
                            wr.write(i[:-1] + '\n')

                        elif i == '\n':
                            print()
                            wr.write('\n')

                        elif i[:-1] == '[end]':
                            print(i[:-1])

                        else:
                            cred = input(i[:-1] + ' ')
                            data = i[:-1] + ' ' + cred + '\n'
                            wr.write(data)

            print('ok')
        except Exception as e:
            print(e)


# if __name__ == "__main__":
#     b = HandleCredentials()
#     b.create_platform_credentials()
