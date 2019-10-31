#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/14 11:17 
# @Author : Wancheng.b 
# @File : video.py 
# @Software: PyCharm

import requests
import re
from selenium import webdriver


class Spider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "referer": "https://www.gaoxiaovod.com/zt/dongwu",
            "Host": "100.100.100.100:8081",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }


    # 详情页提取client_id, vid，并拼接成src,返回src
    def getVidAndClientId(self, link):
        res = requests.get(link)
        res.encoding = 'utf-8'
        content = res.text
        with open('D:\\bianwancheng\Desktop\SC.txt', 'w+')as f:
            f.write(content)

        client_id, vid ,video= '', '', ''
        with open('D:\\bianwancheng\Desktop\SC.txt', 'r+') as f:
            content = f.readlines() # 是一个list
            for i in range(len(content)):
                # 查找client_id所在行确认位置，正则表达式提取client_id
                if content[i].find('client_id:') != -1:
                    client_id = re.findall(r"\w{16}", content[i])[0]
                    print(client_id)
                elif content[i].find('vid:') != -1:
                    vid = re.findall(r"\w{15}", content[i], re.I)[0]
                    print(vid)
                elif content[i].find('video/mp4') != -1:
                    print(i)
                    video = re.findall(r"http.*\w", content[i], re.I)[0].split(',')[0]
                    print(video)

                else:
                    # 除去优酷秒拍ck之外的
                    pass
        if client_id and vid is not None:
            src = "https://player.youku.com/embed/{}==?client_id={}&password=&autoplay=true".format(vid, client_id)
            print(src)
            return src
        elif video is not None:
            src = ''
            driver = webdriver.Chrome()
            try:
                driver.get(video)
                src = driver.find_element_by_xpath('//video[@name="media"]/source').get_attribute('src')
                print(src)
            except Exception as e:
                print(e)
                # raise e
            finally:
                driver.quit()
            return src


    def download_from_url(self, url, filepath):
        res = requests.get(url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    print('downloading')
                    f.write(chunk)

    def getRes(self):
        res = requests.get('https://h5.weishi.qq.com/weishi/feed/76lVtaQWT1IjQ1M7k/wsfeed?wxplay=1&id=76lVtaQWT1IjQ1M7k&spid=1570891350782640&qua=v1_and_weishi_4.0.0_88_push33_e&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011')
        print(res.text)

    def getSele(self):
        driver = webdriver.Chrome()
        driver.get('https://h5.weishi.qq.com/weishi/feed/76lVtaQWT1IjQ1M7k/wsfeed?wxplay=1&amp;id=76lVtaQWT1IjQ1M7k&amp;spid=1570891350782640&amp;qua=v1_and_weishi_4.0.0_88_push33_e&amp;chid=100081014&amp;pkg=3670&amp;attach=cp_reserves3_1000370011')
        iframe = driver.find_element_by_tag_name('iframe')
        print(iframe)
        driver.switch_to.frame(iframe)
        print(driver.page_source)

if __name__ == '__main__':
    # you ck

    # https://www.gaoxiaovod.com/v/v16004.html
    # http://vali.cp31.ott.cibntv.net/6573020445F4271B0D55660BE/03000A01005C25826D1D2DA2F1A2E33FBA5B90-C1B4-40CB-A549-CEFA529CDE8B.mp4?ccode=0512&duration=290&expire=18000&psid=d99981ed1f2174ff948a351f4081f2b2&ups_client_netip=6fcfc2c5&ups_ts=1571049197&ups_userid=&utid=k0XJFQZU5ioCAW%2FPwsW00M14&vid=XMzk4NTI4NDc0NA&vkey=A573d2653f6c63de8ba04472e9e436628&s=efbfbd52efbfbdd6ba11&sp=160&bc=2
    # miao
    # https://www.gaoxiaovod.com/v/v27730.html
    # http://dy-frontend.video.ums.uc.cn/video/wemedia/8030c63bbbc6433a8f49db07b57db98e/5e49558778a78eb7be03a7d154d4c5ff-2131770986-2-0-3.mp4?auth_key=1571044835-2494d61eadc8449ba66c009949146dd1-0-ba39cea5a50fa25b01b96fd93e5310be
    # src = Spider().getVidAndClientId('https://www.gaoxiaovod.com/v/v16004.html')

    Spider().download_from_url('http://v3-dy.ixigua.com/f1e0eae3260074e387075d48fbc41328/5db6a396/video/m/2208a5de9f87ad94667b3a476015f4eed721163f099000003e62f20a5594/?a=1128&br=1195&cr=0&cs=0&dr=0&ds=6&er=&l=2019102815133901000803115561249E&lr=&qs=0&rc=anlpcGh0eG9vcDMzZGkzM0ApNTRnNjdpOjs4NzY2MzM5OmdoLjUtXzZzNW5fLS0yLS9zczQzLWFiNjIyNTQ2YTQ0Nl86Yw%3D%3D', 'D:\\bianwancheng\Desktop\\123.mp4')
    # Spider().getSele()

    # https://g.alicdn.com/alilog/aplus_cplugin/0.1.2/ls.html?_a_ig_p_url=https%3A%2F%2Fplayer.youku.com%2Fembed%2FXMTMzOTY5NTY2OA%3D%3D%3Fclient_id%3Df67e97ee21e17da2%26password%3D%26autoplay%3Dtrue