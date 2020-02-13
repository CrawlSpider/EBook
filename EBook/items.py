# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ################ 自定义 ################
    
    # 书名
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 电子书格式
    format = scrapy.Field()
    # 分类标签
    label = scrapy.Field()
    # ISBN
    isbn = scrapy.Field()
    # 书籍大小
    sizeMB = scrapy.Field()
    # 书籍介绍页面
    book_page = scrapy.Field()
    # 百度网盘下载链接
    down_url = scrapy.Field()
    # 百度网盘下载提取码
    ecode = scrapy.Field()

    #pass
