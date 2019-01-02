# coding:utf-8
__author__ = 'xxj'
'''
针对单线程的请求失败重试机制。当然也可以使用retry模块

'''

import requests
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


def get(url, count, url_des):
    for i in xrange(count):
        response = r(url, i, url_des)
        if response is None:    # 异常
            pass
        elif response.status_code == 200:
            return response
        elif response.status_code == 404:
            print '响应状态码是404'
            return None
    return None


def r(url, i, url_des):
    try:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), url_des, url, 'count：', i
        response = requests.get(url=url, headers=headers, timeout=10)
    except BaseException as e:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'BaseException', 'url：', url
        response = None
        time.sleep(2)
    return response