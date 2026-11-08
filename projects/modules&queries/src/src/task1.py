"""Завдання 1: генератор пароля.

Довжина пароля = кількість літер в імені (латиницею).
Пароль складається з:
  - шістнадцяткових символів (0-9, a-f),
  - спеціальних символів (пунктуація),
  - літер верхнього регістру (A-Z).
"""

import random
import secrets
import string

from name_tools import count_letters

HEX_CHARS = "0123456789abcdef"
PUNCTUATION = string.punctuation
UPPERCASE = string.ascii_uppercase


def generate_password(length: int) -> str:
    """Генерує пароль заданої довжини з усіх трьох груп символів."""
    if length < 3:
        raise ValueError("Довжина пароля має бути не менше 3 символів")

    # Гарантуємо хоча б по одному символу з кожної групи
    password = [
        secrets.choice(HEX_CHARS),
        secrets.choice(PUNCTUATION),
        secrets.choice(UPPERCASE),
    ]

    # Решту символів беремо з усіх груп разом
    pool = HEX_CHARS + PUNCTUATION + UPPERCASE
    password += [secrets.choice(pool) for _ in range(length - 3)]

    # Перемішуємо, щоб обов'язкові символи не стояли завжди на початку
    random.SystemRandom().shuffle(password)
    return "".join(password)


def run(name: str) -> None:
    length = count_letters(name)
    try:
        password = generate_password(length)
    except ValueError as error:
        print(f"Помилка: {error}")
        return

    print(f"Ім'я: {name} -> довжина пароля: {length}")
    print(f"Пароль: {password}")