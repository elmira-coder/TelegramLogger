# telegram_handler.py
"""
Модуль для отправки уведомлений об ошибках в Telegram через логгер.

Файл:
- Определяет класс TelegramHandler, который наследует logging.Handler.
- Используется в logger_setup.py для отправки ошибок уровня ERROR и CRITICAL.
- Отправляет сообщения подписанным пользователям, форматируя текст и стек-трейс.
"""

import logging
import json
import os
import requests
from config import BOT_TOKEN, SUBSCRIBERS_FILE


class TelegramHandler(logging.Handler):
    """
    Обработчик логов для Telegram.

    Основная идея:
    - Берёт записи логов уровня ERROR/CRITICAL.
    - Получает список подписчиков из subscribers.json.
    - Отправляет каждому подписчику сообщение через Telegram Bot API.
    """

    @staticmethod
    def _get_subscribers_path():
        """Возвращает абсолютный путь к файлу подписчиков."""
        return os.path.abspath(SUBSCRIBERS_FILE)

    @staticmethod
    def _escape_html(text: str) -> str:
        """
        Экранирует символы HTML в тексте, чтобы Telegram корректно отображал текст в <pre>.
        Например: &, <, > заменяются на &amp;, &lt;, &gt;
        """
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    @staticmethod
    def _build_title(level: str) -> str:
        """
        Возвращает заголовок сообщения в зависимости от уровня ошибки.
        CRITICAL → 🔥 CRITICAL ERROR
        ERROR → 🚨 ERROR
        """
        if level == "CRITICAL":
            return "🔥 CRITICAL ERROR"
        return "🚨 ERROR"

    def emit(self, record):
        """
        Метод вызывается логгером при записи сообщения.

        Действия:
        1. Загружает список подписчиков.
        2. Если подписчиков нет — ничего не делает.
        3. Форматирует запись лога.
        4. Отправляет каждому подписчику сообщение через Telegram.
        """
        try:
            subscribers = self._load_subscribers()
            if not subscribers:
                return

            formatted_text = self.format(record)

            for chat_id in subscribers:
                self._send_message(chat_id, record, formatted_text)

        except Exception:
            # Игнорируем ошибки внутри обработчика, чтобы логгер не ломался
            pass

    def _load_subscribers(self):
        """
        Загружает список подписчиков из файла subscribers.json.
        Если файла нет или он пустой/невалидный, возвращает пустой список.
        """
        try:
            with open(self._get_subscribers_path(), "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _send_message(self, chat_id, record, formatted_text):
        """
        Отправляет сообщение в Telegram.

        Действия:
        1. Строит URL для вызова Telegram Bot API.
        2. Определяет заголовок (CRITICAL/ERROR).
        3. Форматирует сообщение с HTML тегами:
           - <b> заголовок </b>
           - <pre> стек-трейс </pre>
        4. Ограничивает сообщение 4096 символами (лимит Telegram).
        5. Отправляет POST-запрос на Telegram API.
        """
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        title = self._build_title(record.levelname)

        message = (
                f"<b>{title}</b>\n\n"
                "<pre>"
                + self._escape_html(formatted_text) +
                "</pre>"
        )

        payload = {
            "chat_id": chat_id,
            "text": message[:4096],
            "parse_mode": "HTML"
        }

        # Отправка сообщения (timeout=5 секунд, чтобы не блокировать)
        requests.post(url, json=payload, timeout=5)
