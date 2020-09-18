import scrapy
from gne import GeneralNewsExtractor
from meituan_spider.items import MeituanArticleSpiderItem
import logging

class MeituanArticleSpider(scrapy.Spider):
    runing = False
    name = "meituan_article"

    def __init__(self, name=None, urls=None, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = GeneralNewsExtractor()
        # self.urls = urls if urls is not None else ["https://tech.meituan.com/2013/12/04/yui3-practice.html"]
        if urls is None:
            raise ValueError("url 不能为空")
        self.urls = urls
        self.count = 1
        MeituanArticleSpider.runing = True

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response:scrapy.http.response.Response):
        next_page = response.xpath('//div[@class="navigation-wrapper"]/div/a[@class="next"]/@href').get()
        if next_page:
            print(next_page)
            self.count += 1
            if self.count < 20:
                yield response.follow(next_page, callback=self.parse)

        desc = response.xpath('//meta[@name="description"]/@content').get()
        tags = response.xpath('//span[@class="tag-links"]/a/text()').getall()
        res = self.extractor.extract(response.text)
        yield MeituanArticleSpiderItem(url=response.url,
                                        title=res['title'],
                                        content=res['content'],
                                        tags=tags,
                                        author=res['author'],
                                        publish_time=res['publish_time'])

    @staticmethod
    def close(spider, reason):
        MeituanArticleSpider.runing = False
        return super().close(spider, reason)



