import types
import asyncio
import logging
import aiohttp.web
import scrapy.signals
import scrapy.crawler

from scrapy.utils.project import get_project_settings

import scrapybox.crawler.spiders

SETTINGS = get_project_settings()

logger = logging.getLogger(__name__)


async def poll(crawler, time=1):
    while crawler.crawling:
        await asyncio.sleep(time)


async def parse_post(request):
    """
    $ curl localhost:8080/api/eval -d start_urls=[\"http://scrapinghub.com\",\"http://scrapy.org\"]
    Scraped 2 items: [{'response': <200 http://scrapinghub.com>}, {'response': <200 http://scrapy.org>}]

    <Request POST /api/eval > <MultiDictProxy('start_url': 'scrapy.org', 'parse': 'text = response.xpath(\'id("scrapy-logo")/following-sibling::p\')\r\nitem = dict(text=text.extract())\r\n', 'yield_item': 'on')>
    2016-03-25 12:08:12 [aiohttp.access] INFO: 127.0.0.1 - - [25/Mar/2016:19:08:12 +0000] "POST /api/eval HTTP/1.1" 200 188 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36"
    Scraped 1 items: [{'text': ['<p>An open source and collaborative framework for extracting the data you need from websites.\n      </p>', '<p>In a fast, simple, yet extensible way.</p>']}]

    http://stackoverflow.com/questions/35256152/can-eval-be-applied-on-a-compiled-ast-node-have-a-local-context
        self.emit ('\n{}\n', node.args [1] .s.format (* [
            eval (
                compile (
                    ast.Expression (arg),
                    '<string>',
                    'eval'
                ),
                {},
                {'include': include}
            )
            for arg in node.args [2:]
        ]))
    """
    await request.post()

    server_info = dict(
        request=dict(
            host=str(request.host),
            path=str(request.path),
            POST=dict(request.POST),
            query=str(request.query_string),
            method=str(request.method),
            scheme=str(request.scheme),
            cookies=dict(request.cookies),
            version=str(request.version),
            headers=dict(request.headers),
            content=list(request.content.read()),
            payload=list(request.payload.read()),
            has_body=bool(request.has_body),
        ),
    )

    class Spider(scrapybox.crawler.spiders.ExampleYieldSpider):
        pass

    if 'start_urls' in request.POST:
        value = request.POST['start_urls'].strip()
        if value:
            Spider.start_urls = eval(value)

    if 'start_url' in request.POST:
        value = request.POST['start_url'].strip()
        if value:
            url = scrapy.utils.url.add_http_if_no_scheme(value)
            Spider.start_urls = [url]

    if request.POST.get('parse'):
        def parse(self, response):
            exec(request.POST['parse'], globals(), locals())
            if request.POST.get('yield_item'):
                frame_item = locals()['item']
                yield frame_item
        Spider.parse = types.MethodType(parse, Spider)

    settings = dict(SETTINGS)

    settings['ROBOTSTXT_OBEY'] = 'settings.ROBOTSTXT_OBEY' in request.POST
    settings['HTTPCACHE_ENABLED'] = 'settings.HTTPCACHE_ENABLED' in request.POST
    if 'settings.USER_AGENT' in request.POST:
        settings['USER_AGENT'] = request.POST['settings.USER_AGENT']

    items = []

    def item_scraped(item, response, spider):
        items.append(item)

    crawler = scrapy.crawler.Crawler(Spider, settings)
    crawler.signals.connect(item_scraped, signal=scrapy.signals.item_scraped)
    logger.debug('API starting to crawl {}'.format(crawler))
    crawler.crawl()
    await poll(crawler)
    data = dict(items=items, scrapybox=server_info)

    return aiohttp.web.json_response(data)


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
    class Spider(scrapybox.crawler.spiders.ExampleSpider):
        result = None
        def parse(self, response):
            self.result = eval(self.code())
            yield

        @staticmethod
        def code():
            return request.match_info.get('code')

    crawler = scrapy.crawler.Crawler(Spider, SETTINGS)
    logger.debug('API starting to crawl {}'.format(crawler))
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
    Spider = scrapybox.crawler.spiders.ExampleSpider
    crawler = scrapy.crawler.Crawler(Spider, SETTINGS)
    logger.debug('API starting to crawl {}'.format(crawler))
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
