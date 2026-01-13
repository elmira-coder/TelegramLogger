# error_loop.py

import time
import random
from error_generator import generate_error


def error_loop(logger):
    logger.info("Генератор ошибок запущен")

    while True:
        try:
            time.sleep(random.randint(5, 20))

            if random.random() < 0.6:
                generate_error()
            else:
                logger.info("Итерация без ошибок")

        except Exception:
            logger.exception("Автоматически сгенерированная ошибка")
