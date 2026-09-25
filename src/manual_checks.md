# Ручная проверка Request Router

Команды выполнялись из корня проекта.

| Сценарий | Команда | Ожидаемый результат | Фактический результат | Код завершения | Статус |
|---|---|---|---|---:|---|
| Корректный JSON | `python src/main.py --input datasets/requests.json --output src/result.json` | `src/result.json` создан; результаты совпадают с `datasets/expected-results.json` по `id`; код `0` | `src/result.json` создан. Получено 6 записей: `r-001`–`r-006`. Значения `category` и `priority` совпали с `datasets/expected-results.json` по `id`. | `0` | PASS |
| Корректный CSV | `python src/main.py --input datasets/requests.csv --output src/result.json` | `src/result.json` создан; результаты совпадают с `datasets/expected-results.json` по `id`; код `0` | `src/result.json` создан. Получено 4 записи: `c-001`–`c-004`. Значения `category` и `priority` совпали с `datasets/expected-results.json` по `id`. | `0` | PASS |
| Несуществующий файл | `python src/main.py --input datasets/file-does-not-exist.json --output src/result.json` | Сообщение `Ошибка: входной файл не найден`; traceback отсутствует; ненулевой код | Выведено сообщение `Ошибка: входной файл не найден`. Traceback отсутствует. | `1` | PASS |
| Поврежденный JSON | `python src/main.py --input datasets/broken.json --output src/result.json` | Сообщение `Ошибка: поврежденный JSON`; traceback отсутствует; ненулевой код | Выведено сообщение `Ошибка: поврежденный JSON`. Traceback отсутствует. | `1` | PASS |
| Запись без обязательного поля | `python src/main.py --input datasets/missing-field.json --output src/result.json` | Сообщение о том, что `id` или `text` отсутствует либо пуст; traceback отсутствует; ненулевой код | Выведено сообщение `Ошибка: в записи отсутствует или пустое поле id или text`. Traceback отсутствует. | `1` | PASS |

## Итог

Все пять обязательных сценариев завершились с ожидаемым результатом.

После проверки CSV выполнен повторный запуск с `datasets/requests.json`, поэтому финальный `src/result.json` содержит результаты для JSON-набора: записи `r-001`–`r-006`.