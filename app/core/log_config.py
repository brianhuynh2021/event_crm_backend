import logging
from pythonjsonlogger import jsonlogger


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(funcName)s %(lineno)d"
    )

    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
