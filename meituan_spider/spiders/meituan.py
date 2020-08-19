import scrapy

class MeituanSpider(scrapy.Spider):
    name = "meituan"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super().from_crawler(crawler, *args, **kwargs)

    def start_requests(self):
        urls = [
            "https://tech.meituan.com/",
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_list)

    def make_requests_from_url(self, url):
        return super().make_requests_from_url(url)

    def parse_list(self, response:scrapy.http.response.Response):
        art_links_selector = response.xpath('//*[@id="J_main-container"]//h2[@class="post-title"]/a')
        for art_link_selector in art_links_selector:
            link = art_link_selector.xpath('@href')
            title = art_link_selector.xpath('text()')

        # 首页的第二页按钮
        second_page = response.xpath('//*[@id="J_main-container"]'
                                     '//a[contains(@class, "home-browser-more-btn")]/@href').get()
        if second_page:
            yield response.follow(second_page, callback=self.parse_list)

        #
        next_page = response.xpath('//*[@id="J_main-container"]//ul[@class="pagination"]'
                       '/li[not(contains(@class, "disabled"))]/a[@aria-label="Next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)