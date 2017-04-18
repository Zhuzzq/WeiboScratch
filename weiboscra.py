#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, codecs

# get the response of the follwings
cookiefile = open('cookie.txt')
cookie = cookiefile.read().strip()
userfile = open('user.txt')
userid = userfile.readlines()[2].strip()
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'Host': 'm.weibo.cn',
    # 'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://m.weibo.cn/p/second?containerid=100505%s_-_FOLLOWERS' % userid,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                  'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                  'Version/9.0 Mobile/13B143 Safari/601.1',
    'X-Requested-With': 'XMLHttpRequest'
}
cookiedict = {"Cookie": cookie}

URL = 'http://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS' % userid
h = requests.get(url=URL, headers=headers)
# print(h.text)

# get first page of followings and some info
text = json.loads(h.text)
# print(type(text))
# print(text)
pagecnt = text['maxPage']
fllwingcnt = text['count']
print(pagecnt)
print(fllwingcnt)

allusers = text['cards']
# print(allusers)

# get all followings
for page in range(2, int(pagecnt) + 1):
    URL = 'http://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=%d' % (userid, page)
    h = requests.get(url=URL, headers=headers)
    text = json.loads(h.text)
    allusers = allusers + text['cards']
# print(allusers)

# get each following info and store
Genderstatistic = {'m': 0,
                   'f': 0
                   }
resfile = codecs.open('scratch_data.txt', 'w', 'utf-8')
resfile.write('Followings Info of UserID=%s\nFollowing Count: %s\nPage Count: %s\n\n' % (userid, fllwingcnt, pagecnt))
for eachuser in allusers:
    userinfo = eachuser['user']
    # print(userinfo)
    resfile.write('Screen Name: %s\nGender: %s  Posts: %d  Followings: %d  Followers: %d\n'
                  % (userinfo['screen_name'], userinfo['gender'], userinfo['statuses_count'],
                     userinfo['follow_count'], userinfo['followers_count']))
    if userinfo['description']:
        resfile.write('Description: %s\n\n\n' % userinfo['description'])
    else:
        resfile.write('Description: NONE\n\n\n')
