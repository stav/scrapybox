from scrapybox import api, views


def add(app):
    ar = app.router.add_route

    # API
    ar('POST', '/api/eval',         api.parse_post)
    ar('GET',  '/api/eval/{code}',  api.parse_get)
    ar('GET',  '/api/delay/{time}', api.delay)
    ar('GET',  '/api/hello',        api.hello)

    # Client
    ar('*', '/', views.default)

    # Static
    app.router.add_static('/static', app['static_path'])
