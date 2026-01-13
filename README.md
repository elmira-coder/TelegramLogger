# Telegram Logger

Проект демонстрирует систему логирования на Python с интеграцией Telegram-бота.  
Логгер пишет ошибки в файл и отправляет уведомления пользователям бота в Telegram.  
Также реализован генератор случайных ошибок для демонстрации работы логгера в реальном времени.

---

## Функциональность

- Логирование ошибок в файл (`app.log`).
- Уведомления об ошибках уровня `ERROR` и `CRITICAL` через Telegram.
- Генерация случайных ошибок для демонстрации.
- Поддержка подписки пользователей через команду `/start`.
- Единый запуск: бот и генератор ошибок запускаются в одном процессе (`main.py`).

---

## Требования

- Python 3.12+
- pip
- Docker (опционально, для запуска через контейнер)

---

## Установка и запуск локально

1. Клонируйте репозиторий:

```bash
git clone <URL_репозитория>
cd TelegramLogger
```

2. Создайте виртуальное окружение (рекомендуется):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Настройте config.py:
- Вставьте токен своего Telegram-бота (BOT_TOKEN).

5. Запустите проект:
```bash
python main.py
```

Telegram-бот запустится.
Генератор ошибок начнёт периодически создавать исключения.
Ошибки пишутся в файл и отправляются в Telegram.

---

## Запуск через Docker

1. Соберите Docker-образ:
```bash
docker build -t telegram_logger .
```

2. Запустите контейнер в фоне:
```bash
docker run -d --name telegram_logger telegram_logger
```

3. Чтобы увидеть логи контейнера:
```bash
docker logs -f telegram_logger
```

4. Чтобы остановить контейнер:
```bash
docker stop telegram_logger
docker rm telegram_logger
```
---

## Как подписаться на уведомления
1. Откройте Telegram и найдите вашего бота (тот токен, который указан в config.py).
2. Отправьте команду /start.
3. Ваш chat_id добавится в список подписчиков, и все ошибки уровня ERROR и CRITICAL будут приходить вам в Telegram.

---

## Структура проекта
```yml
project/
├── main.py             # Единый запуск приложения
├── bot_runner.py       # Запуск Telegram-бота
├── error_loop.py       # Генератор случайных ошибок
├── logger_setup.py     # Настройка логгера
├── telegram_handler.py # Handler для отправки сообщений в Telegram
├── error_generator.py  # Список случайных ошибок
├── config.py           # Конфигурация проекта (токен, файлы)
├── subscribers.json    # Файл с chat_id подписчиков
└── requirements.txt    # Зависимости Python
```

