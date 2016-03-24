import asyncio
import aiohttp

from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings as settings
from crawler.spiders import ParseSpider


def example(request):
    """
    $ curl "http://127.0.0.1:8080/api/example"
    Example route response
    """
    text = 'Example route response\n'
    return aiohttp.web.Response(body=text.encode('utf-8'))


async def parse_eval(request):
    """
    $ curl "http://127.0.0.1:8080/api/parse/eval/response.status"
    200

    $ curl "http://127.0.0.1:8080/api/parse/eval/response.headers"
    {b'Last-Modified': [b'Fri, 09 Aug 2013 23:54:35 GMT'], b'Etag': [b'"359670651+gzip"'], b'X-Cache': [b'HIT'], b'Date': [b'Mon, 21 Mar 2016 20:17:19 GMT'], b'X-Ec-Custom-Error': [b'1'], b'Cache-Control': [b'max-age=604800'], b'Vary': [b'Accept-Encoding'], b'Content-Type': [b'text/html'], b'Server': [b'ECS (ftw/FBE4)'], b'Expires': [b'Mon, 28 Mar 2016 20:17:19 GMT']}

    $ curl "http://127.0.0.1:8080/api/parse/eval/response"
    <200 http://www.example.com/>

    $ curl "http://127.0.0.1:8080/api/parse/eval/self"
    <S 'parse' at 0x7f3a3af2fb38>

    $ curl "http://127.0.0.1:8080/api/parse/eval/self.__dict__"
    {'settings': <scrapy.settings.Settings object at 0x7f3a3af47e10>, 'result': {...}, 'crawler': <scrapy.crawler.Crawler object at 0x7f3a3af47b70>}
    """
    class S(ParseSpider):
        result = None
        def parse(self, response):
            self.result = eval(self.code())
            yield

        @staticmethod
        def code():
            return request.match_info.get('code')

    async def poll(crawler):
        while crawler.crawling:
            await asyncio.sleep(1)
        return crawler.spider.result

    crawler = Crawler(S, settings())
    crawler.crawl()
    result = await poll(crawler)
    text = '{}\n'.format(result)

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
    class S(ParseSpider):
        def parse(self, response):
            yield

    async def poll(crawler):
        while crawler.crawling:
            await asyncio.sleep(float(request.match_info.get('time')))

    crawler = Crawler(S, settings())
    crawler.crawl()
    await poll(crawler)
    text = '{}\n'.format(request.path)

    return aiohttp.web.Response(body=text.encode('utf-8'))
