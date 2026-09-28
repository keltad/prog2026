from pathlib import Path
from text_analyzer import TextAnalyzer, read_text_from_file

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    FILE_PATH = BASE_DIR / "data" / "text.txt"
    OUTPUT_PATH = BASE_DIR / "data" / "result.txt"

    if not FILE_PATH.exists():
        print(f"Помилка: Файл не знайдено за шляхом: {FILE_PATH}")
    else:
        text_data = read_text_from_file(FILE_PATH)
        analyzer = TextAnalyzer(text_data)

        analyzer.save_report(OUTPUT_PATH)
        
        print(f"Аналіз завершено! Результати збережено у файл:\n{OUTPUT_PATH}")