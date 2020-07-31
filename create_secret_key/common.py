#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import getpass


class Common:
    """
    common methed
    """
    def __init__(self):
        pass

    def create_folder(self, path):
        os.mkdir(path)

    def file_exist(self, path):
        return os.path.exists(path)








