# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from jianshuusers.items import UserItem


class JianshuusersPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
            host = settings['MONGODB_HOST']
            port = settings['MONGODB_PORT']
            dbName = settings['MONGODB_DBNAME']
            client = pymongo.MongoClient(host=host, port=port)
            tdb = client[dbName]
            self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        user = dict(item)
        self.post.insert(user)
        return item