# bot_runner.py
"""
Модуль запуска Telegram-бота для подписки пользователей на уведомления об ошибках.

Используется в основном приложении (main.py), чтобы бот работал параллельно с генератором ошибок.
"""

import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, SUBSCRIBERS_FILE


def get_subscribers_path():
    """
    Возвращает полный путь к файлу с подписчиками (subscribers.json),
    чтобы бот знал, куда сохранять chat_id пользователей.
    """
    return os.path.abspath(SUBSCRIBERS_FILE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.

    Действия:
    1. Получает chat_id пользователя, который отправил команду.
    2. Загружает существующий список подписчиков или создаёт новый.
    3. Добавляет пользователя в список, если его там ещё нет.
    4. Сохраняет обновлённый список в файл.
    5. Отправляет пользователю сообщение-подтверждение.
    """
    chat_id = update.effective_chat.id
    path = get_subscribers_path()

    try:
        with open(path, "r", encoding="utf-8") as f:
            subscribers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        subscribers = []

    if chat_id not in subscribers:
        subscribers.append(chat_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(subscribers, f)

    await update.message.reply_text(
        "Вы подписаны на уведомления об ошибках."
    )


def run_bot():
    """
    Создаёт и запускает Telegram-бота.

    Действия:
    1. Создаёт объект ApplicationBuilder с токеном бота.
    2. Регистрирует обработчик команды /start.
    3. Выводит сообщение о запуске.
    4. Запускает polling (постоянное получение новых сообщений от пользователей).

    Этот метод блокирует основной поток, поэтому генератор ошибок нужно запускать
    в отдельном потоке, если требуется параллельная работа.
    """
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Telegram-бот запущен")
    app.run_polling()
