# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    print "------------", name
    pass


class HouseItem(scrapy.Item):
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    address = scrapy.Field()
    title = scrapy.Field()
    position = scrapy.Field()

    print "HouseItem------------"


class ChengjiaoHouseItem(scrapy.Item):
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    title = scrapy.Field()
    area = scrapy.Field()
    subarea = scrapy.Field()
    chengjiao_date = scrapy.Field()
    size = scrapy.Field()
    href = scrapy.Field()
    description = scrapy.Field()

class AreaItem(scrapy.Item):
    house_number = scrapy.Field()
    house_mean_price = scrapy.Field()
    area = scrapy.Field()
    subarea = scrapy.Field()
    date = scrapy.Field()
    city = scrapy.Field()
    print "AreaItem------------"




class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()  # 保存抓取问题的url
    title = scrapy.Field()  # 抓取问题的标题
    description = scrapy.Field()  # 抓取问题的描述
    answer = scrapy.Field()  # 抓取问题的答案
    name = scrapy.Field()  # 个人用户的名称
