"""Автоматизовані тести для src/analyzer.py та src/main.py."""

from pathlib import Path

import pytest

from analyzer import (
    EmptyTextError,
    TextReadError,
    analyze_file,
    analyze_text,
    build_frequency_dict,
    count_words,
    detect_language,
    lemmatize,
    read_text,
    tokenize,
)
from main import main

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------- підрахунок слів ----------

def test_count_words_english_ignores_punctuation():
    words = tokenize("Hello, world! Hello again...")
    assert count_words(words) == 4


def test_count_words_ukrainian():
    assert count_words(tokenize("Мама мила раму. Мама!")) == 4


def test_numbers_and_symbols_are_not_words():
    assert tokenize("abc 123 def, 45% ???") == ["abc", "def"]


def test_apostrophe_and_hyphen_stay_inside_word():
    assert tokenize("М'яч і м’яч, по-перше") == ["м'яч", "і", "м'яч", "по-перше"]
    assert tokenize("a well-known idea") == ["a", "well-known", "idea"]


# ---------- словник частотності ----------

def test_frequency_dict_is_case_insensitive():
    assert build_frequency_dict(tokenize("Hello hello HELLO")) == {"hello": 3}


def test_frequency_dict_is_sorted_by_count_then_alphabet():
    frequencies = build_frequency_dict(["b", "a", "b", "c", "a", "d"])
    assert list(frequencies.items()) == [("a", 2), ("b", 2), ("c", 1), ("d", 1)]


def test_analyze_text_result_fields():
    result = analyze_text("to be or not to be")
    assert result.language == "en"
    assert result.total_words == 6
    assert result.unique_words == 4
    assert result.frequencies == {"be": 2, "to": 2, "not": 1, "or": 1}
    assert result.lemmatized is False


# ---------- мова ----------

def test_detect_language():
    assert detect_language("Привіт, світе!") == "uk"
    assert detect_language("Hello, world!") == "en"


# ---------- порожній текст ----------

@pytest.mark.parametrize("text", ["", "   \n\t  ", "... !!! ???", "123 456"])
def test_empty_or_wordless_text_raises(text):
    with pytest.raises(EmptyTextError):
        analyze_text(text)


def test_empty_file_raises(tmp_path):
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(EmptyTextError):
        analyze_file(empty)


# ---------- помилки читання файлу ----------

def test_missing_file_raises(tmp_path):
    with pytest.raises(TextReadError):
        read_text(tmp_path / "nope.txt")


def test_directory_instead_of_file_raises(tmp_path):
    with pytest.raises(TextReadError):
        read_text(tmp_path)


def test_non_utf8_file_raises(tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_bytes(b"\xff\xfe\xfa\xfb")
    with pytest.raises(TextReadError):
        read_text(bad)


def test_utf8_bom_is_ignored(tmp_path):
    file = tmp_path / "bom.txt"
    file.write_bytes("\ufeffпривіт світе".encode("utf-8"))
    assert analyze_file(file).total_words == 2


# ---------- приклади з папки data ----------

def test_sample_files_have_about_300_words():
    for name in ("sample_en.txt", "sample_uk.txt"):
        result = analyze_file(DATA_DIR / name)
        assert 270 <= result.total_words <= 330, name


def test_sample_languages_are_detected():
    assert analyze_file(DATA_DIR / "sample_en.txt").language == "en"
    assert analyze_file(DATA_DIR / "sample_uk.txt").language == "uk"


def test_empty_sample_file_raises():
    with pytest.raises(EmptyTextError):
        analyze_file(DATA_DIR / "empty.txt")


# ---------- лематизація (pymorphy3) ----------

def test_lemmatize_ukrainian_merges_word_forms():
    pytest.importorskip("pymorphy3")
    lemmas = lemmatize(["книга", "книги", "книгу"], "uk")
    assert len(set(lemmas)) == 1


def test_lemmatize_english_returns_words_unchanged():
    assert lemmatize(["running", "books"], "en") == ["running", "books"]


# ---------- консольна програма ----------

def test_cli_prints_report(tmp_path, capsys):
    file = tmp_path / "text.txt"
    file.write_text("one two two", encoding="utf-8")
    assert main([str(file)]) == 0
    output = capsys.readouterr().out
    assert "Усього слів: 3" in output
    assert "two" in output


def test_cli_finds_file_in_data_folder(capsys):
    assert main(["sample_en.txt", "--top", "3"]) == 0
    assert "Усього слів:" in capsys.readouterr().out


def test_cli_returns_error_code_for_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "nope.txt")]) == 1
    assert "Помилка" in capsys.readouterr().err
