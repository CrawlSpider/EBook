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
    # 上传日期
    date = scrapy.Field()
    # ISBN
    isbn = scrapy.Field()
    # 内容简介
    content = scrapy.Field()
    # 书籍大小
    size = scrapy.Field()
    # 下载提供服务商（如：百度网盘等）
    download = scrapy.Field()
    # 书评统计
    comment_cnt = scrapy.Field()
    # 点赞统计
    heart_cnt = scrapy.Field()
    # 分享统计
    share_cnt = scrapy.Field()

    #pass
