# Computer Storage Inventory

Цель: получить единую локальную базу «что / где / сколько хранится» без изменения исходных файлов.

## Первый контур

По умолчанию сканируются 10 уже известных библиотечных/проектных корней из `data/computer_inventory_roots.json`.

База создаётся локально:

`G:\1\OTUS\Библиотека\_inventory\storage_inventory.sqlite`

Отчёты:

`G:\1\OTUS\Библиотека\_inventory\reports\`

Эти артефакты предназначены для локального хранения и не должны автоматически публиковаться в GitHub.

## Таблицы

- `scan_runs` — история проходов и счётчики.
- `roots` — корневые каталоги и назначение.
- `files` — полный путь, относительный путь, имя, расширение, категория, MIME, размер, времена, SHA-256.
- `scan_errors` — недоступные пути, ошибки stat/hash.

## Режимы

### Быстрый инвентарь

`RUN_COMPUTER_INVENTORY_FAST.cmd`

Собирает метаданные без чтения содержимого файлов.

### Поиск точных дублей

`RUN_COMPUTER_INVENTORY_DEDUP.cmd`

Сначала строит метаданные, затем SHA-256 вычисляется только для групп файлов одинакового размера. Это существенно дешевле полного хеширования и позволяет доказать exact duplicates.

### Весь компьютер / все fixed drives

После проверки первого прохода:

`python scripts\build_storage_inventory.py --config data\computer_inventory_roots.json --hash duplicate-candidates --all-fixed-drives`

Этот режим может обойти очень большой объём системных и проектных файлов, поэтому не является первым gate.

## Безопасность

Сканер не удаляет, не перемещает и не переименовывает исходные файлы. В отчёте явно фиксируются:

- `source_files_modified = 0`
- `source_files_deleted = 0`
- `source_files_moved = 0`

Удаление дублей — отдельный будущий этап после ручного review.

## Следующие слои

После M0 inventory:

1. exact SHA-256 duplicate groups;
2. тип документа/книги/курса/архива/модели;
3. идентификация книг (author/title/ISBN/edition/language);
4. semantic same-book variants;
5. выбор preferred copy;
6. классификация для FATHER KB;
7. перенос только после отдельного PLAN/APPLY gate.
