"""Завдання 3. Читання data/sample.txt і підрахунок символів, слів та рядків."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FILE = PROJECT_ROOT / "data" / "sample.txt"


def run(filename=DEFAULT_FILE):
    print("=== Завдання 3 ===")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Помилка: файл '{filename}' не знайдено.")
        return
    except PermissionError:
        print(f"Помилка: немає доступу до файлу '{filename}'.")
        return
    except UnicodeDecodeError:
        print(f"Помилка: не вдалося розкодувати '{filename}' (очікується UTF-8).")
        return

    print("Вміст файлу:")
    print(content)
    print("-" * 30)
    print(f"Кількість символів: {len(content)}")
    print(f"Кількість слів:     {len(content.split())}")
    print(f"Кількість рядків:   {len(content.splitlines())}")