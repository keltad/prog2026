"""Завдання 2. Регулярний вираз, який вводить користувач."""

import re


REGEX_SPECIAL_CHARS = set(".^$*+?{}[]\\|()")

ERROR_SYNTAX = "Помилка: регулярний вираз має некоректний синтаксис."
ERROR_NOT_REGEX = "Помилка: введений рядок не є регулярним виразом."
ERROR_EMPTY = "Помилка: регулярний вираз не може бути порожнім."

# Набір готових прикладів для перевірки: (регулярний вираз, текст).
EXAMPLES = [
    # --- порожній ввід ---
    (r"", "abc"),
    (r"   ", "abc"),
    # --- звичайний текст, а не регулярний вираз ---
    (r"hello", "hello world"),
    (r"просто текст", "просто текст"),
    (r"12345", "12345"),
    # --- некоректний синтаксис ---
    (r"[A-Z", "Hello"),               # незакрита квадратна дужка
    (r"(abc", "abc"),                 # незакрита кругла дужка
    (r"abc)", "abc"),                 # зайва закриваюча дужка
    (r"*abc", "abc"),                 # нічого повторювати
    (r"a{3,1}", "aaa"),               # мінімум більший за максимум
    (r"(?P<name", "abc"),             # незавершена іменована група
    # --- коректні, є збіги ---
    (r"[A-Z]", "Hello World Python"),
    (r"\d+", "Замовлення 123, 45 та 6789"),
    (r"\b[\w.]+@\w+\.\w+\b", "Пишіть на ivan.petrenko@mail.com або olya@ukr.net"),
    (r"\b[А-ЯІЇЄҐ][а-яіїєґ']+", "Київ, Львів і Харків — великі міста України"),
    (r"\+380\d{9}", "Тел.: +380501234567, +380671112233"),
    (r"\d{2}\.\d{2}\.\d{4}", "Дата: 08.11.2026, а також 01.09.2025"),
    # --- коректний, збігів немає ---
    (r"\d+", "Тут зовсім немає цифр"),
]


def check_pattern(pattern_str):
    """Перевірити введений рядок.

    Повертає (скомпільований_вираз, None) або (None, текст_помилки).
    """
    if not pattern_str.strip():
        return None, ERROR_EMPTY
    if not any(ch in REGEX_SPECIAL_CHARS for ch in pattern_str):
        return None, ERROR_NOT_REGEX

    try:
        return re.compile(pattern_str), None
    except re.error:
        return None, ERROR_SYNTAX


def print_matches(pattern, text):
    matches = list(pattern.finditer(text))
    if not matches:
        print("Збігів не знайдено.")
        return
    print(f"Знайдено збігів: {len(matches)}")
    for m in matches:
        print(f"  '{m.group()}' (позиції {m.start()}-{m.end()})")


def run():
    print("=== Завдання 2 ===")
    pattern_str = input("Введіть регулярний вираз: ")

    pattern, error = check_pattern(pattern_str)
    if error:
        print(error)
        return

    text = input("Введіть текст для пошуку: ")
    print_matches(pattern, text)


def run_examples():
    """Автоматична перевірка на заготовлених виразах."""
    print("=== Завдання 2: готові приклади ===")
    for pattern_str, text in EXAMPLES:
        print(f"\nВираз: '{pattern_str}'")
        pattern, error = check_pattern(pattern_str)
        if error:
            print(error)
            continue
        print(f"Текст: {text}")
        print_matches(pattern, text)