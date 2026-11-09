"""Модуль для обчислення Word Error Rate (WER).

    WER = (S + D + I) / N

S - кількість замін (substitutions)
D - кількість видалень (deletions)
I - кількість вставок (insertions)
N - кількість слів в еталонному тексті (reference)

Опис: https://en.wikipedia.org/wiki/Word_error_rate
"""

import re
from dataclasses import asdict, dataclass


@dataclass
class WERResult:
    wer: float
    S: int
    D: int
    I: int
    N: int

    def to_dict(self) -> dict:
        return asdict(self)


def tokenize(text: str) -> list[str]:
    """Розбиває текст на слова: нижній регістр, без розділових знаків."""
    return re.findall(r"\w+(?:['’ʼ-]\w+)*", text.lower())


def word_error_rate(reference: str, hypothesis: str) -> WERResult:
    """Обчислює WER та його складові (S, D, I, N).

    reference  - еталонний текст
    hypothesis - текст, який порівнюємо з еталоном
    """
    ref = tokenize(reference)
    hyp = tokenize(hypothesis)
    n, m = len(ref), len(hyp)

    if n == 0:
        raise ValueError("Еталонний текст не містить жодного слова (N = 0).")

    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][0] = i  
    for j in range(1, m + 1):
        d[0][j] = j  

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j - 1] + cost,  
                d[i - 1][j] + 1,         
                d[i][j - 1] + 1,         
            )

    s = dele = ins = 0
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]):
            if ref[i - 1] != hyp[j - 1]:
                s += 1
            i -= 1
            j -= 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            dele += 1
            i -= 1
        else:
            ins += 1
            j -= 1

    wer = (s + dele + ins) / n
    return WERResult(wer=wer, S=s, D=dele, I=ins, N=n)