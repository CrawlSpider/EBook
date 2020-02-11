# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose, Join
###############################################################################
# NMOD.NET
# 优质电子书免费下载
# https://www.nmod.net/
###############################################################################


class NmodSpider(CrawlSpider):
    name = 'nmod'
    allowed_domains = ['nmod.net']
    start_urls = ['https://www.nmod.net/']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div/a[contains(@class, "cardbuy")]'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//li[contains(@class, "next-page")]/a'), follow=True),
    )

    
    def parse_item(self, response):
        """
        @url https://www.nmod.net
        @returns items 1
        @returns requests 0 0
        @scrapes title author format label date isbn content size download comment_cnt heart_cnt share_cnt
        """
        item = {}
        item['title'] = response.xpath('//div[contains(@class, "alert")]/p/img/@title').extract()
        item['author'] = response.xpath('//div[contains(@class, "alert")]/p/text()').re(u'(?<=作者：).+')
        item['format'] = response.xpath('//div[contains(@class, "alert")]/p/text()').re(u'(?<=格式：).+')
        item['label'] = response.xpath('//div[@class="article-tags"]/a/text()').extract()
        item['date'] = response.xpath('//div[contains(@class, "alert")]/p/text()').re('\d\d\d\d-\d\d-\d\d')
        isbn = response.xpath('//div[contains(@class, "alert")]/p/text()').re(u'(?<=ISBN[:：]).*[0-9]+')
        item['isbn'] = MapCompose(str.strip)(isbn)
        item['content'] = response.xpath('//article[contains(@class, "article-content")]/p/text()').extract()
        size = response.xpath('//table//td/text()').re(u'(?<=大小：)[.0-9MmKkBb]+')
        fun_k2m = lambda x : str('%.2f'%(float(re.sub('[KB]', '', x)) / 1024))
        item['number'] = [x if 'M' in x else x if 'K' not in x else fun_k2m(x)+'MB' for x in size]
        item['download'] = response.xpath('//table//td[@colspan]/a/text()').extract()
        item['comment_cnt'] = response.xpath('//*[contains(@class, "comments")]/../a/text()').re('[0-9]+')
        #number = response.xpath('//*[contains(@class, "comments")]/../a/text()').re('[0-9]+')
        #item['comment_cnt'] = MapCompose(int)(number)
        item['heart_cnt'] = response.xpath('//*[contains(@class, "heart")]/../span[@class="count"]/text()').extract()
        #number = response.xpath('//*[contains(@class, "heart")]/../span[@class="count"]/text()').extract()
        #item['heart_cnt'] = MapCompose(int)(number)
        item['share_cnt'] = response.xpath('//*[contains(@class, "share")]/../span[@class="bds_count"]/text()').extract()
        #number = response.xpath('//*[contains(@class, "share")]/../span[@class="bds_count"]/text()').extract()
        #item['share_cnt'] = MapCompose(int)(number)
        yield item
