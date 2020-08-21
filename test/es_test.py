from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import unittest


class ESTest(unittest.TestCase):
    def setUp(self) -> None:
        hosts = [
            '139.224.237.185:9020',
        ]
        http_auth = ('elastic', 'xiongwei')
        self.es = Elasticsearch(hosts=hosts,
                                http_auth=http_auth,
                                # 节点无法响应后刷新节点
                                sniff_on_connection_fail=True)
        self.index = "meituan-tech"
        if not self.es.indices.exists(self.index):
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

    def tearDown(self) -> None:
        self.es.close()

    def testExist(self):
        result = self.es.indices.exists(self.index)
        print(result)

    def testGet(self):
        print(self.es.get(self.index, '1'))

    def testCreate(self):
        body = {
            "url": "http://111.",
            "title": "Java工程师",
            "desc": "数据库管理"
        }
        print(self.es.index(self.index, body, id='1'))

    def testSearch(self):
        res = self.es.search(index=self.index)
        print(res)


if __name__ == '__main__':
    pass
