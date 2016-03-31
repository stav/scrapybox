import sys
import logging
import logging.config
import twisted.python.log
import scrapy.settings
import scrapy.utils.project

logger = logging.getLogger(__name__)

config = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'twisted': {
            'level': 'INFO',
        },
    }
}


def configure():
    # if not sys.warnoptions:
    #     logging.captureWarnings(True)

    # observer = twisted.python.log.PythonLoggingObserver('twisted')
    # observer.start()

    logging.config.dictConfig(config)

    settings = scrapy.utils.project.get_project_settings()

    # if settings.getbool('LOG_STDOUT'):
    #     sys.stdout = StreamLogger(logging.getLogger('stdout'))

    formatter = logging.Formatter(
        fmt='* [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(settings.get('LOG_LEVEL'))

    logging.root.addHandler(handler)
    logging.root.setLevel(logging.NOTSET)
