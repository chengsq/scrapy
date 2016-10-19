# encoding:utf-8

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pandas as pd
import scrapy
import json
import re
import urlparse
import requests
from PIL import Image
import time
from scrapy.http import Request, FormRequest
from .. import items
from datetime import *

def DEBUG_PRINT(s):
    print s

basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class LianjiaSipder(scrapy.Spider):
    name = "Lianjia_chengjiao"
    allowed_domains = ["www.lianjia.com"]

    AUTO_MODE = 1 # 是否递归自动爬取子区域
    area_url = "http://bj.lianjia.com/chengjiao/"
    #area_url = 'http://bj.lianjia.com/chengjiao/nanshatan1/'
    date_str=date.today().strftime("%Y-%m-%d")
    save_file_path = basedir + '/data/' +area_url.replace('/','_') + name + date_str + '.json'
    start_urls = [
        "http://bj.lianjia.com"
    ]

    custom_settings = {
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 100
        }


    auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'
    headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            "Accept": "image/webp,image/*,*/*;q=0.8",
            "DNT": "1",
            "Referer": "http://bj.lianjia.com/",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8"
        }

    formdata={
              'username': '18667179303',
              'password': 'sdly2013',
              '_eventId': 'submit',
              'verifyCode': '',
              'redirect': ''
          }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [Request('http://www.lianjia.com/', meta={'cookiejar': 1}, callback=self.post_login)]

    # FormRequeset出问题了
    def post_login(self, response):
        DEBUG_PRINT('Preparing login')

        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        #'''
        return FormRequest.from_response(response,
                                          meta={'cookiejar': response.meta[
                                              'cookiejar']},
                                          headers=self.headers,  # 注意此处的headers
                                          formdata = self.formdata,
                                          callback=self.after_login,
                                          dont_filter=True
                                          )

    def after_login(self, response):
        if self.AUTO_MODE :
            yield scrapy.Request(self.area_url,
                             callback=self.parse_area,
                             dont_filter=True)
        else:
            item = items.AreaItem()
            item['city']= ''
            item['area'] = self.area_url.split('/')[-2]
            item['subarea'] = self.area_url.split('/')[-2]
            yield scrapy.Request(self.area_url,
                             meta={'areaItem': item},
                             callback=self.parse_house_page,
                             dont_filter=True)




    def parse_area(self, response):
        # select by 区域
        area_url = response.xpath(
            "//div[@data-role ='ershoufang']/div/a/@href").extract()
        # area_url = response.xpath(
        #    "//div[@data-role ='ditiefang']/div/a/@href").extract()
        # area_url = response.xpath(
        #    "//div[@data-role ='xuequ']/div/a/@href").extract()
        for url in area_url:
            item = items.AreaItem()
            base_url = urlparse.urlsplit(response.url)
            item['city']= base_url.netloc.split('.')[0]
            item['area'] = url.split('/')[-2]
            next_url = base_url._replace(path=url).geturl()
            print next_url
            yield scrapy.Request(next_url,meta={'areaItem': item},
                                 callback=self.parse_subarea,
                                 dont_filter=True)


    def parse_subarea(self, response):
        base_url = urlparse.urlsplit(response.url)
        area_url = response.xpath(
            "/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a/@href").extract()
        print area_url
        item = response.meta['areaItem']
        for url in area_url:
            next_url = base_url._replace(path=url).geturl()
            item['subarea'] = url.split('/')[-2]
            print "parse_subarea",next_url
            yield scrapy.Request(next_url,
                           meta={'areaItem': item},
                           callback=self.parse_house_page,
                            dont_filter=True)

    def parse_house_page(self, response):

        house_number = response.xpath(
            "/html/body/div[4]/div[1]/div[2]/div[1]/span/text()").extract()

        if int(house_number[0]) < 1:
            return

        page_info = response.xpath(
            '/html/body/div[4]/div[1]/div[3]/div[2]/div/@page-data')
        page_js = json.loads(page_info.extract()[0])
        total_page = page_js['totalPage']
        next_url_base = response.url + 'pg'
        print "total_page", total_page
        for p in range(1, total_page):
            next_url = next_url_base + str(p)
            print next_url,total_page
            yield scrapy.Request(next_url,
                                 meta={'areaItem': response.meta['areaItem']},
                                 callback=self.parse_house_detail,
                                 dont_filter=True)

    def parse_house_detail(self, response):
        print response.meta['areaItem']
        item = items.ChengjiaoHouseItem()
        title = response.xpath("//div[@class = 'title']/a/text()").extract()
        unitPrice = response.xpath("//div[@class='unitPrice']/span/text()").extract()
        totalPrice = response.xpath("//div[@class='totalPrice']/span/text()").extract()
        position = response.xpath("//span[@class='dealHouseTxt']/span/text()").extract()
        cj_date = response.xpath("//div[@class='dealDate']/text()").extract()
        description = response.xpath("//div[@class='houseInfo']/text()").extract()
        href = response.xpath("//div[@class='title']/a/@href").extract()
        t = response.meta['areaItem']
        area = t['area']
        subarea = t['subarea']

        #print title
        #print unitPrice
        print totalPrice
        #print position
        #print cj_date
        #print description
        #print href
        print area
        print subarea

        for i in range(len(title)):
            item['title'] = title[i]
            item['total_price'] = float(totalPrice[i])
            item['unit_price'] = float(unitPrice[i])
            item['chengjiao_date'] = cj_date[i]
            item['description'] = description[i]
            item['href'] = href[i]
            item['area'] = area
            item['subarea'] = subarea
            yield item




        #for url in self.start_urls:
        #    yield self.make_requests_from_url(url)
