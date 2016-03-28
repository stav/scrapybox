import scrapybox.server._twisted_monkey_patches

import os
import asyncio
import logging
import aiohttp.web
import aiohttp_jinja2
# import aiohttp_debugtoolbar
import twisted.internet.reactor
import jinja2

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import scrapybox.server.routes

logger = logging.getLogger(__name__)
settings = get_project_settings()
user_path = os.path.join(os.getcwd(), 'scrapybox/user')


async def on_shutdown(app):
    """
    LOG_STDOUT

        If logging stdout then StreamLogger needs a flush() method.
        To recreate: enable LOG_STDOUT, run server, ^C interrupt:
        Exception ignored in: <scrapy.utils.log.StreamLogger object at 0x7f...>
        AttributeError: 'StreamLogger' object has no attribute 'flush'

    twisted_log.PythonLoggingObserver

        Observer is started in configure_logging, do we need to close it?

    Close all opened sockets manually:

        http://aiohttp.readthedocs.org/en/stable/web.html#graceful-shutdown

        for ws in app['websockets']:
            await ws.close(code=999, message='Server shutdown')
    """
    logger.info('Scrapybox server shutting down')
    # print(asyncio.Server.sockets, 'open sockets for asyncio')
    # asyncio.Server.close()
    # print(aiohttp.web.connections, 'open connections for aiohttp')
    app.shutdown()
    # aiohttp.web.finish_connections(5)
    app.cleanup()
    logger.info('Scrapybox server shutdown complete')


def main():
    """
    Scrapy pull request:
        configure_logging() should accept a config argument

    Note:
        scrapy.utils.log.TopLevelFormatter is cool
        need to access Scrapy loggger's handler and replace the filter with a new
        TopLevelFormatter with more names: e.g. ['scrapy', 'scrapybox', 'aiohttp']
    """
    configure_logging(settings)
    logger.info('Scrapybox server starting')
    # formatter = logging.Formatter(fmt=settings.get('LOG_FORMAT'),
    #                               datefmt=settings.get('LOG_DATEFORMAT'))
    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    # handler.setLevel(settings.get('LOG_LEVEL'))
    # logging.root.addHandler(handler)

    twisted.internet.reactor.run()
    logger.info('Twisted reactor running')

    app = aiohttp.web.Application(
        loop=asyncio.get_event_loop(),
        # middlewares=[aiohttp_debugtoolbar.toolbar_middleware_factory]
    )
    # aiohttp_debugtoolbar.setup(app)  # http://127.0.0.1:8080/_debugtoolbar
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(user_path))
    app.on_shutdown.append(on_shutdown)
    app['static_path'] = user_path

    scrapybox.server.routes.add(app)

    logger.info('Aiohttp server starting')
    aiohttp.web.run_app(app)

if __name__ == '__main__':
    main()
