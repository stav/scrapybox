"""
Scrapybox - A Scrapy server joint
"""
# __all__ = ['__version__', 'version_info', 'api', 'routes', 'server']

__version__ = '0.1'
version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))
