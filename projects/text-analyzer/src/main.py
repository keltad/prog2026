"""Консольна програма: аналіз тексту з файлу.

Приклади (із кореня проєкту):
    uv run python src/main.py data/sample_uk.txt
    uv run python src/main.py sample_en.txt --top 15
    uv run python src/main.py sample_uk.txt --lemmas
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from analyzer import AnalysisResult, TextAnalyzerError, analyze_file

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LANGUAGE_NAMES = {"uk": "українська", "en": "англійська"}


def resolve_path(name: str) -> Path:
    """Якщо файлу за вказаним шляхом немає, шукаємо його в папці data."""
    path = Path(name)
    if not path.is_absolute() and not path.exists():
        return DATA_DIR / path
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Аналіз тексту (українська або англійська): "
        "кількість слів і словник частотності."
    )
    parser.add_argument("file", help="шлях до .txt файлу (або ім'я файлу з папки data)")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="скільки найчастіших слів показати (0 - усі), за замовчуванням 10",
    )
    parser.add_argument(
        "--lemmas",
        action="store_true",
        help="рахувати початкові форми слів (лише для української, pymorphy3)",
    )
    return parser


def format_report(result: AnalysisResult, top: int) -> str:
    items = list(result.frequencies.items())
    if top > 0:
        items = items[:top]

    unit = "унікальних лем" if result.lemmatized else "унікальних слів"
    lines = [
        f"Мова тексту: {LANGUAGE_NAMES.get(result.language, result.language)}",
        f"Усього слів: {result.total_words}",
        f"Кількість {unit}: {result.unique_words}",
        "",
        "Словник частотності:",
    ]
    width = max(len(word) for word, _ in items)
    lines += [f"  {word:<{width}}  {count}" for word, count in items]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = analyze_file(resolve_path(args.file), use_lemmas=args.lemmas)
    except TextAnalyzerError as error:
        print(f"Помилка: {error}", file=sys.stderr)
        return 1

    if args.lemmas and not result.lemmatized:
        print("Увага: лематизація доступна лише для української, "
              "показано звичайні форми слів.\n")
    print(format_report(result, args.top))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
