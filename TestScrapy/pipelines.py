# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import csv_writer
from datetime import *

class TestscrapyPipeline(object):

    def __init__(self):
        d =date.today()
        str=d.strftime("%Y-%m-%d")
        self.is_opened = False;



    def process_item(self, item, spider):
        print "process_item  TestscrapyPipeline"
        file_path = spider.save_file_path
        if not self.is_opened:
            self.file = open(file_path, 'a+')
            self.is_opened = True

        #print spider.start_urls
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode('utf-8'))
        return item
