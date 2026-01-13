# logger_setup.py

import logging
from config import LOG_FILE, LOG_LEVEL, ENABLE_TELEGRAM
from telegram_handler import TelegramHandler


def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d\n%(message)s"
    )

    # Файл
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Telegram — только ERROR и CRITICAL
    if ENABLE_TELEGRAM:
        tg_handler = TelegramHandler()
        tg_handler.setLevel(logging.ERROR)
        tg_handler.setFormatter(formatter)
        logger.addHandler(tg_handler)

    return logger
