import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ('http://www.example.com/',)

    def parse(self, response):
        yield


class ExampleYieldSpider(ExampleSpider):
    name = 'example-yield'

    def parse(self, response):
        yield dict(
            request=dict(
                url=response.request.url,
                meta=response.request.meta,
                method=response.request.method,
                cookies=response.request.cookies,
                encoding=response.request.encoding,
                headers={
                    k.decode('utf-8'): [v.decode('utf-8') for v in l]
                    for k, l in response.request.headers.items()
                },
            ),
            response=dict(
                url=response.url,
                meta=response.meta,
                flags=response.flags,
                status=response.status,
                headers={
                    k.decode('utf-8'): [v.decode('utf-8') for v in l]
                    for k, l in response.headers.items()
                },
                body=dict(
                    head=response.css('head').extract_first()[:1000],
                    title=response.xpath('/html/head/title/text()').extract_first(),
                ),
            )
        )
