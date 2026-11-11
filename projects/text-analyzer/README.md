# Аналізатор тексту (укр. / англ.)

Консольна програма на Python: читає текст із файлу, визначає мову, рахує слова
і будує словник частотності. Обробляє порожній текст та помилки читання файлу.

Бібліотеки: **NLTK** (токенізація, `FreqDist`) і **pymorphy3** (лематизація української).

## Запуск

```powershell
uv run python src/main.py data/sample_uk.txt
uv run python src/main.py sample_en.txt --top 15
uv run python src/main.py sample_uk.txt --lemmas
uv run python src/main.py data/empty.txt
```

## Тести

```powershell
uv run pytest -v
```
