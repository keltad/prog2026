from name_tools import count_letters, is_latin
import task1
import task3


def main() -> None:
    name = input("Введи своє ім'я латиницею: ").strip()
    if not is_latin(name):
        print("Ім'я має складатися лише з латинських літер.")
        return

    print("\n--- Завдання 1: генератор пароля ---")
    task1.run(name)

    print("\n--- Завдання 2: власний модуль name_tools ---")
    print(f"is_latin('{name}') = {is_latin(name)}")
    print(f"count_letters('{name}') = {count_letters(name)}")

    print("\n--- Завдання 3: три модулі (random, datetime, requests) ---")
    task3.run()


if __name__ == "__main__":
    main()