# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from os import path
import sys
import datetime

sys.path.append(path.dirname(path.dirname(path.dirname(__file__))))
from DatabaseHandler.initiation import InfoDB




class FetchhandlerPipeline(object):
    def process_item(self, item, spider):
        issued_fmt_time = str(item.get('issued_time', '')).replace('-', '')
        if issued_fmt_time \
                < datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=90), '%Y%m%d'):
            return item
        lecturers = ''
        for person in item['lecturer']:
            lecturers += person
        self.infodb.insert_Lecture(
            item.get('title', ''),
            lecturers,
            item.get('issued_time', ''),
            item.get('lecture_time', ''),
            item.get('location', ''),
            item.get('uni', ''),
            item.get('url', ''),
            item.get('description', '')
        )
        return item

    def open_spider(self, spider):
        self.infodb = InfoDB()
        self.infodb.openDB()

    def close_spider(self, spider):
        self.infodb.closeDB()
