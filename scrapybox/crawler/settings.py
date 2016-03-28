"""
Scrapybox crawler settings
"""
BOT_NAME = 'Scrapybox'

SPIDER_MODULES = ['scrapybox.crawler.spiders']
NEWSPIDER_MODULE = 'scrapybox.crawler.spiders'

USER_AGENT = 'Mozilla/4.0 Scrapybox (Linux x86_64) Scrapy/1.2.0dev2 Python/3.5.0+'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1

HTTPCACHE_ENABLED = True

LOG_STDOUT = True

# DOWNLOAD_DELAY = 3
# COOKIES_ENABLED = False
