#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/21 17:17 
# @Author : Wancheng.b 
# @File : WeiShi.py 
# @Software: PyChar

'''
需要下载模拟器在电脑端（存在问题，可能是模拟器限制，一个用户只能爬取9个视频，之后就向上滑不动了），建议直接用手机
手机端需要安装ATX

'''


import os
import time
import requests
from selenium.webdriver.common.keys import Keys
import uiautomator2 as u2
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def find_element_xpath(driver, xpath):
    return WebDriverWait(driver, 20).until(lambda x: x.find_element_by_xpath(xpath))


def download_from_url(url, title, userName):
    if not os.path.exists('D:\\video\{}'.format(userName)):
        os.mkdir('D:\\video\{}'.format(userName))
    res = requests.get(url, stream=True)
    with open('D:\\video\{}\{}.mp4'.format(userName, title), 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                print('downloading')
                f.write(chunk)

def getVideo(snOrIp):
    # 设置不弹出浏览器
    # firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument('--headless')
    # firefox_options.add_argument('--disable-gpu')
    # driver = webdriver.Firefox(options=firefox_options)
    driver = webdriver.Firefox()
    d = u2.connect(snOrIp)
    d.app_start('com.tencent.weishi')
    a = 0
    while a < 2000:
        a = a + 1
        print(a)
        try:
            d(text="分享").click()
            time.sleep(1)
            d(text="复制链接").click()
            userName = d.xpath('//*[@resource-id="com.tencent.weishi:id/poster"]').get_text()

            # 先去百度把title得到
            driver = webdriver.Firefox()
            # driver = webdriver.Firefox(options=firefox_options)
            driver.get('https://www.baidu.com/')
            driver.implicitly_wait(60)
            find_element_xpath(driver, '//input[@name="wd"]').send_keys(Keys.CONTROL, 'v')
            find_element_xpath(driver, '//input[@class="bg s_btn"]').click()
            url = find_element_xpath(driver, '//input[@name="wd"]').get_attribute('value')
            title = url.split('>>')[0].strip()
            # 获取的文字有的会有乱码，读取的时候回读成?，新建文件不能有？、?，所以替换一下
            if title.find('?') != -1:
                title = title.replace('?', '！')
            if title.find('？') != -1:
                title = title.replace('？', '！')
            print(title)
            time.sleep(2)
            # 去https://weishi.iiilab.com下载
            driver.get('https://weishi.iiilab.com/')
            # input赋值操作
            find_element_xpath(driver, '//input[@class="form-control link-input"]').send_keys(url)
            time.sleep(2)
            # 点击解析
            find_element_xpath(driver, '//button[@class="btn btn-default"]').click()
            # 获取mp4地址
            url_mp4 = find_element_xpath(driver, '//a[@class="btn btn-success"]').get_attribute("href")
            # 下载
            download_from_url(url_mp4, title, userName)
        except Exception as e:
            raise e
            # print(repr(e))
            # print('load失败')
        finally:
            d(scrollable=True).scroll(steps=10)
            driver.quit()


if __name__ == '__main__':
    getVideo('127.0.0.1:62001')
