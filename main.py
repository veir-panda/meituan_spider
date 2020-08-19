import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from meituan_spider.spiders.meituan_article import MeituanArticleSpider

if __name__ == '__main__':
    urls = [
        "https://tech.meituan.com/2020/08/13/openstack-to-kubernetes-in-meituan.html"
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl(MeituanArticleSpider, urls=urls)
    process.start()



