"""
Scrapybox - A Scrapy server joint
"""
# __all__ = ['__version__', 'version_info', '_twisted_monkey_patches',
#            'api', 'routes', 'server']

__version__ = '0.1'
version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))

# import server.api
# import server.routes
