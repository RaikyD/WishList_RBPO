# P10 — SAST & Secrets summary

## Semgrep

- Профиль: `p/ci` + `security/semgrep/rules.yml`

## Gitleaks

- Найдено потенциальных секретов: M
- Ложноположительные:
- Шаблон тестового токена вынесен в `security/.gitleaks.toml`.

## Как используем результаты
- Semgrep и Gitleaks добавлены как часть Security-практик в CI.
- Отчёты `semgrep.sarif` и `gitleaks.json` будут использоваться в DS/итоговом отчёте как доказательства SAST и сканирования секретов.
- Новые findings:
  - для блокирующих проблем создаём Issue/PR сразу;
  - для некритичных — регистрируем задачу в backlog с ссылкой на конкретный отчёт/commit.
