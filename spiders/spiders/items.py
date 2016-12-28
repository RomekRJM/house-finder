# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertyItem(scrapy.Item):
    title = scrapy.Field()
    date_added = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    num_rooms = scrapy.Field()
    floor = scrapy.Field()
    price_per_sqm = scrapy.Field()
    sublist = scrapy.Field()
    extras_list = scrapy.Field()
    location = scrapy.Field()
