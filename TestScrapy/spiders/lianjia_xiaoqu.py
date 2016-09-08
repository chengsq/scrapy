import pandas as pd
import scrapy
import json
import re
from .. import items

def listToString(str_list):
    return "".join(str_list)

class LianjiaSpider(scrapy.Spider):
    name = "Lianjiaxiaoqu"
    allowed_domains = ["tj.lianjia.com"]
    start_urls = [
        "http://tj.lianjia.com/ershoufang/heping/",
        "http://tj.lianjia.com/ershoufang/nankai/",
        "http://tj.lianjia.com/ershoufang/hexi/",
        "http://tj.lianjia.com/ershoufang/hebei/",
        "http://tj.lianjia.com/ershoufang/dongli/",
        'http://tj.lianjia.com/ershoufang/xiqing/',
        'http://tj.lianjia.com/ershoufang/tanggu/',
        'http://tj.lianjia.com/ershoufang/jinnan/'
    ]

    def parse(self, response):
        page_info = response.xpath('/html/body/div[4]/div[1]/div[5]/div[2]/div/@page-data')
        page_js = json.loads(page_info.extract()[0])
        total_page = page_js['totalPage']
        next_url_base = response.url+'pg'
        print "total_page",total_page
        for p in range(1,total_page):
            next_url = next_url_base + str(p)
            #print next_url,total_page
            yield scrapy.Request(next_url,
            callback=self.parse_house,
            dont_filter=True)

    def parse_house(self, response):
        item = items.HouseItem()

        t = response.xpath('/html/body/div[4]/div[1]/ul')
        title = t.xpath("//div[@class='title']/a/text()").extract()
        unitPrice = t.xpath("//div[@class='unitPrice']/@data-price").extract()
        totalPrice = t.xpath("//div[@class='totalPrice']/span/text()").extract()
        address = t.xpath("//a[@data-el='region']/text()").extract()

        for i in range(len(title)):
            item['title'] = title[i]
            item['total_price'] = totalPrice[i]
            item['unit_price'] = unitPrice[i]
            item['address'] = address[i]
            #print item.keys()
            yield item
