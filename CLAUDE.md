# LLM Pilot — инструкции для Claude Code

## Рабочая директория

Проект находится в `/home/dev/projects/llm-pilot/`.
Python-окружение: `.venv/bin/python`. Всегда используй его, не системный `python3`.

---

## Генерация саммари

При любом запросе, связанном с саммари задач или спринта, следуй инструкции из `prompts/sprint-summary-prompt.md`.

Промпт описывает два режима:
- **Одна задача** — пользователь называет ключ (`DEV-XXXXX`)
- **Весь спринт** — пользователь называет номер спринта

Если нужного JSON-файла нет в `data/` — выгрузи его через CLI перед генерацией саммари.

---

## Структура проекта

```
data/sprint-[N]/       — JSON-файлы задач (выгружаются из Трекера)
results/sprint-[N]/    — готовые саммари в Markdown
prompts/               — промпты для LLM
src/client.py          — HTTP-клиент к Yandex Tracker API
config.py              — TRACKER_TOKEN, ORG_ID, настройки
main.py                — CLI: whoami / sprint / issue
```

## Полезные команды

```bash
# Проверить токен
.venv/bin/python main.py whoami

# Выгрузить одну задачу
.venv/bin/python main.py issue DEV-18161

# Выгрузить одну задачу с явным указанием спринта
.venv/bin/python main.py issue DEV-18161 --sprint 31

# Выгрузить весь спринт
.venv/bin/python main.py sprint --sprint "Спринт 31 ПП" --queue DEV
```
