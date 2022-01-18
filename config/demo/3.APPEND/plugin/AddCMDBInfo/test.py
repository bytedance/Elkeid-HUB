
import logging
from logging import config

import plugin

if __name__ == '__main__':
    instance = plugin.Plugin()
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': "INFO"
        }
    }
    config.dictConfig(logging_config)
    instance.log = logging
    instance.plugin_exec(
            {"arg": "elkeid"},
            {"k":"v"}
    )

