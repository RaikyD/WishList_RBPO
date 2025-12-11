# P12 — IaC & Container Security Summary

В этом файле собраны результаты сканирования Dockerfile, инфраструктуры (IaC) и зависимостей
Wishlist API в рамках задания P12.

## 1. Используемые инструменты

- **Hadolint** — линтер Dockerfile.
  - Конфигурация: `security/hadolint.yaml`.
  - Запускается в CI как отдельный шаг.
- **Checkov** — анализ IaC и CI-конфигурации.
  - Конфигурация: `security/checkov.yaml`.
  - Сканирует:
    - `Dockerfile`;
    - GitHub Actions workflow’ы (`.github/workflows/**`).
- **Trivy** — анализ зависимостей и контейнерного окружения.
  - Запуск в режиме `fs` по репозиторию (`/work`).
  - Основной фокус — Python-зависимости (`requirements.txt`).

Все три инструмента интегрированы в отдельный workflow:
`.github/workflows/ci-p12-iac-container.yml`, результаты сохраняются в `EVIDENCE/P12/`.

---

## 2. Результаты сканирования

### 2.1. Hadolint (Dockerfile)

- Отчёт: `EVIDENCE/P12/hadolint_report.json`.
- Формат: JSON.
- Содержимое: пустой список `[]`.

Это означает, что Hadolint не нашёл ни одной проблемы в Dockerfile:
- не используется `latest`-тег без необходимости;
- не тянутся лишние слои;
- команды и структура Dockerfile соответствуют best practices.

---

### 2.2. Checkov (IaC / CI)

- Отчёт: `EVIDENCE/P12/checkov_report.json`.
- Формат: JSON, содержит два отчёта:
  - Отчёт 0:
    - `passed = 87`
    - `failed = 0`
    - `resource_count = 1`
  - Отчёт 1:
    - `passed = 272`
    - `failed = 0`
    - `resource_count = 0`

Сканировались:
- Dockerfile (как часть контейнерной инфраструктуры);
- GitHub Actions workflows (как часть IaC для CI/CD пайплайна).

**Ошибок и нарушений политик Checkov не обнаружено**:
- все проверки прошли успешно;
- парсинг отработал без ошибок (`parsing_errors = 0`).

---

### 2.3. Trivy (зависимости и окружение)

- Отчёт: `EVIDENCE/P12/trivy_report.json`.
- Формат: JSON.
- Trivy запускался в режиме `fs` по каталогу репозитория `/work`.

Основные результаты:
- Тип артефакта: `repository`, `ArtifactName = "/work"`.
- Обнаружен один результат по зависимостям Python (`Type = "pip"`, `Class = "lang-pkgs"`, `Target = "requirements.txt"`).
- Проанализировано 6 пакетов:
  - `PyJWT`
  - `fastapi`
  - `pydantic`
  - `pydantic-core`
  - `sqlalchemy`
  - `uvicorn`
- Для каждого пакета:
  - `Vulnerabilities = []` (список уязвимостей пуст).

---

## 3. Харднинг контейнера и docker-compose

В дополнение к статическому анализу, в `docker-compose.yml` для сервиса `api` настроен
базовый hardening контейнера:

- `read_only: true` — файловая система контейнера доступна только для чтения.
- `tmpfs: /tmp` — временный каталог вынесен в tmpfs.
- `security_opt: ["no-new-privileges:true"]` — запрещено получение новых привилегий внутри контейнера.
- `cap_drop: ["ALL"]` — все Linux capabilities сброшены.
- Данные вынесены во внешний volume `wishlist-data:/data`.

Эти настройки снижают возможный ущерб при компрометации приложения:
- даже при эксплуатации уязвимости у атакующего не будет прав на модификацию файлов внутри контейнера;
- невозможно «поднять» привилегии через setuid/binary;
- к минимуму ограничен доступ к потенциально опасным системным вызовам.

---

## 4. Краткое соответствие критериям P12

- **C1 — Dockerfile / container scan (Hadolint)**  
  - Настроен запуск Hadolint в CI.  
  - Dockerfile собственного сервиса проверяется, отчёт `hadolint_report.json` сохранён.  
  - Нарушений не найдено.

- **C2 — IaC scan (Checkov)**  
  - Checkov анализирует Dockerfile и GitHub Actions workflows.  
  - Все проверки прошли успешно (`failed = 0`).  
  - Отчёт `checkov_report.json` сохранён в `EVIDENCE/P12/`.

- **C3 — Vulnerability scan (Trivy)**  
  - Trivy сканирует репозиторий и Python-зависимости.  
  - Уязвимости в зависимостях на момент проверки не обнаружены.  
  - Отчёт `trivy_report.json` приложен.

- **C4 — Hardening контейнера и окружения**  
  - Реализован hardening через настройки в `docker-compose.yml`: `read_only`, `tmpfs`, `no-new-privileges`, `cap_drop: ALL`, выделенный volume.

- **C5 — Интеграция в CI / evidence**  
  - Все сканеры интегрированы в отдельный workflow `ci-p12-iac-container.yml`.  
  - Артефакты сканирования автоматически загружаются в GitHub Actions и сохраняются в `EVIDENCE/P12/`.

