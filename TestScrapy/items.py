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
