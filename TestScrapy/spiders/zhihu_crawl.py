# encoding:utf-8


import pandas as pd
import scrapy
import json
import re
import urlparse
import requests
from PIL import Image
import time


#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy.http import Request, FormRequest
from .. import items

def DEBUG_PRINT(s):
    print s




def Get_captcha(headers):
    session = requests.session()
    print headers
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = raw_input("please input the captcha\n>")
    print captcha
    return captcha



class ZhihuSipder(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = [
        "http://www.zhihu.com"
    ]

    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Accept": "image/webp,image/*,*/*;q=0.8",
        "DNT": "1",
        "Referer": "http://www.zhihu.com/",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        captcha_str = Get_captcha(self.headers)
        return [Request("http://www.zhihu.com/#signin", meta={'cookiejar': 1}, callback=self.post_login)]

    # FormRequeset出问题了
    def post_login(self, response):
        DEBUG_PRINT('Preparing login')
        # 下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
        xsrf = Selector(response).xpath(
            '//input[@name="_xsrf"]/@value').extract()[0]
        DEBUG_PRINT(xsrf)
        captcha_str = Get_captcha()
        print captcha_str
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        #'''
        return [FormRequest.from_response(response,  # "http://www.zhihu.com/login",
                                          meta={'cookiejar': response.meta[
                                              'cookiejar']},
                                          headers=self.headers,  # 注意此处的headers
                                          formdata={
                                              '_xsrf': xsrf,
                                              'email': '21631712@qq.com',
                                              'password': 'sdly2013',
                                              'remember_me':'true',
                                              'captcha':captcha_str
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]
        #'''
    def after_login(self, response):
        print "after_login"
        pass
        #for url in self.start_urls:
        #    yield self.make_requests_from_url(url)

    def parse_page(self, response):
        problem = Selector(response)
        item = ZhihuItem()
        item['url'] = response.url
        item['name'] = problem.xpath('//span[@class="name"]/text()').extract()
        print item['name']
        item['title'] = problem.xpath(
            '//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        item['description'] = problem.xpath(
            '//div[@class="zm-editable-content"]/text()').extract()
        item['answer'] = problem.xpath(
            '//div[@class=" zm-editable-content clearfix"]/text()').extract()
        return item
