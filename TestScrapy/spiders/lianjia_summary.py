# encoding:utf-8

import os
import pandas as pd
import scrapy
import json
import re
import urlparse
from bs4 import BeautifulSoup
from .. import items
from datetime import *

basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
def listToString(str_list):
    return "".join(str_list)


class LianjiaSpider(scrapy.Spider):
    name = "Lianjia_summary"
    #allowed_domains = ["bj.lianjia.com"]
    start_urls = [
        "http://tj.lianjia.com/ershoufang/",

    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 40
    }

    date_str=date.today().strftime("%Y-%m-%d")
    save_file_path = basedir + '/data/' +start_urls[0].replace('/','_') + name  + '.json'

    def parse(self, response):
        base_url = urlparse.urlsplit(response.url)
        item = items.AreaItem()
        house_number = response.xpath(
            "/html/body/div[4]/div[1]/div[2]/h2/span/text()").extract()
        print house_number
        item['house_number'] = int(house_number[0])
        item['house_mean_price'] = 0
        item['area'] = response.url
        item['date'] = date.today().strftime("%Y-%m-%d")
        yield item

        # select by 区域
        area_url = response.xpath(
            "//div[@data-role ='ershoufang']/div/a/@href").extract()
        # area_url = response.xpath(
        #    "//div[@data-role ='ditiefang']/div/a/@href").extract()
        # area_url = response.xpath(
        #    "//div[@data-role ='xuequ']/div/a/@href").extract()


        for url in area_url:
            next_url = base_url._replace(path=url).geturl()
            #print next_url
            yield scrapy.Request(next_url,
                                 callback=self.parse_area,
                                 dont_filter=True)



    def parse_area(self, response):
        base_url = urlparse.urlsplit(response.url)
        area = base_url.path.split('/')[-2]
        item = items.AreaItem()
        house_number = response.xpath(
            "/html/body/div[4]/div[1]/div[2]/h2/span/text()").extract()
        print house_number
        item['house_number'] = int(house_number[0])
        item['house_mean_price'] = 0
        item['area'] = area
        item['date'] = date.today().strftime("%Y-%m-%d")
        yield item

        return
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
        area = base_url.path.split('/')[-2]
        item = items.AreaItem()
        house_number = response.xpath(
            "/html/body/div[4]/div[1]/div[2]/h2/span/text()").extract()
        print house_number
        item['house_number'] = int(house_number[0])
        item['house_mean_price'] = 0
        item['area'] = area
        item['date'] = date.today().strftime("%Y-%m-%d")
        #print area_url
