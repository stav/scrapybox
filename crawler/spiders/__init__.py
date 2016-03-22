import scrapy


class ParseSpider(scrapy.Spider):
    name = 'parse'
    start_urls = ('http://www.example.com/',)

    def parse(self, response):
        raise NotImplementedError
