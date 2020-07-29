#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: gxs
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: dingjianfeng@light2cloud.com
@software: AWS-DJF
@file: download.py
@ide: PyCharm
@time: 2020/7/23 11:01
@desc：
"""
import os
import pathlib

from baidubce.exception import BceError
from .initialization import BceAuthentication
from .common import _read_bos_file_size, _count_md5


class BceBOSDownload(BceAuthentication):

    def __init__(self):
        super().__init__()

    def main_function(self):
        """
        max_keys=1000
        :return:
        """
        bos_client = self.get_bce_connection()

        try:
            # 'd/2eeQ7f', 'd/1442413150028', 'd/1442754128155', 'd/1444316556440', 'd/jieINz', 'd/yayYVv'
            # file_directory_list = [
            #                        'd/sinldo/bbsy/jk7oxTbYvqiq/1', 'd/sinldo/trsrmyy/XOq7eNQbyEJz/2',
            #                        'd/sinldo/yzrmyy/Pu5WmamyMfYj/3', 'd/sinldo/yzrmyy/QCYljhbqaYR3/4']   # 归档
            file_directory_list = ['d/2eeQ7f', 'c/1442413150028']

            """存放被遍历目录下所有子文件夹的列表"""
            sub_folder_list = []
            """存放被遍历目录下所有文件的列表"""
            file_list = []
            size_list = []
            for _dir_list in file_directory_list:
                marker = None
                is_truncated = True
                while is_truncated:

                    response = bos_client.list_objects(bucket_name=self.bos_src_bucket,
                                                       max_keys=1000,
                                                       prefix=_dir_list,
                                                       marker=marker)
                    for object in response.contents:
                        if object.size == 0 and object.key[-1] == '/':
                            sub_folder_list.append(object.key)
                        else:
                            file_list.append(object.key)
                            size_list.append(object.size)
                    is_truncated = response.is_truncated
                    marker = getattr(response, 'next_marker', None)

                if sub_folder_list:
                    self.makedir_directory_from_bos(file_directory_list, sub_folder_list)
                else:
                    self.makedir_directory_from_bos(file_directory_list,)
                self.logger.warning(f'从 BOS 存储桶读取文件总数量：{len(file_list)} ')
                self.logger.warning(f'从 BOS 存储桶读取文件总大小：{_read_bos_file_size(size_list)} GB ')
                if _read_bos_file_size(size_list) <= str(700):
                    return self.download_file_from_bos(bos_client, file_list, file_directory_list)
                else:
                    self.logger.warning(f'从 BOS 存储桶读取文件总大小超过 700 GB')

        except BceError as e:
            self.logger.error('从 BOS 存储桶读取文件详情时，发生错误 {}'.format(e))
            return []

    def makedir_directory_from_bos(self, directories: list, sub_folders: list = None):
        try:
            if sub_folders:
                for directory in directories:
                    if not os.path.isdir(directory):
                        os.makedirs(directory)
                for sub_folder in sub_folders:
                    if not os.path.isdir(sub_folder):
                        os.makedirs(sub_folder)
            else:
                for directory in directories:
                    if not os.path.isdir(directory):
                        os.makedirs(directory)
        except FileExistsError as e:
            self.logger.error('创建对应的多级目录时，发生错误 {}'.format(e))

    def download_file_from_bos(self, bos_client, file_lists: list, file_directory_list: list):
        """
        :param bos_client:
        :param file_lists: list BOS 数据列表
        :param file_directory_list: CSV 路径列表
        :return:
        """
        try:
            for file in file_lists:
                path = pathlib.Path(file)
                if path.is_file():
                    pass
                    # self.logger.info(f'BOS 存储桶中的文件：{file} 在本地存在，不执行下载操作')
                else:
                    if not os.path.isdir(os.path.dirname(file)):
                        os.makedirs(os.path.dirname(file))
                    if bos_client.get_object_meta_data(bucket_name=self.bos_src_bucket,
                                                       key=file).metadata.bce_storage_class == 'ARCHIVE':
                        self.logger.critical(f'BOS 归档文件：{file} ')
                        continue
                    response = bos_client.get_object_to_file(
                        bucket_name=self.bos_src_bucket,
                        key=file,
                        file_name=file,
                    )
                    # self.logger.info(f'BOS 存储桶中的文件：{file} 下载到本地')

                    content_md5 = response.metadata.content_md5
                    self.check_file_md5(bos_client=bos_client, file_name=file, file_content_md5=content_md5,
                                        file_directory_list=file_directory_list)

        except BceError as e:
            self.logger.error(f'从 BOS 存储桶下载文件 时，发生错误 {e}')
            return []

        except Exception as e:
            self.logger.exception(f'从 BOS 存储桶下载文件时，发生错误 {e} ')
            return []

    def check_file_md5(self, bos_client, file_name: str, file_content_md5: str, file_directory_list: list):
        """
        :param bos_client:
        :param file_name:
        :param file_content_md5:
        :param file_directory_list:
        :return:
        """
        md5 = _count_md5(file_name)
        if file_content_md5 == md5[0]:
            self.logger.info(f'下载、校验文件：{file_name} 完成，数据完整，content_md5：{file_content_md5} ')
        else:
            self.logger.warning(f'下载校验文件：{file_name} 发现数据损坏..... 原始 content_md5：{file_content_md5} '
                                f'下载后 content_md5：{md5[0]} ')
            # TODO： 校验失败处理


if __name__ == '__main__':
    bos = BceBOSDownload()
    bos.main_function()