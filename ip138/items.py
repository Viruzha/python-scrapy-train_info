# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ip138Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    locat=scrapy.Field()
    route=scrapy.Field()
    type_tr=scrapy.Field()
    dist=scrapy.Field()
    cost=scrapy.Field()
