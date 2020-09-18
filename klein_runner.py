import json

from klein import Klein, route, run
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
import datetime

from meituan_spider.spiders.meituan_article import MeituanArticleSpider

app = Klein()

scheduler = TwistedScheduler()
# crawl_job = None

class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        # dfd.addCallback(self.return_items)
        return dfd
        # return json.dumps({"code":200, "msg":"ok"})

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        return self.items


def return_spider_output(output):
    """
    :param output: items scraped by CrawlerRunner
    :return: json with list of items
    """
    # this just turns items into dictionaries
    # you may want to use Scrapy JSON serializer here
    return json.dumps([dict(item) for item in output], ensure_ascii=False)

with app.subroute("/api/v1") as app:
    @app.route("/crawl")
    def schedule(request):
        print(1)
        urls = [
            # "https://tech.meituan.com/2020/08/13/openstack-to-kubernetes-in-meituan.html"
            "https://tech.meituan.com/2013/12/04/yui3-practice.html"
        ]
        runner = MyCrawlerRunner(settings=get_project_settings())
        spider = MeituanArticleSpider
        deferred = runner.crawl(spider, urls=urls)


        # deferred.addCallback(return_spider_output)
        return deferred

    @app.route("/status")
    def status(request):
        print(2)
        return json.dumps(MeituanArticleSpider.runing)


def schedule_crawl_job():
    print("定时检测任务", MeituanArticleSpider.runing)
    if not MeituanArticleSpider.runing:
        print("重新启动任务")
        crawl(get_last_crawled_url())

def crawl(urls):
    runner = MyCrawlerRunner(settings=get_project_settings())
    spider = MeituanArticleSpider
    deferred = runner.crawl(spider, urls=urls)

def get_last_crawled_url():
    return ["https://tech.meituan.com/2013/12/04/yui3-practice.html"]


if __name__ == '__main__':
    # crawl(get_last_crawled_url())
    # print("开始调度")
    # scheduler.add_job(schedule_crawl_job, "interval",
    #                   seconds=10,
    #                   start_date=datetime.datetime.now())
    # scheduler.start()
    # app.run("localhost", 9000)

    settings = get_project_settings()

    print(settings)