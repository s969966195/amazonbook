# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    author=scrapy.Field()
    press=scrapy.Field() #出版社
    ISBN=scrapy.Field()
    ASIN=scrapy.Field()
    introduction=scrapy.Field() #简介
    promotion=scrapy.Field() #促销
    prime_paperback=scrapy.Field()
    prime_ebook=scrapy.Field()
