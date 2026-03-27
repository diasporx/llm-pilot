# LLM Pilot — Генерация саммари задач из Яндекс Трекера

Инструмент для выгрузки задач из Яндекс Трекера и генерации саммари через LLM.
Саммари используется как мини-ТЗ для ревью кода — помогает быстро погрузиться в контекст задачи.

---

## Структура проекта

```
llm-pilot/
├── src/
│   ├── client.py       — HTTP-клиент к Yandex Tracker API
│   └── serializer.py   — нормализует ответ API в чистый JSON
├── prompts/
│   └── sprint-summary-prompt.md  — инструкция для LLM (Claude)
├── data/               — сырые JSON-файлы задач (результат выгрузки)
│   └── sprint-31/
│       └── DEV-18281.json
├── results/            — готовые саммари в Markdown
│   └── sprint-31/
│       └── DEV-18281.md
├── config.py           — токен и настройки подключения
├── main.py             — CLI
└── requirements.txt
```

---

## Установка

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

---

## Настройка

### 1. Получить OAuth-токен Яндекса

1. Создай приложение на [oauth.yandex.ru](https://oauth.yandex.ru):
   - Платформа: **Веб-сервисы**, Callback URI: `https://oauth.yandex.ru/verification_code`
   - Доступы: `Яндекс Трекер → tracker:read, tracker:write` и `Чтение данных об организации`
2. Открой в браузере (подставь свой ClientID):
   ```
   https://oauth.yandex.ru/authorize?response_type=token&client_id=ВАШ_CLIENT_ID
   ```
3. После авторизации скопируй `access_token` из URL

### 2. Найти ORG_ID

Запусти после настройки токена:
```bash
.venv/bin/python main.py whoami
```
Программа автоматически выведет список организаций с их ID.

Если не получилось — открой [admin.yandex.ru](https://admin.yandex.ru), в URL будет:
```
https://admin.yandex.ru/company/XXXXXXX/...
```
`XXXXXXX` — это и есть `ORG_ID`.

### 3. Заполнить config.py

```python
TRACKER_TOKEN = "y0_your_token_here"
ORG_ID        = "12345678"
ORG_TYPE      = "yandex360"   # или "cloud" для Яндекс Cloud организаций
BASE_URL      = "https://api.tracker.yandex.net/v2"
```

---

## Использование

### Проверить подключение
```bash
.venv/bin/python main.py whoami
```

### Выгрузить все задачи спринта
```bash
.venv/bin/python main.py sprint --sprint "Спринт 31 ПП" --queue DEV
```
Сохранит все задачи в `data/sprint-31/`.

### Выгрузить одну задачу
```bash
# Если у задачи указан спринт в Трекере — спринт определится автоматически
.venv/bin/python main.py issue DEV-18281

# Если спринт в задаче не указан — задай вручную
.venv/bin/python main.py issue DEV-18281 --sprint 31
```

---

## Генерация саммари через LLM

После выгрузки задач напиши в чат Claude Code:

```
Напиши саммари по 31 спринту
```

Claude прочитает файлы из `data/sprint-31/`, сформирует саммари для каждой задачи
и сохранит результаты в `results/sprint-31/DEV-XXXXX.md`.

Каждый файл саммари содержит:
- **Описание** — контекст задачи и цель
- **Договорённости и комментарии** — ключевые решения из обсуждений
- **Для разработчика** — технический контекст для ревью кода
- **Для тестировщика** — что и как проверять

Инструкция для LLM находится в `prompts/sprint-summary-prompt.md`.

---

## Токен просрочен?

OAuth-токены Яндекса имеют ограниченный срок жизни. Если видишь ошибку `expired_token` —
получи новый токен по той же ссылке и обнови `TRACKER_TOKEN` в `config.py`.
# llm-pilot
