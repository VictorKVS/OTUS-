# Локальная библиотека архитектора — intake pipeline

Источник по умолчанию:

```text
G:\1\OTUS\Библиотека
```

Исходные книги не требуются в GitHub. Сканирование и последующая обработка выполняются локально.

## Запуск

Из корня `G:\1\OTUS`:

```bat
RUN_LIBRARY_PIPELINE.cmd
```

Или по этапам:

```powershell
python tools\library_scan.py "G:\1\OTUS\Библиотека"
python tools\book_extract.py
python tools\book_prepare_translation.py
```

## Этап 1 — inventory

`tools/library_scan.py` рекурсивно обходит библиотеку и для поддерживаемых форматов сохраняет:

- относительный путь;
- имя файла и нормализованный заголовок;
- формат;
- размер;
- время изменения;
- SHA-256;
- количество страниц PDF, если установлен `pypdf`;
- duplicate group size по SHA-256;
- простой architecture relevance score.

Результаты:

```text
knowledge\library_inventory\generated\library_inventory.json
knowledge\library_inventory\generated\library_inventory.csv
knowledge\library_inventory\generated\library_inventory.md
```

Сканер выбирает первый архитектурный pilot-кандидат среди уникальных SHA-256 и создаёт приватный workspace:

```text
G:\1\OTUS\_PRIVATE_BOOK_CORPUS\BOOK-...\source_manifest.json
```

## Этап 2 — extraction

`tools/book_extract.py` сверяет SHA-256 исходника и извлекает текст.

Поддержка MVP:

- PDF — `pypdf`, fallback `PyMuPDF`;
- DOCX — `python-docx`;
- EPUB — стандартный ZIP/HTML parser;
- TXT/MD/RTF — текстовое чтение.

Результаты остаются только в `_PRIVATE_BOOK_CORPUS`:

```text
extracted_text.txt
pages.jsonl
extraction_manifest.json
```

Каждая страница получает `char_start`, `char_end`, `text_sha256`.

Если PDF фактически скан и машиночитаемого текста недостаточно, pipeline ставит `NEEDS_OCR` и прекращает дальнейший анализ.

## Этап 3 — translation units

`tools/book_prepare_translation.py` делит извлечённый текст на абзацные единицы и сохраняет:

```text
translation_units.jsonl
translation_manifest.json
```

Каждая единица содержит:

- stable `unit_id`;
- исходный диапазон символов;
- начальную/конечную страницу;
- исходный текст;
- SHA-256 исходного текста;
- `translated_text: null`;
- статус перевода и проверки.

То есть дальнейший перевод не сможет потерять связь с оригиналом.

## Следующий слой

После заполнения `translated_text` каждая единица поступает в Knowledge Analyst:

```text
Book
  → Part / Chapter / Section
  → Paragraph / List / Figure / Table / Example
  → TERM / CONCEPT / DEFINITION
  → CLAIM / PRINCIPLE / PATTERN
  → TRADEOFF / DECISION_CRITERION / FAILURE_MODE
  → RELATION
  → professor cross-source review
  → reviewed Knowledge Base
```

Полный текст книги и полный перевод остаются приватным evidence corpus. В публичный knowledge graph должны попадать производные знания, метаданные, хэши и ссылки на `source_span_id`, а не реконструируемая копия книги.
