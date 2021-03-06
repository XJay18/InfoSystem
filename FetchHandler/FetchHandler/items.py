# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfoItem(scrapy.Item):
    title = scrapy.Field()
    lecturer = scrapy.Field()  # list object
    lecture_time = scrapy.Field()
    location = scrapy.Field()
    uni = scrapy.Field()
    url = scrapy.Field()
    issued_time = scrapy.Field()
    description = scrapy.Field()
