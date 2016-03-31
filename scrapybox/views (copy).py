# import asyncio
import queue
import logging
import logging.handlers
import aiohttp
import aiohttp_jinja2

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template('home.j2.html')
def default(request):
    return {}


@aiohttp_jinja2.template('sockettest.j2.html')
def sockettest(request):
    return {}


class SocketQueueListener(logging.handlers.QueueListener):
    socket = None
    def prepare(self, record):
        if self.socket:
            self.socket.send_str(record.msg)
        return record


async def socketconn(request):

    ws = aiohttp.web.WebSocketResponse()
    logger.debug('WebSocket opened {}'.format(ws))
    await ws.prepare(request)
    logger.debug('WebSocket prepared {}'.format(ws))

    formatter = logging.Formatter('%(threadName)s: %(message)s')

    que = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(que)
    queue_handler.setFormatter(formatter)

    listener = SocketQueueListener(que, queue_handler)
    listener.socket = ws

    root_logger = logging.getLogger('')
    root_logger.addHandler(queue_handler)

    listener.start()
    root_logger.warning('Look out!')

    import scrapybox.api
    class Request():
        POST = None
        async def post(self):
            self.POST = {'yield_item': True, 'settings.HTTPCACHE_ENABLED': True}
    request = Request()
    response = await scrapybox.api.parse_post(request)
    logger.debug('Response {} keys: {}'.format(len(response), str(response)[:200]))

    root_logger.removeHandler(queue_handler)
    listener.stop()
    ws.send_str('close')

    async for msg in ws:
        logger.debug('WebSocket received {}'.format(msg))
        if msg.tp == aiohttp.MsgType.text:
            if msg.data == 'close':
                await ws.close()
            else:
                ws.send_str(msg.data + '/answer')
        elif msg.tp == aiohttp.MsgType.error:
            logger.warning('WebSocket error: {}'.format(ws.exception()))

    logger.debug('WebSocket closed {}'.format(ws))

    return ws

# @asyncio.coroutine
# def handler(request):
#     context = {'name': 'Andrew', 'surname': 'Svetlov'}
#     response = aiohttp_jinja2.render_template(
#         'tmpl.j2.html', request, context)
#     response.headers['Content-Language'] = 'ru'
#     return response
