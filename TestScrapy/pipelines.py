# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import csv_writer

basedir = os.path.dirname(os.path.dirname(__file__))


class TestscrapyPipeline(object):

    def __init__(self):
        self.file = open(basedir + '/info.json', 'w')
        self.csv_writer = csv_writer.CSVWriter(
            ['address', 'total_price', 'unit_price', 'title'])

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode('utf-8'))
        return item
