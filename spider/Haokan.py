#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/15 12:57 
# @Author : Wancheng.b 
# @File : Haokan.py 
# @Software: PyCharm
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def find_element_xpath(driver, xpath):
    return WebDriverWait(driver, 20).until(lambda x: x.find_element_by_xpath(xpath))

def find_elements_xpath(driver, xpath):
    return WebDriverWait(driver, 20).until(lambda x: x.find_elements_by_xpath(xpath))

def download(url, title):
    res = requests.get(url, stream=True)
    with open("D:\\bianwancheng\Desktop\{}.mp4".format(title), 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                print('downloading')
                f.write(chunk)

driver = webdriver.Chrome()
# driver.maximize_window()
url = 'https://haokan.baidu.com/tab/gaoxiao'
driver.get(url)
liList = []
js = "var q=document.documentElement.scrollTop=100000"
# 达到条件满足才停止向下滑动
while len(liList) <= 2000:
    liList = find_elements_xpath(driver, '//div[@class="infinite"]//ul/li/a')
    driver.execute_script(js)
liList_href = []

# 获取所有的href
for li in liList:
    liList_href.append(li.get_attribute('href'))

print(liList_href)
# 详情页进行下载
for href in liList_href:
    try:
        driver = webdriver.Chrome()
        driver.get(href)
        title = find_element_xpath(driver, '//h2[@class="videoinfo-title"]').text
        src = find_element_xpath(driver, '//video[@mediatype="video"]').get_attribute('src')
        print(title)
        print(src)
        download(src, title)
    except:
        print('下载失败')
    finally:
        driver.quit()
