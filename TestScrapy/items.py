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


class SchoolItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    shool_name = scrapy.Field()
    shool_alias_name = scrapy.Field()
    address = scrapy.Field()
    retive_high_school = scrapy.Field()
    price_start = scrapy.Field()
    avg_price = scrapy.Field()
    Community_num = scrapy.Field()
    house_num = scrapy.Field()
    print "SchoolItem------------"
    # print name
