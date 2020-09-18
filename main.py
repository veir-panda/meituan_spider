import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from meituan_spider.spiders.meituan_article import MeituanArticleSpider
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
import threading
import logging
from multiprocessing import Process
import os
import time
import multiprocessing

configure_logging()


def crawl(cls, *args, **kwargs):
    crawler = CrawlerRunner(get_project_settings())
    crawler.crawl(cls, *args, **kwargs)

    d = crawler.join()
    print(MeituanArticleSpider.runing)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    urls = [
        # "https://tech.meituan.com/2020/08/13/openstack-to-kubernetes-in-meituan.html"
        "https://tech.meituan.com/2013/12/04/yui3-practice.html"
    ]

    # process = CrawlerProcess(get_project_settings())
    # process.crawl(MeituanArticleSpider, urls=urls)
    # process.start()

    # print(MeituanArticleSpider.runing)
    #
    # crawl(MeituanArticleSpider, urls=urls)
    # print("第二次")
    # crawl(MeituanArticleSpider, urls=urls)

    # task = threading.Thread(target=crawl, name="CrawlerThread",
    #                         args=(MeituanArticleSpider, ),
    #                         kwargs={
    #                             "urls": urls
    #                         })
    # task.start()
    # print(MeituanArticleSpider.runing)
    # task.join()

    print('Parent process %s.' % os.getpid())
    print("结果1：", MeituanArticleSpider.runing)
    p = Process(target=crawl, args=(MeituanArticleSpider,),
                kwargs={"urls": urls})
    print('Child process will start.')
    p.start()
    p2 = Process(target=crawl, args=(MeituanArticleSpider,),
                kwargs={"urls": urls})
    print('Child process will start.')
    p2.start()
    print("结果2：", MeituanArticleSpider.runing)
    time.sleep(1)
    print("结果2.2：", MeituanArticleSpider.runing)
    time.sleep(2)
    print("结果2.3：", MeituanArticleSpider.runing)
    p.join()
    p2.join()
    print("结果3：", MeituanArticleSpider.runing)
    print('Child process end.')

    multiprocessing.Semaphore()
