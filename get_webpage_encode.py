# coding:utf-8
__author__ = 'xxj'

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def page_encode(response):
    '''
    获取网页的编码类型
    :param response:
    :return:
    '''
    search_obj = re.search(r'<meta.*?charset="?(.*?)"', response.text, re.S)
    if search_obj:
        charset = search_obj.group(1)    # 获取到的网页的编码类型
        response.encoding = charset
    else:
        content = ''
        print '解析新的页面编码meta字符串'
        return content


def main():
    page_encode()


if __name__ == '__main__':
    main()

