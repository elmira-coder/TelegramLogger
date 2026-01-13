# app.py

import time
import random
from logger_setup import setup_logger
from error_generator import generate_error

logger = setup_logger()

logger.info("Приложение запущено и работает постоянно")

while True:
    try:
        # случайная пауза от 5 до 20 секунд
        time.sleep(random.randint(5, 120))

        # случайно: будет ошибка или нет
        if random.random() < 0.6:
            generate_error()
        else:
            logger.info("Очередная итерация без ошибок")

    except Exception:
        logger.exception("Автоматически сгенерированная ошибка")
