
import pandas as pd
import scrapy
from TestScrapy.items import SchoolItem

shool_list = []
def listToString(str_list):
    return "".join(str_list)

class LianjiaSpider(scrapy.Spider):
    name = "Lianjia"
    allowed_domains = ["tj.lianjia.com"]
    start_urls = [
        "http://tj.lianjia.com/xuequfang/"
    ]

    def parse(self, response):
        #base_link = response.xpath('//base/@href').extract()
        links = response.xpath("/html/body/div[5]/div[2]/div/div/div[1]/ul/li")
        filename = response.url.split("/")[-2]
        #print base_link
        for link in links[0:-1]:
            #print link.extract()
            shool_info = SchoolItem()
            shool_info['url'] = link.xpath("a/@href").extract()
            shool_info['img_url'] = link.xpath("a/img/@src").extract()
            str_list = link.xpath("div[@class='host-count']/h2/a/text()").extract()
            shool_info['shool_name'] = listToString(str_list)
            str_list = link.xpath("div[@class='host-count']/div[1]/div[1]/p[1]/text()").extract()
            shool_info['shool_alias_name'] = listToString(str_list)[3:-1]
            str_list = link.xpath("div[@class='host-count']/div[1]/div[1]/p[2]/text()").extract()
            shool_info['address'] = listToString(str_list)[3:-1]
            str_list = link.xpath("div[@class='host-count']/div[2]/text()").extract()
            shool_info['retive_high_school'] = listToString(str_list)[5:-1]
            str_list = link.xpath("div//div[@class='price fl']/span/span/text()").extract()
            #print float(listToString(str_list)),int(listToString(str_list))
            shool_info["price_start"] = float(listToString(str_list))
            str_list = link.xpath("div//div[@class='price fl']/p[1]/text()").extract()
            shool_info["avg_price"] = listToString(str_list)
            #print listToString(str_list)
            str_list = link.xpath("div//div[@class='fr num']/p[1]/a/span/text()").extract()
            shool_info["Community_num"] = int(listToString(str_list))
            str_list = link.xpath("div//div[@class='fr num']/p[2]/a/span/text()").extract()
            shool_info["house_num"] =  int(listToString(str_list)[0:-1])

            #shool_list.append(shool_info)
            yield  shool_info
            #print  shool_info["house_num"]

        print len(shool_list)
        shool_df = pd.DataFrame(shool_list)

        #shool_df.to_csv(filename + '.csv')
