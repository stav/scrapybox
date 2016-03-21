import aiohttp

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings as settings
from crawler.spiders.example import ExampleSpider


def example(request):
    print(request)

    runner = CrawlerRunner(settings())
    runner.crawl(ExampleSpider)

    text = 'Example crawler started\n'

    return aiohttp.web.Response(body=text.encode('utf-8'))
