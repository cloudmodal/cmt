#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: gxs
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: dingjianfeng@light2cloud.com
@software: AWS-DJF
@file: initialization.py
@ide: PyCharm
@time: 2020/7/23 11:01
@desc：
"""
import os

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.sts.sts_client import StsClient
from baidubce.exception import BceError
from baidubce.services.bos.bos_client import BosClient
from baidubce.services.bos import storage_class
from .common import get_logger, get_config


class BceAuthentication:
    """
    config = {
        'BCE_ACCESS_KEY_ID': BCE_ACCESS_KEY_ID,
        'BCE_SECRET_ACCESS_KEY': BCE_SECRET_ACCESS_KEY,
        'BCE_BOS_HOST': BCE_BOS_HOST,
        'BCE_STS_HOST': BCE_STS_HOST,
        'BOS_SRC_BUCKET': BOS_SRC_BUCKET,
        'BOS_STORAGE_CLASS': BOS_STORAGE_CLASS,
        'BOS_DES_DIR': BOS_DES_DIR,
        'LOGGING_LEVEL': LOGGING_LEVEL
    }

    self.logger.debug('DEBUG')
    self.logger.info('INFO')
    self.logger.warning('WARNING')
    self.logger.error('ERROR')
    self.logger.critical('CRITICAL')

    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.bce_access_key_id = self.config['BCE_ACCESS_KEY_ID']
        self.bce_secret_access_key = self.config['BCE_SECRET_ACCESS_KEY']
        self.bce_bos_host = self.config['BCE_BOS_HOST']
        self.bce_sts_host = self.config['BCE_STS_HOST']
        self.bos_src_bucket = self.config['BOS_SRC_BUCKET']
        self.bos_storage_class = self.config['BOS_STORAGE_CLASS']
        self.bos_des_dir = self.config['BCE_SECRET_ACCESS_KEY']

    def _bce_access_key_id(self):
        bce_access_key_id = self.config['BCE_ACCESS_KEY_ID']
        return bce_access_key_id

    def _bce_secret_access_key(self):
        bce_secret_access_key = self.config['BCE_SECRET_ACCESS_KEY']
        return bce_secret_access_key

    def _bce_bos_host(self):
        bce_bos_host = self.config['BCE_BOS_HOST']
        return bce_bos_host

    def _bce_sts_host(self):
        bce_sts_host = self.config['BCE_STS_HOST']
        return bce_sts_host

    def _bos_src_bucket(self):
        bce_sts_host = self.config['BOS_SRC_BUCKET']
        return bce_sts_host

    def _bos_storage_class(self):
        bos_storage_class = self.config['BOS_STORAGE_CLASS']
        return bos_storage_class

    def _bos_des_dir(self):
        bos_des_dir = self.config['BOS_DES_DIR']
        return bos_des_dir

    def _bce_init_connection(self):
        try:
            bce_config = BceClientConfiguration(
                credentials=BceCredentials(
                    access_key_id=self.bce_access_key_id,
                    secret_access_key=self.bce_secret_access_key),
                endpoint=self.bce_bos_host)
            bos_client = BosClient(bce_config)
            return bos_client

        except BceError as e:
            self.logger.error('使用BCE当前凭证，在连接时发生错误 {}'.format(e))
            return []

        except Exception as e:
            self.logger.exception('使用BCE当前凭证，在连接时发生异常错误 {}'.format(e))
            return []

    def _bce_init_connection_sts(self):
        try:
            bce_config = BceClientConfiguration(
                credentials=BceCredentials(
                    access_key_id=self.bce_access_key_id,
                    secret_access_key=self.bce_secret_access_key),
                endpoint=self.bce_sts_host)
            sts_client = StsClient(bce_config)
            access_dict = {}
            duration_seconds = 3600
            access_dict["service"] = "bce:bos"
            access_dict["region"] = "bj"
            access_dict["effect"] = "Allow"
            resource = ["*"]
            access_dict["resource"] = resource
            permission = ["*"]
            access_dict["permission"] = permission

            access_control_dict = {"accessControlList": [access_dict]}
            response = sts_client.get_session_token(acl=access_control_dict, duration_seconds=duration_seconds)

            config = BceClientConfiguration(
                credentials=BceCredentials(str(response.access_key_id), str(response.secret_access_key)),
                endpoint=self.bce_bos_host,
                security_token=response.session_token)
            bos_client = BosClient(config)
            return bos_client

        except BceError as e:
            self.logger.error('使用BCE当前连接令牌，在连接时发生错误 {}'.format(e))
            return []

        except Exception as e:
            self.logger.exception('使用BCE当前连接令牌，在连接时发生异常错误 {}'.format(e))
            return []

    def get_bce_connection(self):
        if self.bce_access_key_id is not None and self.bce_sts_host is not None:
            bos_client = self._bce_init_connection_sts()
        else:
            bos_client = self._bce_init_connection()

        return bos_client

