import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ('http://www.example.com/',)

    def parse(self, response):
        yield


class ExampleYieldSpider(ExampleSpider):

    def parse(self, response):
        yield dict(response=response)
