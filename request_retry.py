# coding:utf-8 
__author__ = 'xxj'

import time
import requests
import sys
import lxml.etree
import redis
import Queue
import re
import os
from jparser import PageModel
import json

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
PROXY_IP_Q = Queue.Queue()     # 代理ip队列
rc = redis.StrictRedis(host="172.31.10.75", port=9221)


class OtherException(Exception):
    def __init__(self, message):
        super(OtherException, self).__init__()
        self.message = message


class ResponseStatusCodeException(Exception):
    '''
    响应状态码异常
    '''
    def __init__(self, message):
        super(ResponseStatusCodeException, self).__init__()
        self.message = message


def get_redis_proxy():
    '''
    从redis相应的key中获取代理ip
    :return:
    '''
    kuai_proxy_length = rc.scard('spider:kuai:proxy')  # 快代理
    print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'redis中kuai的代理ip长度：', kuai_proxy_length
    if kuai_proxy_length == 0:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'redis中的代理ip数量为0，等待60s'
        time.sleep(60)
        return get_redis_proxy()
    kuai_proxy_set = rc.smembers('spider:kuai:proxy')    # 快代理集合
    for i, ip in enumerate(kuai_proxy_set):
        if i == 20:
            break
        else:
            PROXY_IP_Q.put(ip)


def retry_get(url, count, retry_time, url_des):
    global ip
    for i in xrange(count):
        response = retry_res(url, i, url_des)
        if response is None:
            if PROXY_IP_Q.empty():
                get_redis_proxy()
                ip_num = PROXY_IP_Q.qsize()
                print '代理ip为空，重新获取到的代理ip数量：', ip_num
            ip = PROXY_IP_Q.get(False)
            print '切换新的代理ip：', ip
            time.sleep(retry_time)
        else:
            return response
    return None


def retry_res(url, i, url_des):
    try:
        proxies = {
            'http': "http://{ip}".format(ip=ip),
            'https': "http://{ip}".format(ip=ip)
        }
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), url_des, url, '代理proxies：', proxies, 'count：', i
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=10)
        status_code = response.status_code
        if status_code == 200:
            pass
        else:
            print '其他类型响应状态码：', status_code
            response = None

        # response_text = response.text    # 针对响应内容的异常（如：出现验证码等情况的）
        # ****
        # ****

    except BaseException as e:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), '请求异常信息：', e.message, 'url：', url
        response = None
    return response



# 上面案例解析：
    # 1、retry_res模块：实现对请求异常、响应状态码异常等异常情况的捕获；
    # 2、retry_get模块：主要实现重试次数、重试请求之间的间隔、异常的处理方式：代理ip切换。



# 请求重试类型有： 1、请求异常重试；2、请求之后状态码异常重试；3、请求之后响应内容异常重试

# 该重试模块主要更加清晰地分离重试模块中的两大模块主要功能：
    # 1、retry_res模块：主要实现对需要进行重试的异常情况发生时的捕捉；
    # 2、retry_get模块：主要实现相应的重试机制以及异常的处理。
