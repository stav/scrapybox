import asyncio
import aiohttp.web
import scrapy.signals
import scrapy.crawler

from scrapy.utils.project import get_project_settings

from scrapybox.crawler.spiders import ParseSpider

SETTINGS = get_project_settings()


async def poll(crawler, time=1):
    while crawler.crawling:
        await asyncio.sleep(time)


async def parse_post(request):
    """
    $ curl localhost:8080/api/eval -d start_urls=[\"http://scrapinghub.com\",\"http://scrapy.org\"]
    Crawled responses: [<200 http://scrapinghub.com/>, <200 http://scrapy.org>]
    """
    class Spider(ParseSpider):
        def parse(self, response):
            yield {}

    for prop in await request.post():
        setattr(Spider, prop, eval(request.POST[prop]))

    responses = []

    def item_scraped(item, response, spider):
        responses.append(response)

    crawler = scrapy.crawler.Crawler(Spider, SETTINGS)
    crawler.signals.connect(item_scraped, signal=scrapy.signals.item_scraped)
    crawler.crawl()
    await poll(crawler)
    text = 'Crawled responses: {}\n'.format(responses)

    return aiohttp.web.Response(body=text.encode('utf-8'))


async def parse_get(request):
    """
    $ curl "http://127.0.0.1:8080/api/parse/eval/response.status"
    200

    $ curl "http://127.0.0.1:8080/api/parse/eval/response.headers"
    {b'Last-Modified': [b'Fri, 09 Aug 2013 23:54:35 GMT'], b'Etag': [b'"359670651+gzip"'], b'X-Cache': [b'HIT'], b'Date': [b'Mon, 21 Mar 2016 20:17:19 GMT'], b'X-Ec-Custom-Error': [b'1'], b'Cache-Control': [b'max-age=604800'], b'Vary': [b'Accept-Encoding'], b'Content-Type': [b'text/html'], b'Server': [b'ECS (ftw/FBE4)'], b'Expires': [b'Mon, 28 Mar 2016 20:17:19 GMT']}

    $ curl "http://127.0.0.1:8080/api/parse/eval/response"
    <200 http://www.example.com/>

    $ curl "http://127.0.0.1:8080/api/parse/eval/self"
    <Spider 'parse' at 0x7f3a3af2fb38>

    $ curl "http://127.0.0.1:8080/api/parse/eval/self.__dict__"
    {'settings': <scrapy.settings.Settings object at 0x7f3a3af47e10>, 'result': {...}, 'crawler': <scrapy.crawler.Crawler object at 0x7f3a3af47b70>}
    """
    class Spider(ParseSpider):
        result = None
        def parse(self, response):
            self.result = eval(self.code())
            yield

        @staticmethod
        def code():
            return request.match_info.get('code')

    crawler = scrapy.crawler.Crawler(Spider, SETTINGS)
    crawler.crawl()
    await poll(crawler)
    text = '{}\n'.format(crawler.spider.result)

    return aiohttp.web.Response(body=text.encode('utf-8'))


async def delay(request):
    """
    $ curl localhost:8080/api/delay/15 &
    [1] 17172
    $ curl localhost:8080/api/delay/5 &
    [2] 17174
    $ curl localhost:8080/api/delay/1 &
    [3] 17177
    $ /api/delay/1
    /api/delay/5
    /api/delay/15
    """
    class Spider(ParseSpider):
        def parse(self, response):
            yield

    crawler = scrapy.crawler.Crawler(Spider, SETTINGS)
    crawler.crawl()
    await poll(crawler, float(request.match_info.get('time')))
    text = '{}\n'.format(request.path)

    return aiohttp.web.Response(body=text.encode('utf-8'))


def hello(request):
    """
    $ curl "http://127.0.0.1:8080/api/hello"
    Hello world!
    """
    text = 'Hello world!\n'
    return aiohttp.web.Response(body=text.encode('utf-8'))
