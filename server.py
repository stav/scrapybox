import asyncio
import _twisted_monkey_patches
import twisted.internet.reactor

# import aiohttp_debugtoolbar
import aiohttp.web

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings as settings

import routes

configure_logging(settings())
twisted.internet.reactor.run()

async def on_shutdown(app):
    print('@@@', app)
    pass

app = aiohttp.web.Application(
    loop=asyncio.get_event_loop(),
    # middlewares=[aiohttp_debugtoolbar.toolbar_middleware_factory]
)
# aiohttp_debugtoolbar.setup(app)  # http://127.0.0.1:8080/_debugtoolbar
app.on_shutdown.append(on_shutdown)

routes.add(app.router)

aiohttp.web.run_app(app)
