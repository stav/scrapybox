import aiohttp

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from crawler.spiders.wikipedia import WikipediaSpider


def route(request):
    print(request)
    route = request.match_info.get('route')
    text = 'Route: {}\n'.format(route)

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(WikipediaSpider)

    return aiohttp.web.Response(body=text.encode('utf-8'))
