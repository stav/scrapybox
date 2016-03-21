import asyncio
import _twisted_monkey_patches
import twisted.internet.reactor
twisted.internet.reactor.run()

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
configure_logging(get_project_settings())

# import aiohttp_debugtoolbar
import aiohttp.web
import api

async def on_shutdown(app):
    print('@@@', app)
    pass

app = aiohttp.web.Application(
    loop=asyncio.get_event_loop(),
    # middlewares=[aiohttp_debugtoolbar.toolbar_middleware_factory]
)
# aiohttp_debugtoolbar.setup(app)  # http://127.0.0.1:8080/_debugtoolbar
app.router.add_route('GET', '/api/v1/{route}', api.route)
app.on_shutdown.append(on_shutdown)

aiohttp.web.run_app(app)
