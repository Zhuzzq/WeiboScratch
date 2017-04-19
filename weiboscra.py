#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, codecs, random, time
from matplotlib import pyplot as plt

# get the response of the follwings
cookiefile = open('cookie.txt')
cookie = cookiefile.read().strip()
userfile = open('user.txt')
userid = userfile.readlines()[1].strip()
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Connection': 'keep-alive',
    'Cookie': cookie,  # to remove the cookie use '' instead
    'Host': 'm.weibo.cn',
    'Referer': 'http://m.weibo.cn/p/second?containerid=100505%s_-_FOLLOWERS' % userid,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                  'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                  'Version/9.0 Mobile/13B143 Safari/601.1',
    'X-Requested-With': 'XMLHttpRequest'
}

URL = 'http://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS' % userid
h = requests.get(url=URL, headers=headers)
if h.text:
    print('First Connection Succeeded')
else:
    print('First Connection Failed')

# print(h.text)

# get first page of followings and some info
text = json.loads(h.text)
# print(type(text))
# print(text)
pagecnt = text['maxPage']
fllwingcnt = text['count']
# print(pagecnt)
# print(fllwingcnt)

allusers = text['cards']
# print(allusers)

# get all followings
for page in range(2, int(pagecnt) + 1):
    time.sleep(random.random())
    URL = 'http://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=%d' % (userid, page)
    h = requests.get(url=URL, headers=headers)
    text = json.loads(h.text)
    allusers = allusers + text['cards']
# print(allusers)

# get each following info and store
Genderstatistic = {'m': 0,
                   'f': 0
                   }
verified = {True: 0,
            False: 0
            }
w = []
x = []
y = []
z = []
resfile = codecs.open('scratch_data.txt', 'w', 'utf-8')
resfile.write('Followings Info of UserID=%s\nFollowing Count: %s\nPage Count: %s\n\n' % (userid, fllwingcnt, pagecnt))
print('writing...')
for eachuser in allusers:
    userinfo = eachuser['user']
    print(userinfo)
    Genderstatistic[userinfo['gender']] += 1
    verified[userinfo['verified']] += 1
    w.append(int(userinfo['follow_count']))
    x.append(int(userinfo['statuses_count']))
    y.append(int(userinfo['followers_count']))
    z.append(userinfo['verified'])
    resfile.write('Screen Name: %s\nGender: %s  Posts: %d  Followings: %d  Followers: %d\n'
                  % (userinfo['screen_name'], userinfo['gender'], userinfo['statuses_count'],
                     userinfo['follow_count'], userinfo['followers_count']))
    if userinfo['description']:
        resfile.write('Description: %s\n\n\n' % userinfo['description'])
    else:
        resfile.write('Description: NONE\n\n\n')
resfile.close()

print(Genderstatistic)

# gender pie figure
plt.rcParams['figure.figsize'] = (16, 9)
piefig1 = plt.subplot(2, 2, 1)
mfper = [Genderstatistic['m'] * 100 / fllwingcnt, Genderstatistic['f'] * 100 / fllwingcnt]
piecolor = ['lightblue', 'pink']
patches, l_text, p_text = piefig1.pie(mfper, labels=Genderstatistic.keys(), colors=piecolor, explode=(0.06, 0),
                                      labeldistance=1.1, autopct='%3.2f%%', shadow=False, startangle=90,
                                      pctdistance=0.6)
piefig1.axis('equal')
piefig1.legend()
piefig1.set_title('GenderStatistic of UserID=%s\'s Followings\n\n%d in Total' % (userid, fllwingcnt))

# verification pie figure
piefig2 = plt.subplot(2, 2, 2)
vper = [verified[True] * 100 / fllwingcnt, verified[False] * 100 / fllwingcnt]
piecolor = ['orange', 'cyan']
patches, l_text, p_text = piefig2.pie(vper, labels=['verified', 'not verified'], colors=piecolor, explode=(0.06, 0),
                                      labeldistance=1.1, autopct='%3.2f%%', shadow=False, startangle=90,
                                      pctdistance=0.6)
piefig2.axis('equal')
piefig2.legend()
piefig2.set_title('V or NOT Statistic of UserID=%s\'s Followings\n\n%d in Total' % (userid, fllwingcnt))

# follower_cnt ~ post_cnt Curve
fig3 = plt.subplot(2, 2, 3)
for i in range(0, len(x)):
    fig3.plot(x[i], y[i], '+', color='orange' if z[i] else 'cyan')
fig3.set_xlabel('post count')
fig3.set_ylabel('follower count')
fig3.set_title('follower_cnt ~ post_cnt Curve')

# follower ~ follow Curve
fig4 = plt.subplot(2, 2, 4)
for i in range(0, len(y)):
    fig4.plot(w[i], y[i], '+', color='orange' if z[i] else 'cyan')
fig4.set_xlabel('follow count')
fig4.set_ylabel('follower count')
fig4.set_title('follower ~ follow Curve')

plt.savefig('statistic.png', dpi=300)
plt.show()
