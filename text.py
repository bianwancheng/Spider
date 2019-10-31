#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/21 16:15 
# @Author : Wancheng.b 
# @File : text.py e
# @Software: PyCharm
# str = '现在的年轻人都乱套了??！'
# print(str.replace('?', '！'))
# if str.find('?') != -1:
#     str = str.replace('?', '！')
#     print(str)


'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/24 17:30
# @Author : Wancheng.b
# @File : Bilibili.py
# @Software: PyCharm

import os
import requests
from lxml import etree


# 搜索关键字下载爬取
def getBySearch():

    global input
    input = input('请输入要查询的关键字：')


    # https://search.bilibili.com/all?keyword=火影&page=1
    bilili_url = 'https://search.bilibili.com/all?keyword={}&page=1'.format(input)
    res = requests.get(bilili_url)
    print(res.status_code)
    html = res.text
    selector = etree.HTML(html)
    # 获取总页数
    pageNum = int(selector.xpath('//li[@class="page-item last"]/button/text()')[0].strip())
    print('总页数：', pageNum)

    # 存放目录
    if not os.path.exists('d:/video/{}'.format(input)):
        os.mkdir('d:/video/{}'.format(input))

    # 下载
    for i in range(1, pageNum+1):
        bilili_url = 'https://search.bilibili.com/all?keyword={}&page={}'.format(input, i)
        res = requests.get(bilili_url)
        print(res.status_code)
        html = res.text
        selector = etree.HTML(html)
        a_list = selector.xpath('//li[@class="video-item matrix"]/a/@href')
        print(a_list)
        for a in a_list:
            # 根据you-get下载
            os.system('you-get -o d:/video/{} {}'.format(input, a))


# 首页热门爬取

def getShouYe():
    pass


if __name__ == '__main__':
    getBySearch()

'''
# import os
#
# os.system('you-get -o d:/video www.bilibili.com/video/av13454305?from=search')
# # www.bilibili.com/video/av68245533?from=search
# os.system('you-get -o d:/video www.bilibili.com/video/av68245533?from=search')
# import time
#
# print(time.time())
# time.sleep(1)
# print(time.time())

title_list = ['asdf', '影视杂谈', '影视剪辑', '短片', '预告·资讯']
input_title = '影视杂谈'
if input_title in title_list[1:]:
    print(input_title)
    print('asdf')