#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: gxs
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: dingjianfeng@light2cloud.com
@software: AWS-DJF
@file: upload.py
@ide: PyCharm
@time: 2020/7/23 11:01
@desc：
"""
import os
from baidubce.exception import BceError
from initialization import BceAuthentication


class BceBOSUpload(BceAuthentication):

    def __init__(self):
        super().__init__()

    def upload_file_to_bos(self, file):
        """
        BOS储存类型: # 标准存储	STANDARD | 低频存储 STANDARD_IA | 冷存储 COLD | 归档存储	ARCHIVE

        :param file_lists:
        :return:
        """
        bos_client = self.get_bce_connection()
        print(file)
        print(os.path.basename(file))
        try:
            response = bos_client.put_object_from_file(
                bucket=self.bos_src_bucket,
                file_name=file,
                key=os.path.basename(file),
                # storage_class=self.bos_storage_class,
            )
            self.logger.info(f'文件：{file} 上传到 BOS 存储桶成功')

        except BceError as e:
            self.logger.error('本地数据上传到 BOS 存储桶时，发生错误 {}'.format(e))
            return []

        return response

if __name__ == '__main__':
    bos = BceBOSUpload()
    print(bos.__dict__)
    bos.upload_file_to_bos('E:\Python\l2c\S3Migration\ConvenientMigrationTool\BceBOS\/test.py')