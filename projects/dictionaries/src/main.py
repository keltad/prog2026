from pathlib import Path
from text_analyzer import TextAnalyzer, read_text_from_file

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    FILE_PATH = BASE_DIR / "data" / "text.txt"

    if not FILE_PATH.exists():
        print(f"Помилка: Файл не знайдено за шляхом: {FILE_PATH}")
    else:
        text_data = read_text_from_file(FILE_PATH)
        analyzer = TextAnalyzer(text_data)

        print("=== Результати аналізу тексту ===")
        print("Загальна кількість слів:", analyzer.get_total_words_count())
        print("Кількість унікальних слів:", analyzer.get_unique_words_count())
        print("Найкоротші слова:", analyzer.get_shortest_words())
        print("Найдовші слова:", analyzer.get_longest_words())
        print("Використані літери:", analyzer.get_used_letters())
        print("Найчастіша літера:", analyzer.get_most_frequent_letter())

        print("\nЧастотний словник слів (%):")
        for word, pct in analyzer.get_frequency_dict_pct().items():
            print(f"  {word}: {pct}%")