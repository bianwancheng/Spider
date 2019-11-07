#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/28 14:02 
# @Author : Wancheng.b 
# @File : DouYin.py 
# @Software: PyCharm


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

def getVideo(snOrIp, userName):
    # 设置不弹出浏览器
    # firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument('--headless')
    # firefox_options.add_argument('--disable-gpu')
    # driver = webdriver.Firefox(options=firefox_options)
    d = u2.connect(snOrIp)
    d.app_start('com.ss.android.ugc.aweme')

    a = 1
    while a < 200:
        driver = webdriver.Firefox()
        print('下载第', a, '个视频')
        try:
            if d(text="查看详情").exists(timeout=5) or d(text="立即下载").exists(timeout=5):
                print('淘宝购物跳过')
                continue
            a = a + 1
            # userName = d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/jt"]/android.widget.LinearLayout[1]/text()')
            # print(userName)

            time.sleep(1)
            title = d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/a7l"]').get_text()
            d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/d6b"]').click()
            time.sleep(1)

            # 获取的文字有的会有乱码，读取的时候回读成?，新建文件不能有？、?，所以替换一下
            if title.find('?') != -1:
                title = title.replace('?', '！')
            if title.find('？') != -1:
                title = title.replace('？', '！')
            print('userName', userName, 'title:', title)

            d(text="复制链接").click()
            # 去http://3g.gljlw.com/diy/douyin.php获取下载地址
            driver.get('http://3g.gljlw.com/diy/douyin.php')
            # input赋值操作
            find_element_xpath(driver, '//div[@class="content"]/input[@type="text"]').send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            # 点击获取
            find_element_xpath(driver, '//input[@type="submit"]').click()
            # 获取mp4地址
            url_mp4 = find_element_xpath(driver, '//textarea[@class="KL_bbs_textarea"]').text
            # 下载
            download_from_url(url_mp4, title, userName)
        except Exception as e:
            # raise e
            print(repr(e))
            print('load失败')
        finally:
            d.swipe(0.641, 0.863, 0.348, 0.232, 0.1)
            # d(scrollable=True).scroll(steps=10)
            driver.quit()


if __name__ == '__main__':
    # 设备ip或者sn号，用户名
    getVideo('127.0.0.1:62001', '祝晓晗')
