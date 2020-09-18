from elasticsearch import Elasticsearch

class ESModel():
    def __init__(self, hosts, http_auth):
        self.es = Elasticsearch(hosts=hosts,
                                http_auth=http_auth,
                                # 节点无法响应后刷新节点
                                sniff_on_connection_fail=True)

    def __call__(self, *args, **kwargs):
        return self.es

    def close(self):
        return self.es.close()

if __name__ == '__main__':
    hosts = [
        '',
    ]
    http_auth = ('', '')
    es = ESModel(hosts=hosts, http_auth=http_auth)

    es().search(index="meituan-tech")

    es.close()