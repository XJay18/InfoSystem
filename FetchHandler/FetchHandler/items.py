# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfoItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
    issuedDate = scrapy.Field()
    holdingDate = scrapy.Field()
    place = scrapy.Field()
    uni = scrapy.Field()
    url = scrapy.Field()
