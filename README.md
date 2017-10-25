
> This project was put on hold after I realized that I did not have an easy way
> to get control of the logging output; I must be missing something easy.

> Crawling is currently still hardcoded to `example.com`.

# Scrapybox - a Scrapy GUI

A RESTful async Python web server that runs arbitrary code within Scrapy spiders
via an HTML webapge interface.

1. Server receives POST request
2. Server uses Scrapy to crawl site
3. Server sends back standard output

### Quick Serve

    pip install scrapybox
    pip install scrapy
    python -m scrapybox.server.server

#### GUI

Visit http://localhost:8080/ in web browser.

#### Client

    curl "http://localhost:8080/api/eval/response.status"
    200

## License

BSD licensed

## Installation

### Requirements

* Python 3.5.0+

See also: `requirements.txt`

### Install Scrapy

    $ pip install scrapy

### Install Scrapybox

    $ git clone git@github.com:stav/scrapybox.git
    $ cd scrapybox
    $ python setup.py install

    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/scrapybox-0.1-py3.6.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/aiohttp-2.3.1-py3.6-linux-x86_64.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/Jinja2-2.9.6-py3.6.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/yarl-0.13.0-py3.6-linux-x86_64.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/async_timeout-2.0.0-py3.6.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/multidict-3.3.0-py3.6.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/chardet-3.0.4-py3.6.egg
    Installed /home/stav/.virtualenvs/xme2/lib/python3.6/site-packages/MarkupSafe-1.0-py3.6-linux-x86_64.egg
    Finished processing dependencies for scrapybox==0.1

## Server

Run in the server in a terminal perhaps.

### Startup

    $ sbserve

    Reactor installed
    2017-10-25 12:14:22 [scrapybox.server.server] INFO: Scrapybox server starting
    2017-10-25 12:14:22 [scrapybox.server.server] INFO: Twisted reactor running
    2017-10-25 12:14:22 [scrapybox.server.server] INFO: Aiohttp server starting
    2017-10-25 12:14:22 [stdout] INFO: ======== Running on http://0.0.0.0:8080 ========
    2017-10-25 12:14:22 [stdout] INFO: (Press CTRL+C to quit)

### Shutdown

Send interrupt signal *(ctrl-c)*

    ^C
    2017-10-25 12:19:44 [scrapybox.server.server] INFO: Scrapybox server shutting down
    2017-10-25 12:19:44 [scrapybox.server.server] INFO: Scrapybox server shutdown complete

## Client Examples

### Hello world!

    $ curl "http://localhost:8080/api/hello"

    Hello world!

### Get response status

    $ curl -i "http://localhost:8080/api/eval/response.status"

    HTTP/1.1 200 OK
    Content-Length: 4
    Content-Type: application/octet-stream
    Date: Wed, 25 Oct 2017 16:29:45 GMT
    Server: Python/3.6 aiohttp/2.3.1

    200

### Get response headers

    $ curl "http://localhost:8080/api/eval/response.headers"

    {b'Accept-Ranges': [b'bytes'], b'Cache-Control': [b'max-age=604800'], b'Content-Type': [b'text/html'], b'Date': [b'Wed, 25 Oct 2017 06:49:17 GMT'], b'Etag': [b'"359670651"'], b'Expires': [b'Wed, 01 Nov 2017 06:49:17 GMT'], b'Last-Modified': [b'Fri, 09 Aug 2013 23:54:35 GMT'], b'Server': [b'ECS (mdw/1275)'], b'Vary': [b'Accept-Encoding'], b'X-Cache': [b'HIT']}

### Show the response object

    $ curl "http://localhost:8080/api/eval/response"

    <200 http://www.example.com/>

### Show the spider object

    $ curl "http://localhost:8080/api/eval/self"

    <Spider 'parse' at 0x7f3a3af2fb38>

    $ curl "http://localhost:8080/api/eval/self.__dict__"

    {'settings': <scrapy.settings.Settings object at 0x7f3a3af47e10>, 'result': {...}, 'crawler': <scrapy.crawler...>}
