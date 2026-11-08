"""Мій власний модуль: допоміжні функції для роботи з іменем."""

import string


def is_latin(text: str) -> bool:
    """Повертає True, якщо текст складається лише з латинських літер."""
    return bool(text) and all(ch in string.ascii_letters for ch in text)


def count_letters(text: str) -> int:
    """Рахує літери в тексті (пробіли, цифри та інші символи не враховуються)."""
    return sum(ch.isalpha() for ch in text)


if __name__ == "__main__":
    print(is_latin("Oleksandr"))       
    print(is_latin("Олександр"))       
    print(count_letters("Oleksandr"))  