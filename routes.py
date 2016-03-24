import api


def add(router):
    ar = router.add_route
    ar('GET', '/api/example',           api.example)
    ar('GET', '/api/parse/eval/{code}', api.parse_eval)
    ar('GET', '/api/delay/{time}',      api.delay)
