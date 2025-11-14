# SecDev Course Template
## Локальный запуск (one-liner)

```bash
mkdir -p EVIDENCE/S06 && export PYTHONPATH="$(pwd)" && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt && python -m pytest -q --junitxml=EVIDENCE/S06/test-report.xml
```

Отчёт тестов будет в `EVIDENCE/S06/test-report.xml`.

## Конфиги / переменные окружения

Приложение читает конфигурацию из переменных окружения:

- `JWT_SECRET` — секрет для JWT (обязательно переопределить в проде)
- `ENV` — окружение (`dev`|`prod`), по умолчанию `dev`
- `DATABASE_URL` — строка подключения к БД (по умолчанию `sqlite:///./wishlist.db`)
- `RATE_LIMIT_PER_MINUTE` — лимит запросов в минуту для GET (по умолчанию `60`)

В прод-окружении приложение не стартует, если `JWT_SECRET=dev` (guard безопасности).

Стартовый шаблон для студенческого репозитория (HSE SecDev 2025).

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
uvicorn app.main:app --reload
```

## Ритуал перед PR
```bash
ruff --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

## Тесты
```bash
pytest -q
```

## CI
В репозитории настроен workflow **CI** (GitHub Actions) — required check для `main`.
Badge добавится автоматически после загрузки шаблона в GitHub.

## Контейнеры
```bash
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```

## Эндпойнты
- `GET /health` → `{"status": "ok"}`
- `POST /items?name=...` — демо-сущность
- `GET /items/{id}`

## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.
