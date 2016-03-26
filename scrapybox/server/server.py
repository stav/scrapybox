import asyncio
import scrapybox.server._twisted_monkey_patches
import twisted.internet.reactor

# import aiohttp_debugtoolbar
import aiohttp.web

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings as settings

import scrapybox.server.routes


async def on_shutdown(app):
    # http://aiohttp.readthedocs.org/en/stable/web.html#graceful-shutdown
    # for ws in app['websockets']:
    #     await ws.close(code=999, message='Server shutdown')
    print('Shutting down...')
    # print(asyncio.Server.sockets, 'open sockets for asyncio')
    # asyncio.Server.close()
    # print(aiohttp.web.connections, 'open connections for aiohttp')
    app.shutdown()
    # aiohttp.web.finish_connections(5)
    app.cleanup()
    print('done.')


def main():
    configure_logging(settings())
    twisted.internet.reactor.run()

    app = aiohttp.web.Application(
        loop=asyncio.get_event_loop(),
        # middlewares=[aiohttp_debugtoolbar.toolbar_middleware_factory]
    )
    # aiohttp_debugtoolbar.setup(app)  # http://127.0.0.1:8080/_debugtoolbar
    app.on_shutdown.append(on_shutdown)

    scrapybox.server.routes.add(app.router)

    aiohttp.web.run_app(app)

if __name__ == '__main__':
    main()
