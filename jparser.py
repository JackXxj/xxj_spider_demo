# coding:utf-8
__author__ = 'xxj'

'''
针对正文内容、图片、标题的提取（只限于python2）
'''

import requests
import re
import time
from jparser import PageModel    # jparser库只适合python2版本， 不兼容python3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


response = requests.get("http://newgame.duowan.com/1508/303904283898.html")
search_obj = re.search(r'<meta.*?charset="?(.*?)"', response.text, re.S)
if search_obj:
    charset = search_obj.group(1)
    response.encoding = charset
else:
    content = ''
    print '解析新的页面编码meta字符串'

start_time = time.time()
pm = PageModel(response.text)
result = pm.extract()    # result是一个dict

print "==title=="
print result['title']    # 获取页面标题

print "==content=="
for x in result['content']:
    if x['type'] == 'text':     # 正文每个段落内容，（连在一起就是正文内容）
        print x['data']

    if x['type'] == 'image':
        print "[IMAGE]", x['data']['src']     # 正文中的图片url

end_time = time.time()
print 'spend_time：', end_time - start_time