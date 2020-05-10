import logging


def get_orm_logger(name: str = 'liteorm', log_level=logging.INFO):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger
