# Custom Logger Using Loguru

import logging
import sys
from pathlib import Path
from loguru import logger
import json


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class CustomizeLogger:

    @classmethod
    def make_logger(cls, config_path: Path = None):

        if config_path is None:
            config_path = Path(__file__).with_name("logging.json")

        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        _logger = cls.customize_logging(
            logging_config.get('path'),
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            _format=logging_config.get('format')
        )
        return _logger

    @classmethod
    def customize_logging(
            cls,
            filepath: Path,
            level: str,
            rotation: str,
            retention: str,
            _format: str
    ):

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=_format
        )
        # logger.add(
        #     str(filepath),
        #     rotation=rotation,
        #     retention=retention,
        #     enqueue=True,
        #     backtrace=True,
        #     level=level.upper(),
        #     format=_format
        # )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
