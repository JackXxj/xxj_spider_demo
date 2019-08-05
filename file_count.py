# coding:utf-8 
__author__ = 'xxj'

import sys
import time
import math

reload(sys)
sys.setdefaultencoding('utf-8')


def file_count(source_file_path):
    '''
    统计文件行数
    :param source_file_path: 来源文件
    :return:
    '''
    source_file_obj = open(source_file_path, 'rb')
    # print source_file_obj.readlines()
    for count, line in enumerate(source_file_obj):
        pass
    count += 1
    print '该文件的行数：', count

    source_file_obj.close()
    print source_file_obj.closed

# 统计文本行数不要使用f.readlines()，因为它将文件存储在内存当中，当文件非常大时，非常消耗内存，导致memory error(内存溢出错误)
# 可以使用for循环统计文件行数，因为文件对象是迭代对象，大大减少了对内存的消耗。
# 注意：
    # 1、不管是使用readlines()还是for循环方法读文件，文件都不会自动关闭，需要f.close()实现文件关闭  【只有 with 能实现文件结束后自动关闭】
    # 2、可以通过f.closed属性查看文件的关闭状态（Ture为关闭；False为未关闭）


# 分割文件（有时候文件太大，所以会按一定量对文件进行分割输出）
# 方法一：
    # 首先对文件进行行数的统计，然后进行按一定量进行文件的分割，获取分割次数
def file_split_count(source_file_path, file_line_num):
    '''
    统计拆分文件的次数
    :param source_file_path: 来源文件
    :param file_line_num: 拆分文件的行数
    :return:
    '''
    source_file_obj = open(source_file_path, 'r')
    for count, line in enumerate(source_file_obj):
        pass
    count += 1
    print '该文件的行数：', count
    file_split_num = int(math.ceil(count/float(file_line_num)))     # 文件分割次数
    print '文件分割次数：', file_split_num
    return file_split_num


# 然后按分割次数对文件进行分割
def flie_handler(source_file_path, file_line_num):
    '''
    拆分文件
    :param source_file_path: 来源文件路径
    :param file_line_num: 每个分割文件的行数
    :return:
    '''
    # file_split_num = file_split_count(source_file_path, file_line_num)
    source_file_obj = open(source_file_path, 'r')
    count = 1    # 分割计数
    file_count = 1    #
    dest_file_obj = open(r'C:\Users\xj.xu\Desktop\ww\ww{}'.format(file_count), 'w')  # 每次循环都会产生一个文件对象
    for index, line in enumerate(source_file_obj):
        line = line.strip()
        if count <= file_line_num:
            dest_file_obj.write(line)
            dest_file_obj.write('\n')
            dest_file_obj.flush()
            count += 1

        else:
            file_count += 1
            dest_file_obj.close()
            dest_file_obj = open(r'C:\Users\xj.xu\Desktop\ww\ww{}'.format(file_count), 'w')    # 针对节点值的优化（不然节点值会丢失相关源数据）
            dest_file_obj.write(line)
            dest_file_obj.write('\n')
            dest_file_obj.flush()
            count = 2    # 保证后续文件行数一定，就是file_line_num值

    if dest_file_obj.closed is False:
        dest_file_obj.close()


def readPredictData(data_path):
    # 打开txt文件
    num = 0
    hive_data = []
    open_data_file = open(data_path, 'r')
    try:
        for line in open_data_file:
            num = num + 1
            if num <= 100:    # 1000001
                line = line.strip()
                # line_ls = line.split('\t')
                hive_data.append(line)

            else:
                line = line.strip()
                print(len(hive_data))
                num = 1
                hive_data = []
                hive_data.append(line)
        print(len(hive_data))
    finally:
        open_data_file.close()


def main():
    source_file_path = r'C:\Users\xj.xu\Desktop\data_20196251431.txt'
    # file_count(source_file_path)
    # file_split_count(source_file_path, 10)
    # flie_handler(source_file_path, 100)
    readPredictData(source_file_path)


if __name__ == '__main__':
    print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'start'
    main()
    print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'end'

