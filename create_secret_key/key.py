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
                self.modify_platform_credentials(credentials_path)

        # elif s == 'Linux' or s == 'Darwin':
        #     # /home/username/.cmt
        #     lin = CreateUnixKey()

    # 修改凭证文件
    def modify_platform_credentials(self, path):

        try:
            with open(path, 'r+') as wr:
                sx = wr.readlines()
                # print(sx)
                wr.seek(0, 0)
                wr.truncate()

                for i in sx:
                    if i[:-1] == '[aws default]' or i[:-1] == '[ali default]' \
                            or i[:-1] == '[BceDownloadBasic]':
                        print(i[:-1])
                        wr.write(i[:-1] + '\n')

                    elif i[:-1] == 'Default Output Format [json]: json (Only support json)':
                        print(i[:-1])
                        wr.write(i[:-1] + '\n')

                    elif i[:-4] == 'Default Language [zh|en] =':
                        out = i.split('=')
                        x = out[0] + out[1][:-1] + ' = '
                        cred = input(x)
                        c = 'en' if cred != 'zh' and cred != 'en' else cred
                        data = i[:-4] + ' ' + c + '\n'
                        wr.write(data)

                    elif i == '\n':
                        print()
                        wr.write('\n')

                    else:
                        out = i.split('=')
                        cred = input(out[0] + '[' + out[1].strip() + '] = ')
                        data = out[0] + '= ' + cred + '\n'
                        wr.write(data)

            print('ok')
        except Exception as e:
            print(e)

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

                        elif i[:-1] == 'Default Language [zh|en] =':
                            # default en
                            cred = input(i[:-1] + ' ')
                            c = 'en' if cred != 'zh' and cred != 'en' else cred
                            data = i[:-1] + ' ' + c + '\n'
                            wr.write(data)

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
