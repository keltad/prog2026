"""Завдання 1. Власний виняток EmptyTextError і функція analyze_text."""

class EmptyTextError(Exception):
    """Виняток: переданий текст порожній."""
    pass


def analyze_text(text):
    if not isinstance(text, str):
        raise TypeError("text має бути рядком (str)")
    if not text.strip():
        raise EmptyTextError("текст порожній")
    return len(text)


def run():
    print("=== Завдання 1 ===")
    samples = ["Привіт, світ!", "", "   ", 12345]
    for sample in samples:
        try:
            count = analyze_text(sample)
            print(f"{sample!r}: {count} символів")
        except EmptyTextError as e:
            print(f"{sample!r}: помилка — {e}")
        except TypeError as e:
            print(f"{sample!r}: помилка — {e}")