import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ('http://www.example.com/',)

    def parse(self, response):
        yield {'url': response.url, 'body': response.body[:100]}
