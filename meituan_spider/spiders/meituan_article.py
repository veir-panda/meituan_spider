import scrapy
from gne import GeneralNewsExtractor
from meituan_spider.items import MeituanArticleSpiderItem

class MeituanArticleSpider(scrapy.Spider):
    name = "meituan_article"

    def __init__(self, name=None, urls=None, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = GeneralNewsExtractor()
        self.urls = urls if urls is not None else ["https://tech.meituan.com/2013/12/04/yui3-practice.html"]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response:scrapy.http.response.Response):
        next_page = response.xpath('//div[@class="navigation-wrapper"]/div/a[@class="next"]').get()
        if next_page:
            # yield response.follow(next_page, callback=self.parse)
            print(next_page)

        res = self.extractor.extract(response.text)
        return MeituanArticleSpiderItem(url=response.url,
                                        title=res['title'],
                                        content=res['content'],
                                        author=res['author'],
                                        publish_time=res['publish_time'])



