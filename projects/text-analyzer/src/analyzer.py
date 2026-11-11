"""Логіка аналізу тексту: читання файлу, підрахунок слів, словник частотності.

Використані бібліотеки:
    * NLTK      - токенізація (RegexpTokenizer) і підрахунок частот (FreqDist);
    * pymorphy3 - лематизація українських слів (необов'язковий режим).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer

_TOKENIZER = RegexpTokenizer(r"[^\W\d_]+(?:['\-][^\W\d_]+)*")

_APOSTROPHES = str.maketrans({"’": "'", "ʼ": "'", "`": "'"})


class TextAnalyzerError(Exception):
    """Базовий клас помилок програми."""


class EmptyTextError(TextAnalyzerError):
    """Текст порожній або не містить жодного слова."""


class TextReadError(TextAnalyzerError):
    """Файл неможливо прочитати."""


@dataclass(frozen=True)
class AnalysisResult:
    """Результат аналізу тексту."""

    language: str  
    total_words: int 
    unique_words: int  
    frequencies: dict[str, int]  
    lemmatized: bool = False


def read_text(path: str | Path) -> str:
    """Прочитати текст із файлу (UTF-8, BOM із Блокнота Windows допускається).

    Raises:
        TextReadError: файлу немає, це папка, немає доступу або не UTF-8.
    """
    path = Path(path)
    try:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise TextReadError(f"Файл не знайдено: {path}") from None
    except IsADirectoryError:
        raise TextReadError(f"Це папка, а не файл: {path}") from None
    except PermissionError:
        raise TextReadError(f"Немає доступу до файлу: {path}") from None
    except UnicodeDecodeError:
        raise TextReadError(
            f"Файл {path} не в кодуванні UTF-8. Збережіть його як UTF-8."
        ) from None
    except OSError as error:
        raise TextReadError(f"Не вдалося прочитати файл {path}: {error}") from None


def detect_language(text: str) -> str:
    """Визначити мову за співвідношенням кирилиці й латиниці: "uk" або "en"."""
    cyrillic = sum("\u0400" <= ch <= "\u04ff" for ch in text)
    latin = sum(("a" <= ch <= "z") or ("A" <= ch <= "Z") for ch in text)
    return "uk" if cyrillic > latin else "en"


def tokenize(text: str) -> list[str]:
    """Розбити текст на слова в нижньому регістрі (NLTK RegexpTokenizer)."""
    normalized = text.translate(_APOSTROPHES).lower()
    return _TOKENIZER.tokenize(normalized)


def count_words(words: list[str]) -> int:
    """Кількість слів."""
    return len(words)


def build_frequency_dict(words: list[str]) -> dict[str, int]:
    """Словник частотності (NLTK FreqDist): від частіших слів до рідших.

    Слова з однаковою частотою йдуть за алфавітом, тому результат стабільний.
    """
    distribution = FreqDist(words)
    ordered = sorted(distribution.items(), key=lambda item: (-item[1], item[0]))
    return dict(ordered)


@lru_cache(maxsize=1)
def _ukrainian_morph():
    import pymorphy3  

    return pymorphy3.MorphAnalyzer(lang="uk")


def lemmatize(words: list[str], language: str) -> list[str]:
    """Звести слова до початкової форми (pymorphy3).

    pymorphy3 підтримує лише українську (і російську), тому для інших мов
    слова повертаються без змін.
    """
    if language != "uk":
        return list(words)
    morph = _ukrainian_morph()
    return [morph.parse(word)[0].normal_form for word in words]


def analyze_text(text: str, use_lemmas: bool = False) -> AnalysisResult:
    """Проаналізувати текст.

    Raises:
        EmptyTextError: текст порожній або в ньому немає слів.
    """
    if not text or not text.strip():
        raise EmptyTextError("Текст порожній.")

    words = tokenize(text)
    if not words:
        raise EmptyTextError("У тексті немає жодного слова.")

    language = detect_language(text)
    lemmatized = use_lemmas and language == "uk"
    if lemmatized:
        words = lemmatize(words, language)

    frequencies = build_frequency_dict(words)
    return AnalysisResult(
        language=language,
        total_words=count_words(words),
        unique_words=len(frequencies),
        frequencies=frequencies,
        lemmatized=lemmatized,
    )


def analyze_file(path: str | Path, use_lemmas: bool = False) -> AnalysisResult:
    """Прочитати файл і проаналізувати його вміст."""
    return analyze_text(read_text(path), use_lemmas=use_lemmas)
