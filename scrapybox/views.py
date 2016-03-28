# import asyncio
import aiohttp_jinja2


@aiohttp_jinja2.template('home.j2.html')
def default(request):
    return {}


# @asyncio.coroutine
# def handler(request):
#     context = {'name': 'Andrew', 'surname': 'Svetlov'}
#     response = aiohttp_jinja2.render_template(
#         'tmpl.j2.html', request, context)
#     response.headers['Content-Language'] = 'ru'
#     return response
