# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import logging

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MeituanArticleSaveSpiderPipeline(object):
    def __init__(self):
        print("inited")

    def open_spider(self, spider):
        print("start crawled")

    def close_spider(self, spider):
        print("closed")

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
        # print(item)
        return item


class MeituanArticleESSaverPipeline(object):
    def __init__(self, es_host, es_auth):
        self.es = Elasticsearch(hosts=es_host,
                                http_auth=es_auth,
                                # 节点无法响应后刷新节点
                                sniff_on_connection_fail=True)
        self.index = "meituan-tech"
        logging.info("ElasticSearch index: %s", self.index)
        if not self.es.indices.exists(self.index):
            logging.info("ElasticSearch index not exist, will auto created.")
            idx_body = {
                "mappings": {
                    "properties": {
                        "url": {
                            "type": "text",
                        },
                        "title": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "desc": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "content": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "tags": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "author": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "publish_time": {
                            "type": "date",
                        },
                    }
                }
            }
            self.es.indices.create(self.index, body=idx_body)

    def open_spider(self, spider):
        logging.info("spider started.")

    def close_spider(self, spider):
        self.es.close()
        logging.info("spider closed.")

    def process_item(self, item, spider):
        # res = self.es.index(self.index, dict(item))
        return item

    @classmethod
    def from_crawler(cls, crawler):
        """
        从管道中访问爬虫实例，例如爬虫的配置信息
        :param crawler:
        :return:
        """
        return cls(
            es_host=crawler.settings.get('ELASTICSEARCH_HOSTS'),
            es_auth=crawler.settings.get('ELASTICSEARCH_AUTH')
        )
