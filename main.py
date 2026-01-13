# main.py

import threading
from logger_setup import setup_logger
from error_loop import error_loop
from bot_runner import run_bot


def main():
    logger = setup_logger()
    logger.info("Приложение запущено")

    # Запуск генератора ошибок в отдельном потоке
    error_thread = threading.Thread(
        target=error_loop,
        args=(logger,),
        daemon=True
    )
    error_thread.start()

    # Запуск Telegram-бота (основной поток)
    run_bot()


if __name__ == "__main__":
    main()
