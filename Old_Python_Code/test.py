# coding=utf-8

import hashlib
import time
import urllib2
from bs4 import BeautifulSoup

# 请替换appkey和secret
appkey = "5934525"
secret = "d2f4c808b4f9a1800b7290b8907e9f76"

paramMap = {
    "app_key": appkey,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  # 如果你的程序在国外，请进行时区处理
}
# 排序
keys = paramMap.keys()
keys.sort()

codes = "%s%s%s" % (secret, str().join('%s%s' % (key, paramMap[key]) for key in keys), secret)

# 计算签名
sign = hashlib.md5(codes).hexdigest().upper()

paramMap["sign"] = sign

# 拼装请求头Proxy-Authorization的值
keys = paramMap.keys()
authHeader = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)

print
authHeader

# 接下来使用蚂蚁动态代理进行访问

proxy_handler = urllib2.ProxyHandler({"http": '123.57.138.199:8123'})
opener = urllib2.build_opener(proxy_handler)

request = urllib2.Request('http://shanghai.anjuke.com/school/')

##将authHeader放入请求头中即可, 注意authHeader必须在每次请求时都重新计算，要不然会因为时间误差而认证失败
request.add_header('Proxy-Authorization', authHeader)

html = urllib2.urlopen(request, timeout=10)
#print(html)

bsObj = BeautifulSoup(html, "lxml")
print(bsObj)

#def getBSobj(url):
#    try:
#        #req = urllib2.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
#        req = urllib2.Request(url)
#        html = urllib2.urlopen(req, timeout=10)
#    except urllib2.HTTPError as e:
#        return None
#    try:
#        bsObj = BeautifulSoup(html, "html.parser")
#    except AttributeError as e:
#        return None
#    return bsObj