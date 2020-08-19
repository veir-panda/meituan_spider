# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MeituanArticleSaveSpiderPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        """
        从管道中访问爬虫实例，例如爬虫的配置信息
        :param crawler:
        :return:
        """
        # return cls(
        #     mongo_uri=crawler.settings.get('MONGO_URI'),
        #     mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        # )
        return cls()

    def process_item(self, item, spider):
        print(111)
        return item
