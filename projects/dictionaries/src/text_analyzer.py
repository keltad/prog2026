import re
from pathlib import Path


def read_text_from_file(file_path: Path | str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


class TextAnalyzer:

    def __init__(self, text: str):
        self.text = text
        self.words = self._extract_words()
        self.letters = self._extract_letters()
        self.word_counts = self._build_frequency_dict(self.words)
        self.letter_counts = self._build_frequency_dict(self.letters)

    def _extract_words(self) -> list[str]:
        return re.findall(r"\b[a-zA-Zа-яА-ЯіІїЇєЄґҐ']+\b", self.text.lower())

    def _extract_letters(self) -> list[str]:
        return [char.lower() for char in self.text if char.isalpha()]

    def _build_frequency_dict(self, items: list[str]) -> dict[str, int]:
        stats_dict = {}
        for item in items:
            if item in stats_dict:
                stats_dict[item] += 1
            else:
                stats_dict[item] = 1
        return stats_dict

    def get_frequency_dict_pct(self) -> dict[str, float]:
        if not self.words:
            return {}
        total_words = len(self.words)
        return {
            word: round((count / total_words) * 100, 2)
            for word, count in self.word_counts.items()
        }

    def get_shortest_words(self) -> list[str]:
        if not self.words:
            return []
        min_len = min(len(w) for w in self.words)
        return [w for w in self.word_counts.keys() if len(w) == min_len]

    def get_longest_words(self) -> list[str]:
        if not self.words:
            return []
        max_len = max(len(w) for w in self.words)
        return [w for w in self.word_counts.keys() if len(w) == max_len]

    def get_unique_words_count(self) -> int:
        return len(self.word_counts)

    def get_total_words_count(self) -> int:
        return len(self.words)

    def get_used_letters(self) -> list[str]:
        return sorted(list(self.letter_counts.keys()))

    def get_most_frequent_letter(self) -> list[str]:
        if not self.letters:
            return []
        max_count = max(self.letter_counts.values())
        return [char for char, count in self.letter_counts.items() if count == max_count]