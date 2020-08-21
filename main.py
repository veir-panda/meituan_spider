import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from meituan_spider.spiders.meituan_article import MeituanArticleSpider
import logging

if __name__ == '__main__':
    # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    urls = [
        # "https://tech.meituan.com/2020/08/13/openstack-to-kubernetes-in-meituan.html"
        "https://tech.meituan.com/2013/12/04/yui3-practice.html"
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl(MeituanArticleSpider, urls=urls)
    process.start()



