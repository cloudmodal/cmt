#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import getpass


class CreateWinKey:
    """
    Creating key under Windows
    """

    def __init__(self, path):
        self.user = getpass.getuser()
        self.path = path

    @property
    def key(self):
        return self.path

    @key.setter
    def key(self, value):
        pass

class CreateUnixKey:
    """
    Creating key under Linux/MAC
    """
    def __init__(self):
        pass


class Common:
    """
    common methed
    """
    def __init__(self):
        pass

    def create(self, path):
        pass

    def file_exist(self, path):
        return os.path.exists(path)


def create_credentials():

    s = platform.system()

    if s == 'Windows':
        path = os.path.join(r'C:\Users', getpass.getuser(), '.cmt')
        com = Common()
        
        if not com.file_exist(path):
            os.mkdir(path)
            with open(os.path.join(path, 'credentials'), 'w') as f:
                pass
            # os.mknod("credentials")
            print('okkk')
        else:
            pass

    # elif s == 'Linux' or s == 'Darwin':
    #     # /home/username/.cmt
    #     lin = CreateUnixKey()

# create_credentials()






