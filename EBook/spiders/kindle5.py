# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.http import FormRequest
import logging
###############################################################################
# 5kindle
# 《子午书简》免费电子书分享交流下载
# https://5kindle.com/
###############################################################################


class Kindle5Spider(CrawlSpider):
    name = 'kindle5'
    allowed_domains = ['5kindle.com']
    start_urls = ['http://5kindle.com/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div/a[contains(@class, "buy")]'), callback='parse_e_secret', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//li[contains(@class, "next-page")]/a'), follow=True),
    )

    def parse_e_secret(self, response):
        self.logger.info('已经打开书籍页面 \"' + response.url + '\"，判断是否需要提取码')
        is_e_secret_code = response.xpath(u'//input[@type = "password" and @name = "e_secret_key"]')
        if is_e_secret_code:
            self.logger.info('页面 \"' + response.url + '\" 存在提取码，准备发送申请请求')
            return [
                FormRequest(
                    url = response.url,
                    formdata = {'e_secret_key': '68682019'},    # 此处校验码会不定期改变，如果发现失效则需更新
                                                                # 请访问网址并在任何书籍介绍页面查看更新方式（关注小程序并发送指定消息获取）
                    callback = self.parse_item,
                )]
        else:
            self.logger.info('页面 \"' +  response.url + '\" 不存在提取码，放弃...')
    
    def parse_item(self, response):
        """
        @url https://5kindle.com
        @returns items 1
        @returns requests 0 0
        @scrapes title author label book_page ecode down_url
        """
        item = {}

        #
        # 校验一下获取 "提取码" 是否成功
        is_e_secret_code = response.xpath(u'//input[@type = "password" and @name = "e_secret_key"]')
        if is_e_secret_code:
            self.logger.info('页面 \"' +  response.url + '\" 存在故障，无法成功获取 \"提取码\"，放弃本页')
            return item
        else:
            self.logger.info('获取 \"提取码\" 成功, 开始提取页面 \"' + response.url + '\" 中的信息...')
        #print(response.body.decode('utf-8'))
        #
        # 提取书名
        item['title'] =  response.xpath(u'//h1[contains(@class, "article-title")]/a/text()').get().strip()
        #
        # 提取书籍作者
        author = response.xpath(u'//span[@class = "muted"]/i[contains(@class, "fa-user")]/following-sibling::a/text()').get()
        if author:
            item['author'] = author.strip()
        #
        # 提取书籍分类标签
        item['label'] = response.xpath(u'//meta[@name = "keywords"]/@content').get()
        #
        # 本书介绍页面
        item['book_page'] = response.url
        #
        #
        # 
        ecode = response.xpath(u'//div[@class = "e-secret"]/p[contains(text(), "密码")]/text()').get()
        if ecode:
            # 原始内容为格式如："网盘密码：百度网盘密码：6c0r\xa0\xa0\xa0\xa0\xa0天翼云盘密码：8251"
            # 将所有 \xa0（也就是 &nbsp;）整体替换为单个空格
            # 期望结果为 "网盘密码：百度网盘密码：6c0r 天翼云盘密码：8251"
            ecode = re.sub(u'\s+', u' ', ecode)
            # 再进行分割
            # 期望结果为 "['网盘密码', '百度网盘密码', '6c0r', '天翼云盘密码', '8251']"
            ecode = re.split(u'：| ', ecode)
            # 最后删除第一个元素
            if '网盘密码' == ecode[0]:
                ecode.remove('网盘密码')
            else:
                del ecode[0]
            item['ecode'] = ecode
            item['down_url'] = response.xpath(u'//div[@class = "e-secret"]//a/@href').re(u'(?<=url=).+')
        else:
            # 这是不需要下载码的下载方式
            d_url = response.xpath(u'//div[@class = "e-secret"]//a/@href').re(u'(?<=url=).+')
            if 'sobooks' in str(d_url):
                # 某种下载方式，测试基本都已失效
                d_url.append(u'地址可能失效')
            if 'olecn' in str(d_url):
                # 论坛下载
                d_url.append(u'地址可能失效')
            #
            item['down_url'] = d_url
            item['ecode'] = u'不需要'

        yield item
