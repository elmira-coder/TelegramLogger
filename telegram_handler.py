import logging
import json
import os
import requests
from config import BOT_TOKEN, SUBSCRIBERS_FILE


class TelegramHandler(logging.Handler):

    @staticmethod
    def _get_subscribers_path():
        return os.path.abspath(SUBSCRIBERS_FILE)

    @staticmethod
    def _escape_html(text: str) -> str:
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    @staticmethod
    def _build_title(level: str) -> str:
        if level == "CRITICAL":
            return "🔥 CRITICAL ERROR"
        return "🚨 ERROR"

    def emit(self, record):
        try:
            subscribers = self._load_subscribers()
            if not subscribers:
                return

            formatted_text = self.format(record)

            for chat_id in subscribers:
                self._send_message(chat_id, record, formatted_text)

        except Exception:
            pass

    def _load_subscribers(self):
        try:
            with open(self._get_subscribers_path(), "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _send_message(self, chat_id, record, formatted_text):
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

        requests.post(url, json=payload, timeout=5)




