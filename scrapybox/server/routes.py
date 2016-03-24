from scrapybox.server import api


def add(router):
    ar = router.add_route
    ar('POST', '/api/eval',         api.parse_post)
    ar('GET',  '/api/eval/{code}',  api.parse_get)
    ar('GET',  '/api/delay/{time}', api.delay)
    ar('GET',  '/api/hello',        api.hello)
