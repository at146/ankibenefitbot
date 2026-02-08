# ankibenefitbot

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Telegram-бот для бренда ANKI, предназначенный для генерации лидов и сбора аналитики через опросы пользователей.

## Описание

Бот представляет собой маркетинговый инструмент, который:
- Предоставляет пользователям доступ к статье о росте продаж бизнеса
- Проводит детальные опросы пользователей (до 19 вопросов + финальный вопрос)
- Отслеживает взаимодействие пользователей (переходы по статьям, подписки на каналы)
- Автоматически синхронизирует данные с Google Sheets для аналитики
- Управляет лид-магнитами и подписчиками каналов


## Технологический стек

- **Python** 3.12+
- **aiogram** 3.19+ — фреймворк для Telegram ботов
- **aiogram-dialog** 2.3+ — управление диалогами
- **SQLAlchemy** 2.0+ — ORM с поддержкой async PostgreSQL
- **PostgreSQL** — основная база данных
- **Redis** — хранилище состояний FSM (опционально)
- **gspread** 6.2+ — интеграция с Google Sheets API
- **APScheduler** 3.11+ — планировщик задач
- **Alembic** — миграции базы данных
- **uv** — менеджер пакетов
- **Docker** — контейнеризация

## Структура проекта

```
ankibenefitbot/
├── bot/                    # Основной код бота
│   ├── api/               # Интеграции с внешними API
│   │   └── google_sheets/ # Работа с Google Sheets
│   ├── core/              # Конфигурация и настройки
│   ├── crud/              # CRUD операции с БД
│   ├── db/                # Модели базы данных
│   ├── dialogs/           # Диалоги бота (aiogram-dialog)
│   │   └── menu/          # Меню и опросы
│   ├── handlers/          # Обработчики событий
│   ├── middlewares/       # Middleware
│   └── utils/             # Утилиты
├── migrations/            # Миграции Alembic
├── scripts/               # Вспомогательные скрипты
├── Dockerfile             # Образ для production
├── docker-compose.yml     # Конфигурация Docker Compose
└── pyproject.toml         # Конфигурация проекта и зависимости
```

## Модели базы данных

- **User** — основная информация о пользователях
- **AnswerQuestions** — результаты опросов пользователей
- **UserChannel** — пользователи, подписавшиеся на канал
- **UserLidMagnit** — пользователи лид-магнита

## Установка и запуск

### Требования

- Python 3.12+
- PostgreSQL
- Redis (опционально, для production)
- Google Sheets API credentials
- Telegram Bot Token

### Настройка окружения

1. Склонируйте репозиторий:
```bash
git clone <repository-url>
cd ankibenefitbot
```

2. Установите зависимости через `uv`:
```bash
uv sync
```

3. Создайте файл `.env` на основе примера и заполните необходимые переменные:
```env
BOT_TOKEN=your_telegram_bot_token
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USERNAME=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ankibenefitbot
GOOGLE_SHEET_TABLE_ID=your_google_sheet_id
GOOGLE_PATH_CREDITS=path/to/credentials.json
GOOGLE_SHEET_MINUTE_CHECK_TABLE=5
# ... и другие переменные
```

4. Примените миграции базы данных:
```bash
alembic upgrade head
```

### Запуск в режиме разработки

```bash
docker compose -f docker-compose-dev.yml up
```

### Запуск в production

```bash
docker compose up -d
```

## Режимы работы

Бот поддерживает два режима работы:

1. **Webhook** (production) — получает обновления через webhook
2. **Polling** (development) — опрашивает Telegram API

Режим выбирается через переменную окружения `USE_WEBHOOK`.

## Разработка

### Создание миграций

```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```

### Линтинг и форматирование

```bash
make lint
```

Или вручную:
```bash
mypy .
ruff check .
ruff format .
```

### Pre-commit hooks

Проект использует pre-commit для автоматической проверки кода:
```bash
pre-commit install
```

## Конфигурация

Основные настройки находятся в `.env` файле и обрабатываются через `bot/core/config.py`:

- Настройки Telegram (токен, webhook)
- Параметры базы данных (PostgreSQL)
- Настройки Redis
- Конфигурация Google Sheets
- Список администраторов бота

## Особенности

- Асинхронная архитектура для высокой производительности
- Поддержка webhook и polling режимов
- Автоматическая синхронизация с Google Sheets
- Гибкая система диалогов через aiogram-dialog
- Типизация с помощью mypy
- Строгие правила линтинга через ruff

## Автор

Alex Tarasov
