# ankibenefitbot

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## library

aiogram
aiogram-dialog
sqlalchemy
apscheduler
gspread
redis

## Dev

alembic revision --autogenerate -m "init"

alembic upgrade head

```bash
docker compose -f docker-compose-dev.yml up
```
