# coding:utf-8
__author__ = 'xxj'

import requests
import time
import re
import json
import Queue
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PROXY_IP_Q = Queue.Queue()    # 代理ip队列

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }


# 使用代理ip的重试次数demon（单线程）
def get_proxy_ip():
    '''
    获取单个代理ip（主要是由于当过早提取出代理ip未使用，出现代理ip失效的问题）
    :return:
    '''
    try:
        url = 'https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=860068921904605585&num={num}&http_type=3&result_fields=1,2,3&result_format=json'.format(num=1)
        response = requests.get(url=url, headers=headers, timeout=10)
        ip_list = json.loads(response.text).get('result')
        if not ip_list:
            print '代理ip接口获取频繁：', response.text
            content_json = response.json()
            code_msg = content_json.get('code_msg')  # 异常信息
            code_msg = code_msg.encode('utf-8')
            search_obj = re.search(r'.*?，【(.*?)秒】', code_msg, re.S)
            stop_time = search_obj.group(1)
            stop_time = int(stop_time)
            print '代理ip接口限制,限制时间为：', stop_time, '秒'
            time.sleep(stop_time)
            return get_proxy_ip()
        result = ip_list[0]
        ip = result.get('ip:port')
        proxies = {
            'http': "http://8c84700fa7d2:kgvavaeile@{ip}".format(ip=ip)
        }
        return proxies
    except BaseException as e:
        print 'BaseException：', '代理ip请求异常'
        time.sleep(60)
        return get_proxy_ip()


proxies = get_proxy_ip()
print '首次获取到的代理ip：', proxies


def get(url, count):
    global proxies
    for i in xrange(count):
        r = res(url, count)
        if r:
            return r
        time.sleep(5)    # 可调整
    proxies = get_proxy_ip()
    print '代理ip失效，切换代理ip：', proxies
    return get(url, count)


def res(url, count):
    s = requests.session()
    s.adapters.DEFAULT_RETRIES = 10
    s.headers.update(headers)
    try:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), url, proxies, count
        r = s.get(url=url, headers=headers, proxies=proxies, timeout=10)    # 可调整timeout值
    except BaseException as e:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'BaseException', e.message
        return None
    else:
        return r


# 解决上个文件的那些问题

# 该文件还有一个问题：记得区分请求成功但是ip未返回  和  请求失败的处理（这种方式对于请求失败是会报错的，因为response.json()会出现异常）【已解决】


# 使用代理ip的重试次数demon（多线程）

def get_proxy_ips(num):
    '''
    获取代理ip,将代理ip放入PROXY_IP_Q队列中
    :return:
    '''
    try:
        url = 'https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=860068921904605585&num={num}&http_type=3&result_fields=1,2,3&result_format=json'.format(num=num)
        response = requests.get(url=url, headers=headers, timeout=10)
        ip_list = json.loads(response.text).get('result')
        if not ip_list:
            print '代理ip接口请求过于频繁：', response.text
            content_json = response.json()
            code_msg = content_json.get('code_msg')  # 异常信息
            code_msg = code_msg.encode('utf-8')
            search_obj = re.search(r'.*?，【(.*?)秒】', code_msg, re.S)
            stop_time = search_obj.group(1)
            stop_time = int(stop_time)
            print '代理ip接口限制,限制时间为：', stop_time, '秒'
            time.sleep(stop_time)
            return get_proxy_ips(num)
        for ip in ip_list:
            ip = ip.get('ip:port')
            proxies = {
                # 'http': "http://{ip}".format(ip=ip)    # 8c84700fa7d2:kgvavaeile@
                'http': "http://8c84700fa7d2:kgvavaeile@{ip}".format(ip=ip)
            }
            PROXY_IP_Q.put(proxies)
    except BaseException as e:
        print 'BaseException：', '代理ip请求异常'
        time.sleep(60)
        return get_proxy_ips(num)


# 对于代理ip请求而言：一种是代理ip接口过于频繁导致的重试；一种是代理ip请求异常导致的重试