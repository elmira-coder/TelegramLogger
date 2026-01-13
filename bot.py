# bot.py

import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, SUBSCRIBERS_FILE


def get_subscribers_path():
    return os.path.abspath(SUBSCRIBERS_FILE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print(f"Subscribers file: {get_subscribers_path()}")

app.run_polling()
