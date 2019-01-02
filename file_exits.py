# coding:utf-8
__author__ = 'xxj'

import time
import os

# 文件读取重试机制

LOOP = True

# gaode_file_path = os.getcwd()  # Windows和测试机210中高德源数据目录
# gaode_file_name = os.path.join(gaode_file_path, 'gd_20180703_1.txt')  # Windows高德源数据文件路径
# gaode_file = open(gaode_file_name, 'r')

while LOOP:
    time.sleep(1)
    gaode_file_path = '/ftp_samba/112/file_4spider/gd_location'  # 线上高德源数据文件目录
    gaode_file_name = os.path.join(gaode_file_path, 'gd_{date}_1.txt'.format(date=date))  # 线上高德源数据文件路径
    if os.path.exists(gaode_file_name):
        LOOP = False

gaode_file = open(gaode_file_name, 'r')    # 存在该文件之后，开始读取该文件