# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from pymongo import MongoClient

mongo = MongoClient(
    host=os.environ.get('CRAWLAB_MONGO_HOST') or 'localhost',
    port=int(os.environ.get('CRAWLAB_MONGO_PORT') or 27017),
    username=os.environ.get('CRAWLAB_MONGO_USERNAME'),
    password=os.environ.get('CRAWLAB_MONGO_PASSWORD'),
    authSource=os.environ.get('CRAWLAB_MONGO_AUTHSOURCE') or 'admin'
)
db = mongo[os.environ.get('CRAWLAB_MONGO_DB') or 'test']
col = db[os.environ.get('CRAWLAB_COLLECTION') or 'test']
task_id = os.environ.get('CRAWLAB_TASK_ID')

class EbookPipeline(object):
    def process_item(self, item, spider):
        item['task_id'] = task_id
        if col is not None:
            col.save(item)
        return item
