# EBook

- scrapy 框架爬虫的第一个联系代码
- 尝试爬取 NMOD 图书目录

#### 运行
- 一般启动   
	`scrapy crawl nmod`
- 限制启动（仅爬取第一页的部分，测试用）    
	`scrapy crawl nmod -s CLOSESPIDER_ITEMCOUNT=1`
- 将爬取的内容存入 CSV 文件以便用 excel 查看    
	`scrapy crawl nmod -o nmod.csv -s FEED_EXPORT_ENCODING="gb18030"`
