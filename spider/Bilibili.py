#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/24 17:30 
# @Author : Wancheng.b 
# @File : Bilibili.py 
# @Software: PyCharm

'''
nav标签栏链接:
首页：https://www.bilibili.com
动漫：https://www.bilibili.com/v/douga
影视：https://www.bilibili.com/v/cinephile  影视剪辑和影视杂谈
'''

import os
import time

import requests
from lxml import etree
from selenium import webdriver


class BiliSearch:
    '''搜索关键字下载爬取'''

    def getBySearch(self):

        global input
        input = input('请输入要查询的关键字：')
        print('输入的是：', input)
        # https://search.bilibili.com/all?keyword=火影&page=1
        print(input)
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
        for i in range(1, pageNum + 1):
            bilili_url = 'https://search.bilibili.com/all?keyword={}&page={}'.format(input, i)
            res = requests.get(bilili_url)
            print(res.status_code)
            html = res.text
            selector = etree.HTML(html)
            a_list = selector.xpath('//li[@class="video-item matrix"]/a/@href')
            print(a_list)
            for a in a_list:
                # 根据you-get下载
                print('you-get -o d:/video/{} http:{}'.format(input, a))
                os.system('you-get -o d:/video/{} https:{}'.format(input, a))


'''
首页Nav栏爬取,考虑到爬取全站太费时间了，可以爬取某个Nav下的全部或者某个小分类
参数格式(nav, lev1, lev2, ...) ('影视', '影视杂谈', '影视剪辑', ...)
'''


class BiliNav:

    def __init__(self):
        self.shouye_url = 'https://www.bilibili.com'
        self.Headers = {
            'Origin': 'https://www.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.bilibili.com/v/cinephile/cinecism/?spm_id_from=333.6.b_7072696d6172795f6d656e75.88'
        }

    def getNav(self):
        global input
        input = '影视, 影视杂谈, 影视剪辑'
        # input = input("请输入爬取的Nav内容，如(影视, 影视杂谈, 影视剪辑, ...)：")
        print('输入的是：', input)
        input_list = input.split(', ')
        res = requests.get(self.shouye_url)
        print(res.status_code)
        print('输入的数据拆分成列表，input_list:', input_list)
        selector = etree.HTML(res.text)

        # 返回格式[['影视', '影视杂谈', '按热度排序的url'], ...]
        list = []
        for input_title in input_list[1:]:
            url = selector.xpath(
                '//ul[@class="nav-menu"]/li/a/div[contains(text(), "{}")]/parent::a/parent::li/ul//a/span[contains(text(), "{}")]/parent::a/@href'.format(
                    input_list[0], input_title))[0]

            # 获取到的url：www.bilibili.com/v/cinephile/cinecism/是默认排序的转换为按热度排序为：https://www.bilibili.com/v/cinephile/cinecism/#/all/click，多了/#/all/click
            url_title = []
            url_title.append(input_list[0])
            url_title.append(input_title)
            url_title.append('https:' + url + '#/all/click')
            list.append(url_title)
        print("返回格式形如[['影视', '影视杂谈', '按热度排序的url'], ...]", list)
        # https://www.bilibili.com/v/cinephile/cinecism/#/all/click
        return list

    def getVideo(self, url, inputType):

        # res = requests.get(url, headers=self.Headers)
        # print(res.status_code)
        # print(res.text)
        # selector = etree.HTML(res.text)
        # href_list = selector.xpath('//div[@id="videolist_box"]//ul/li//a/@href')
        # print(href_list)
        driver = webdriver.Chrome()
        driver.get(url)

        # 存放目录
        if not os.path.exists('D:/voide/{}'.format(inputType)):
            os.mkdir('d:/voide/{}'.format(inputType))
        pageNum = driver.find_element_by_xpath('//button[@class="pagination-btn"]').text
        for page in range(int(pageNum) + 1):
            time.sleep(2)
            a_list = driver.find_elements_by_xpath('//div[@id="videolist_box"]//ul/li//a')
            for href in a_list:
                # 根据you-get下载
                print(href.get_attribute('href'))
                os.system('you-get -o D:/voide/{} {}'.format(inputType, href.get_attribute('href')))
            driver.find_element_by_xpath('//button[@class="nav-btn iconfont icon-arrowdown3"]').click()


if __name__ == '__main__':
    # 通过搜索爬
    BiliSearch().getBySearch()

    # 通过nav爬取
    # title_url = BiliNav().getNav()
    # print(title_url)
    # for i in range(len(title_url)):
    #     BiliNav().getVideo(title_url[i][2], title_url[i][1])
