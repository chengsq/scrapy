import pandas as pd
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector



def listToString(str_list):
    return "".join(str_list)

class LianjiaSpider(scrapy.Spider):
    name = "Lianjia"
    allowed_domains = ["tj.lianjia.com"]
    download_delay = 2

    start_urls = [
        "http://tj.lianjia.com/xuequfang/",
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=('/u012150179/article/details'),
                              restrict_xpaths=('//li[@class="next_article"]')),
             callback='parse_item',
             follow=True)
    ]


    def parse(self, response):
        pass
