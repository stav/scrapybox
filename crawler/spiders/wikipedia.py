import scrapy


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['wikipedia.com']
    start_urls = ('http://www.wikipedia.com/',)

    def parse(self, response):
        yield {'url': response.url, 'body': response.body[:100]}
