"""Читає два тексти з файлів і зберігає метрики WER, S, D, I, N у JSON-файл.

Запуск:
    python main.py
    python main.py data/reference.txt data/hypothesis.txt result.json
"""

import json
import sys
from pathlib import Path

from wer import word_error_rate


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    base = Path(__file__).parent
    reference_path = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "data" / "reference.txt"
    hypothesis_path = Path(sys.argv[2]) if len(sys.argv) > 2 else base / "data" / "hypothesis.txt"
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else base / "result.json"

    reference = read_text(reference_path)
    hypothesis = read_text(hypothesis_path)

    result = word_error_rate(reference, hypothesis)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=4)

    print(f"WER = {result.wer:.4f} ({result.wer:.2%})")
    print(f"S = {result.S}, D = {result.D}, I = {result.I}, N = {result.N}")
    print(f"Результат збережено у {output_path}")


if __name__ == "__main__":
    main()