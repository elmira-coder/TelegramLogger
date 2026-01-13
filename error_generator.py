# error_generator.py

import random
import math


def generate_error():
    errors = [
        # Арифметика
        lambda: 1 / 0,
        lambda: math.sqrt(-1),

        # Преобразование типов
        lambda: int("abc"),
        lambda: float("nan_value"),

        # Коллекции
        lambda: [][1],
        lambda: {}["key"],
        lambda: (1,)[2],

        # Файлы
        lambda: open("missing_file.txt"),
        lambda: open("/root/forbidden.txt"),

        # Импорт
        lambda: __import__("non_existing_module"),

        # Атрибуты
        lambda: None.upper(),
        lambda: (10).append(5),

        # Индексы строк
        lambda: "abc"[10],

        # Деление по модулю
        lambda: 10 % 0
    ]

    error = random.choice(errors)
    error()

