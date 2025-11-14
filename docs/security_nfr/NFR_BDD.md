Feature: Безопасность и устойчивость Wishlist API

  Scenario: Ошибки возвращаются в едином формате без PII
    Given запущен сервис
    When вызываю GET /wishes/999999
    Then статус 404
    And тело ошибки не содержит email/PII
    And тело соответствует контракту {"error": {"code": "...", "message": "..."}}

  Scenario: Мутирующие ручки требуют JWT
    Given токен не передан
    When вызываю POST /wishes с валидным телом
    Then статус 401

  Scenario: Rate limit ограничивает запросы
    Given 100 быстрых запросов GET /wishes с одного IP
    When отправляю их в течение минуты
    Then не более 60 успешных ответов
    And часть ответов со статусом 429

  Scenario: p95 /wishes укладывается в 200мс при 20 RPS
    Given нагружаю k6 20 RPS 1 минуту
    When измеряю p95
    Then p95 ≤ 200 ms

  Scenario: CI блокирует уязвимости High/Critical
    Given в зависимостях найден High
    When запускается CI SCA
    Then задача падает со статусом failure
