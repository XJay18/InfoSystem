# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from os import path
import sys

sys.path.append(path.dirname(path.dirname(path.dirname(__file__))))
from DatabaseHandler.initiation import InfoDB


class FetchhandlerPipeline(object):
    def process_item(self, item, spider):
        print('process_test')
        self.infodb.insert_Lecture(title=item['title'], url=item['url'], issuedDate=item['issued_time'],
                                   uni=item['uni'], holdingDate=item['lecture_time'], place=item['location'])
        return item

    def open_spider(self, spider):
        self.infodb = InfoDB()
        self.infodb.openDB()

    def close_spider(self, spider):
        self.infodb.closeDB()
