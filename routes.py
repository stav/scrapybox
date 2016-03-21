import api


def add(router):
    f = router.add_route
    f('GET', '/api/v1/example',            api.example)
