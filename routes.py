import api


def add(router):
    f = router.add_route
    f('GET', '/api/v1/{route}', api.route)
    f('GET', '/api/v1/parse/print/{code}', api.parse_print)

