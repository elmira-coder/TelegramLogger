# bot.py
"""
Файл запускает Telegram-бота для подписки пользователей на уведомления об ошибках.

Функционал:
- Пользователь отправляет команду /start.
- Его chat_id сохраняется в файле subscribers.json.
- Все ошибки приложения будут отправляться подписанным пользователям.
"""

import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, SUBSCRIBERS_FILE


def get_subscribers_path():
    """Возвращает полный путь к файлу с chat_id подписчиков."""
    return os.path.abspath(SUBSCRIBERS_FILE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.

    Действия:
    1. Получает chat_id пользователя.
    2. Загружает список подписчиков из файла (или создаёт новый список, если файла нет).
    3. Добавляет пользователя, если его ещё нет.
    4. Сохраняет обновлённый список в файл.
    5. Отправляет подтверждение пользователю.
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


# Создаём приложение Telegram-бота
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Регистрируем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Выводим путь к файлу подписчиков (для отладки)
print(f"Subscribers file: {get_subscribers_path()}")

# Запуск бота (polling, постоянно проверяет новые сообщения)
app.run_polling()
