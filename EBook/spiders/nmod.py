# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose, Join
from scrapy.http import FormRequest
###############################################################################
# NMOD.NET
# 优质电子书免费下载
# https://www.nmod.net/
###############################################################################


class NmodSpider(CrawlSpider):
    name = 'nmod'
    allowed_domains = ['nmod.net']
    start_urls = ['https://www.nmod.net/']

    def start_requests(self):
        return [
            FormRequest(
                'https://www.nmod.net/book/14407.html',
                formdata={'huoduan_verifycode': '369521'},  # 此处校验码会不定期改变，如果发现失效则需更新
                                                            # 请访问网址并在任何书籍介绍页面查看更新方式（关注小程序并发送指定消息获取）
                callback=self.parse_ecode
            )]

    def parse_ecode(self, response):
        print('获取\"提取码\"提交成功')
        for url in self.start_urls:
            yield scrapy.Request(url=url)

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
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
        #item['title'] = response.xpath(u'//div[contains(@class, "alert")]/p/img/@title').extract()
        title = response.xpath(u'//table[contains(@class, "dltable")]//td/text()').re(u'(?<=文件名称：).+')
        if len(title) == 0:
            item['title'] = response.xpath(u'//h1[contains(@class, "title")]/a/text()').extract()
        else:
            item['title'] = title
        author = response.xpath(u'//article[contains(@class, "article-content")]//p/text()').re(u'(?<=作者[:：]).+')
        item['author'] = MapCompose(str.strip)(author)   # str 对象是 python3 的语法，python2 请更换为 unicode
        format = response.xpath(u'//article[contains(@class, "article-content")]//p/text()').re(u'(?<=格式[:：]).+')
        item['format'] = MapCompose(str.strip)(format)   # str 对象是 python3 的语法，python2 请更换为 unicode
        label = response.xpath(u'//div[@class="article-tags"]/a/text()').extract()
        if len(label) == 0:
            item['label'] = response.xpath(u'//article[contains(@class, "article-content")]//p/text()').re(u'(?<=标签[:：]).+')
        else:
            item['label'] = label
        isbn = response.xpath(u'//div[contains(@class, "alert")]/p/text()').re(u'(?<=ISBN[:：]).*[0-9]+')
        item['isbn'] = MapCompose(str.strip)(isbn)   # str 对象是 python3 的语法，python2 请更换为 unicode
        size = response.xpath(u'//table//td/text()').re(u'(?<=大小：)[.0-9MmKkGgBb]+')
        fun_k2m = lambda x : str(u'%.2f'%(float(re.sub(u'[KB]', u'', x)) / 1024))
        fun_g2m = lambda x : str(u'%.2f'%(float(re.sub(u'[GB]', u'', x)) * 1024))
        size_mb = [x if u'M' in x else x if u'K' not in x else fun_k2m(x)+u'MB' for x in size]
        size_mb = [x if u'M' in x else x if u'G' not in x else fun_g2m(x)+u'MB' for x in size_mb]
        item['sizeMB'] = [re.sub('[kKMmGgBb]+', '', i) for i in size_mb]
        item['ecode'] = response.xpath(u'//span/strong/text()').re(u'[a-zA-Z0-9]+')
        item['book_page'] = response.url
        item['down_url'] = response.xpath(u'//table[@class="dltable"]//a/@href').re(u'(?<=url=).+')

        yield item
        
