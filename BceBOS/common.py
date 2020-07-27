#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: gxs
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: dingjianfeng@light2cloud.com
@software: AWS-DJF
@file: common.py
@ide: PyCharm
@time: 2020/7/23 11:00
@desc：
"""
import logging
import os
import sys
import time
import datetime
import hashlib
import base64
from configparser import ConfigParser, RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

LOG_DIR = os.path.join(BASE_DIR, 'logs')
# BOS_LOG_FILE = os.path.join(LOG_DIR, 'bos_to_s3_all.log')
# BOS_LOG_FILE_ERROR = os.path.join(LOG_DIR, 'bos_to_s3_warning.log')
# BOS_LOG_Danger = os.path.join(LOG_DIR, 'data_danger.log')

__all__ = [
    'get_config', 'get_logger',
    'get_time', 'get_time_utc',
    '_read_bos_file_size', '_count_md5'
]


def get_config() -> dict:
    """
    读取配置文件
    """
    config_file = os.path.join(BASE_DIR, 'config.ini')

    if not os.path.exists(config_file):
        config_file += '.default'
        print(f'自定义配置文件：{config_file}不存在，读取默认配置')

    cfg = ConfigParser()
    print(1, f'Reading config file: {config_file}')

    try:
        cfg.read(config_file, encoding='utf-8-sig')
        BCE_ACCESS_KEY_ID = cfg.get('BceDownloadBasic', 'BCE_ACCESS_KEY_ID')
        BCE_SECRET_ACCESS_KEY = cfg.get('BceDownloadBasic', 'BCE_SECRET_ACCESS_KEY')
        BCE_BOS_HOST = cfg.get('BceDownloadBasic', 'BCE_BOS_HOST')
        BCE_STS_HOST = cfg.get('BceDownloadBasic', 'BCE_STS_HOST')
        BOS_SRC_BUCKET = cfg.get('BceDownloadBasic', 'BOS_SRC_BUCKET')
        BOS_STORAGE_CLASS = cfg.get('BceDownloadBasic', 'BOS_STORAGE_CLASS')
        BOS_DES_DIR = cfg.get('BceDownloadBasic', 'BOS_DES_DIR')
        LOGGING_LEVEL = cfg.get('BceAdvanced', 'LOGGING_LEVEL')
        # BCE_ACCESS_KEY_ID(cfg.get('BceDownloadBasic', 'BCE_ACCESS_KEY_ID'))
        # BCE_SECRET_ACCESS_KEY(cfg.get('BceDownloadBasic', 'BCE_SECRET_ACCESS_KEY'))
        # BCE_BOS_HOST(cfg.get('BceDownloadBasic', 'BCE_BOS_HOST'))
        # BCE_STS_HOST(cfg.get('BceDownloadBasic', 'BCE_STS_HOST'))
        # BOS_SRC_BUCKET(cfg.get('BceDownloadBasic', 'BOS_SRC_BUCKET'))
        # BOS_STORAGE_CLASS(cfg.get('BceDownloadBasic', 'BOS_STORAGE_CLASS'))
        # BOS_PREFIX(cfg.get('BceDownloadBasic', 'BOS_PREFIX'))
        # BOS_DES_DIR(cfg.get('BceDownloadBasic', 'BOS_DES_DIR'))
        # LOGGING_LEVEL(cfg.get('BceAdvanced', 'LOGGING_LEVEL'))

    except Exception as e:
        print("加载 config.ini 出现异常错误:", str(e))
        input('按回车退出')
        sys.exit(0)

    else:
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
    return config


# def BCE_ACCESS_KEY_ID(BCE_ACCESS_KEY_ID):
#     return BCE_ACCESS_KEY_ID
#
#
# def BCE_SECRET_ACCESS_KEY(BCE_SECRET_ACCESS_KEY):
#     return BCE_SECRET_ACCESS_KEY
#
#
# def BCE_BOS_HOST(BCE_BOS_HOST):
#     return BCE_BOS_HOST
#
#
# def BCE_STS_HOST(BCE_STS_HOST):
#     return BCE_STS_HOST
#
#
# def BOS_SRC_BUCKET(BOS_SRC_BUCKET):
#     return BOS_SRC_BUCKET
#
#
# def BOS_STORAGE_CLASS(BOS_STORAGE_CLASS):
#     return BOS_STORAGE_CLASS
#
#
# def BOS_PREFIX(BOS_PREFIX):
#     if BOS_PREFIX == '/':
#         BOS_PREFIX = ''
#         print("BOSPrefix", BOS_PREFIX)
#     return BOS_PREFIX
#
#
# def BOS_DES_DIR(BOS_DES_DIR):
#     return BOS_DES_DIR
#
#
# def LOGGING_LEVEL(LOGGING_LEVEL):
#     return LOGGING_LEVEL


def get_logger(name=None) -> logging.getLogger:
    """
    10(DEBUG),20(INFO),30(WARNING),40(ERROR),50(CRITICAL)
    :param name:
    :return:
    """
    _logging = logging.getLogger('%s' % name)

    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    formatter_file = logging.Formatter('%(asctime)s [%(module)s, %(process)d:%(thread)d] '
                                       '%(levelname)s - %(message)s',
                                       datefmt="%Y-%m-%d %H:%M:%S")
    formatter_stream = logging.Formatter('%(asctime)s %(name)s: [line:%(lineno)d] '
                                         '%(levelname)s - %(message)s',
                                         datefmt="%Y-%m-%d %H:%M:%S")
    # _logging.setLevel(10)
    # """写入日志文件, 大等于20(INFO)的日志被写入"""
    # fh = logging.FileHandler(BOS_LOG_FILE, mode='a', encoding='utf8')
    # fh.setLevel(20)
    # fh.setFormatter(formatter_file)
    #
    # """写入日志文件, 大等于30(WARNING)的日志被写入"""
    # fh_error = logging.FileHandler(BOS_LOG_FILE_ERROR, mode='a', encoding='utf8')
    # fh_error.setLevel(30)
    # fh_error.setFormatter(formatter_file)
    #
    # """写入日志文件, 大等于50(CRITICAL)的日志被写入"""
    # fh_critical = logging.FileHandler(BOS_LOG_Danger, mode='a', encoding='utf8')
    # fh_critical.setLevel(50)
    # fh_critical.setFormatter(formatter_file)
    #
    # """输出到终端"""
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # ch.setFormatter(formatter_stream)

    """输出到文件"""
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    file_time = datetime.datetime.now().isoformat().replace(':', '-')[:19]
    log_file_name = os.path.join(LOG_DIR, file_time + '.log')
    fh = logging.FileHandler(log_file_name, mode='a', encoding='utf8')
    fh.setFormatter(formatter_file)

    """输出到终端"""
    ch = logging.StreamHandler()
    ch.setFormatter(formatter_stream)

    """设置Level"""
    LoggingLevel = get_config()["LOGGING_LEVEL"]
    if LoggingLevel == 'INFO':
        _logging.setLevel(20)
    elif LoggingLevel == 'WARNING':
        _logging.setLevel(logging.WARNING)
    elif LoggingLevel == 'ERROR':
        _logging.setLevel(40)
    elif LoggingLevel == 'CRITICAL':
        _logging.setLevel(50)
    else:
        _logging.setLevel(10)

    """向 _logging 添加handler """
    _logging.addHandler(fh)
    # _logging.addHandler(fh_error)
    # _logging.addHandler(fh_critical)
    _logging.addHandler(ch)
    return _logging


def get_time(day: int = 0, hour=0, minute=0, second=0, get_time_type=None):
    """
    计算当前本地时间
    :param day:
    :param hour:
    :param minute:
    :param second:
    :param get_time_type:
    :return:
    """

    bj_now_time = datetime.datetime.now().replace(tzinfo=None)
    if get_time_type == "time_stamp":
        now_tm = (bj_now_time + datetime.timedelta(
            days=day, hours=hour, minutes=minute, seconds=second
        )).strftime("%Y-%m-%d %H:%M:%S")
        time_array = time.strptime(now_tm, "%Y-%m-%d %H:%M:%S")
        return_tm = str(int(time.mktime(time_array)))
    elif get_time_type == "time_stamp_sf":
        return_tm = (bj_now_time + datetime.timedelta(
            days=day, hours=hour, minutes=minute, seconds=second)).strftime("%Y-%m-%d %H:%M:%S")
    elif get_time_type == "time_stamp_sp":
        return_tm_sf = (bj_now_time + datetime.timedelta(
            days=day, hours=hour, minutes=minute, seconds=second)).strftime("%Y-%m-%d %H:%M:%S")
        return_tm = datetime.datetime.strptime(return_tm_sf, '%Y-%m-%d %H:%M:%S')
    else:
        return_tm = bj_now_time
    return return_tm


def get_time_utc(day: int = 0, hour=0, minute=0, second=0, get_time_type=None):
    """
    计算当前 UTC 时间
    :param day:
    :param hour:
    :param minute:
    :param second:
    :param get_time_type:
    :return:
    """
    if get_time_type == "time_stamp":
        now_tm = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=day, hours=hour, minutes=minute, seconds=second
        )).strftime("%Y-%m-%d %H:%M:%S")
        time_array = time.strptime(now_tm, "%Y-%m-%d %H:%M:%S")
        return_tm = str(int(time.mktime(time_array)))
    elif get_time_type == "time_stamp_sp":
        return_tm_sf = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=day, hours=hour, minutes=minute, seconds=second)).strftime("%Y-%m-%d %H:%M:%S")
        return_tm = datetime.datetime.strptime(return_tm_sf, '%Y-%m-%d %H:%M:%S')
    elif get_time_type == "time_stamp_sf":
        """创建RDS快照；"""
        # TODO：后续可以替换创建AMI中的时间参数
        return_tm = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=day, hours=hour, minutes=minute, seconds=second)).strftime("%Y-%m-%d-%H%M")
    else:
        """复制AMI；启动EC2；"""
        # datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        return_tm = datetime.datetime.now(datetime.timezone.utc)
    return return_tm


def _read_bos_file_size(size_list: list) -> str:
    """
    计算对象数据大小
    :param size_list:
    :return:
    """
    size_sum = 0
    for n in size_list:
        size_sum = size_sum + n
    size_sum_gb = size_sum / (1024 * 1024 * 1024)
    size_sum_gb = ("%.5f" % size_sum_gb)
    return size_sum_gb


def _count_md5(file_name) -> list:
    """
    计算单个对象数据的 MD5 值
    :param file_name:
    :return:
    """
    buf_size = 8192
    with open(file_name, 'rb') as fp:
        file_md5 = hashlib.md5()
        while True:
            bytes_to_read = buf_size
            buf = fp.read(bytes_to_read)
            if not buf:
                break
            file_md5.update(buf)
        etag = file_md5.hexdigest()
    content_md5 = str(base64.standard_b64encode(file_md5.digest()), encoding='utf-8')
    return [content_md5, etag]


if __name__ == '__main__':
    get_logger = get_logger()
