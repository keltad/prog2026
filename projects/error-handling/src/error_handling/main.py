import task1
import task2
import task3

MENU = """
Оберіть завдання:
  1 — Завдання 1 (EmptyTextError, analyze_text)
  2 — Завдання 2 (регулярний вираз від користувача)
  3 — Завдання 3 (читання data/sample.txt)
  4 — Завдання 2: перевірка на готових виразах
  0 — Вихід"""


def main():
    actions = {
        "1": task1.run,
        "2": task2.run,
        "3": task3.run,
        "4": task2.run_examples,
    }

    while True:
        print(MENU)
        try:
            choice = input("Ваш вибір: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            break

        action = actions.get(choice)
        if action is None:
            print("Невідомий пункт меню.")
            continue
        print()
        action()


if __name__ == "__main__":
    main()