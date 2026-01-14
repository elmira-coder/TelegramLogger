# logger_setup.py
"""
Модуль настройки логгера приложения.

Файл:
- Создаёт объект логгера, который пишет сообщения в файл и при необходимости в Telegram.
- Поддерживает разные уровни логирования (INFO, ERROR, CRITICAL и т.д.).
- Telegram-уведомления отправляются только для ошибок уровня ERROR и CRITICAL.
"""

import logging
from config import LOG_FILE, LOG_LEVEL, ENABLE_TELEGRAM
from telegram_handler import TelegramHandler


def setup_logger():
    """
    Создаёт и настраивает логгер для приложения.

    Действия:
    1. Создаёт логгер с именем "app_logger".
    2. Устанавливает уровень логирования (LOG_LEVEL из config.py).
    3. Создаёт формат сообщений, включающий:
       - Время
       - Уровень ошибки
       - Имя файла и номер строки
       - Сообщение
    4. Добавляет обработчик для записи в файл (LOG_FILE).
    5. При включённом ENABLE_TELEGRAM добавляет обработчик для отправки ошибок в Telegram
       (только уровни ERROR и CRITICAL).
    6. Возвращает готовый объект логгера.
    """

    # Создаём логгер с именем app_logger
    logger = logging.getLogger("app_logger")
    logger.setLevel(LOG_LEVEL)  # Устанавливаем уровень логирования

    # Форматирование сообщений
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d\n%(message)s"
    )

    # ----------------------------
    # 1. Запись логов в файл
    # ----------------------------
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # ----------------------------
    # 2. Отправка ошибок в Telegram (только ERROR и CRITICAL)
    # ----------------------------
    if ENABLE_TELEGRAM:
        tg_handler = TelegramHandler()
        tg_handler.setLevel(logging.ERROR)  # Только ошибки и критические
        tg_handler.setFormatter(formatter)
        logger.addHandler(tg_handler)

    # Возвращаем настроенный логгер
    return logger
