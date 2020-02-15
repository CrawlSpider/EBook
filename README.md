# EBook
![](https://img.shields.io/badge/python3-Yes-brightgreen.svg) ![](https://img.shields.io/badge/python2-No-blue.svg)

- scrapy 框架爬虫的第一个练习代码
- 爬取电子书
- 获取图书下载的 "百度网盘提取码" 需要提交验证码，该码会不定期自动更换，请验证码在文件 nmode.py 的如下位置   
	```python
	 def start_requests(self):
        return [
            FormRequest(
                'https://www.nmod.net/book/14407.html',
                formdata={'huoduan_verifycode': '369521'},  
				# 此处校验码会不定期改变，如果发现失效则需更新
				# 请访问网址并在任何书籍介绍页面查看更新方式（关注小程序并发送指定消息获取）
                callback=self.parse_ecode
            )]
	```   
- python2 需要修改 nmode.py 的如下位置，一共有 **4** 处   
	```python 
	MapCompose(str.strip)(xxxxx) 
	改为 
	MapCompose(unicode.strip)(xxxxx)
	```


#### 运行
- 一般启动   
	`scrapy crawl nmod`
- 限制启动（仅爬取一个 item，测试用）    
	`scrapy crawl nmod -s CLOSESPIDER_ITEMCOUNT=1`
- 将爬取的内容存入 CSV 文件以便用 excel 查看    
	`scrapy crawl nmod -o nmod.csv -s FEED_EXPORT_ENCODING="gb18030"`

#### 事件
- 2020-02-14 添加 [NMOD.NET](https://www.nmod.net/) 的爬虫
- 2020-02-16 添加 [子午书简](https://5kindle.com/)  的爬虫