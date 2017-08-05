# -*- coding: utf-8 -*-
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self):
        #链接数据库
        self.client=pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db=self.client[settings['MONGO_DB']]
        self.coll=self.db[settings['MONGO_COLL']]#collection

    def process_item(self,item,spider):
        postItem=dict(item) #把item转化成字典形式
        self.coll.insert(postItem) #向数据库插入一条记录
        return item
