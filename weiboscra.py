#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, os, requests, json

# get the response of the follwings
cookiefile = open('..\SinaWeiboDataDigging\cookie.txt')
cookie = cookiefile.read().strip()
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'Host': 'm.weibo.cn',
    # 'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://m.weibo.cn/p/second?containerid=1005055413496550_-_FOLLOWERS',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                  'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                  'Version/9.0 Mobile/13B143 Safari/601.1',
    'X-Requested-With': 'XMLHttpRequest'
}
cookiedict = {"Cookie": cookie}
following_url = 'http://m.weibo.cn' \
                '/p/second?containerid=1005055413496550_-_FOLLOWERS'
URL = 'http://m.weibo.cn/api/container/getSecond?containerid=1005055413496550_-_FOLLOWERS'
s = requests.session()
h = s.get(url=URL, headers=headers)
print(h.text)

hfile = open('get_url.html', 'w')
hfile.write(h.text)

text = json.loads(h.text)
print(type(text))
print(text)
pagecnt = text['maxPage']
fllwingcnt = text['count']
print(pagecnt)
print(fllwingcnt)
