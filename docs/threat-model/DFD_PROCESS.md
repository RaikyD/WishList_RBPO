# DFD: Уровень процесса - Бизнес-логика Wishlist

Диаграмма потока данных уровня процесса для операций CRUD с желаниями (wishes).

```mermaid
flowchart TD
    CLIENT[Client Application] -->|F1: HTTP Request| ROUTER[Wish Router]

    subgraph Edge[Trust Boundary: Edge]
        ROUTER -->|F2: Validate Request| VALIDATOR[Request Validator - Pydantic]
        VALIDATOR -->|F3: Validated Data| AUTH_CHECK[Auth Check - JWT]
    end

    AUTH_CHECK -->|F4: Unauthorized| ERROR_HANDLER[Error Handler]
    AUTH_CHECK -->|F5: Authorized Request| BL[Business Logic]

    subgraph Core[Trust Boundary: Core]
        BL -->|F6: Query Params| FILTER[Filter Logic]
        FILTER -->|F7: Search/Filter Criteria| REPO[Wish Repository]

        BL -->|F8: Create/Update Data| VALIDATOR_BL[Business Validator]
        VALIDATOR_BL -->|F9: Validated Business Data| REPO

        REPO -->|F10: SQL Query (ORM)| ORM[SQLAlchemy ORM]
        ORM -->|F11: Parameterized Query| DB[(Database)]

        DB -->|F12: Result Set| ORM
        ORM -->|F13: Domain Models| REPO
        REPO -->|F14: Wish Objects| BL
    end

    BL -->|F15: Response Data| SERIALIZER[Response Serializer]
    SERIALIZER -->|F16: JSON Response| CLIENT

    ERROR_HANDLER -->|F17: Error Response| CLIENT

    RATE_LIMIT[Rate Limit Check] -.->|F18: Limit Check| ROUTER

    style VALIDATOR stroke-width:2px
    style AUTH_CHECK stroke-width:2px
    style ORM stroke-width:2px
    style DB stroke-width:2px
    style REPO stroke-width:2px
    style ERROR_HANDLER stroke-width:2px
```

## Описание потоков данных

| Поток | Описание | Защита |
|-------|----------|--------|
| F1 | HTTP запрос (GET/POST/PATCH/DELETE) | HTTPS |
| F2 | Валидация структуры запроса | Pydantic схемы |
| F3 | Валидированные данные запроса | Типобезопасность |
| F4 | Ошибка аутентификации | 401 Unauthorized |
| F5 | Авторизованный запрос к бизнес-логике | JWT проверен |
| F6 | Параметры запроса (поиск, фильтры) | Санитизация параметров |
| F7 | Критерии поиска/фильтрации | Валидация типов |
| F8 | Данные для создания/обновления | Валидация бизнес-правил |
| F9 | Валидированные бизнес-данные | Проверка целостности |
| F10 | SQL запрос через ORM | Защита от SQL-инъекций |
| F11 | Параметризованный SQL запрос | ORM placeholders |
| F12 | Результат запроса из БД | Только необходимые данные |
| F13 | Преобразование в доменные модели | Инкапсуляция данных |
| F14 | Объекты Wish для бизнес-логики | Безопасные типы |
| F15 | Данные для ответа | Сериализация |
| F16 | JSON ответ клиенту | Стандартный формат |
| F17 | Ошибка в стандартном формате | RFC 7807 |
| F18 | Проверка rate limit | 429 при превышении |

## Операции бизнес-логики

### 1. Создание желания (POST /wishes)
```
F1 → F2 → F3 → F5 → F8 → F9 → F10 → F11 → F12 → F13 → F14 → F15 → F16
```

### 2. Получение списка (GET /wishes)
```
F1 → F6 → F7 → F10 → F11 → F12 → F13 → F14 → F15 → F16
```

### 3. Обновление (PATCH /wishes/{id})
```
F1 → F2 → F3 → F5 → F8 → F9 → F10 → F11 → F12 → F13 → F14 → F15 → F16
```

### 4. Удаление (DELETE /wishes/{id})
```
F1 → F5 → F10 → F11 → F12 → F16 (204 No Content)
```

## Границы доверия

- **Edge (Trust Boundary: Edge)**: Пограничный слой API
  - Валидация входных данных
  - Проверка аутентификации
  - Не доверяет клиентским данным

- **Core (Trust Boundary: Core)**: Ядро бизнес-логики
  - Бизнес-валидация
  - Работа с БД через ORM
  - Изоляция данных

## Угрозы и контрмеры

| Угроза | Поток | Контрмера | Связь с STRIDE |
|--------|-------|-----------|----------------|
| Невалидные данные | F2, F3 | Pydantic валидация | T: Tampering → R5 |
| SQL-инъекция | F10, F11 | ORM параметризованные запросы | T: Tampering → R8 |
| Неавторизованный доступ | F4, F5 | JWT проверка для мутаций | S: Spoofing → R1 |
| Эскалация привилегий | F5, F8 | Проверка ownership (будущее) | E: Elevation → R6 |
| Утечка данных через БД | F11, F12 | Принцип минимальных прав | I: Information Disclosure → R7 |
| Перегрузка API | F18 | Rate limiting | D: Denial of Service → R3 |

## Валидация данных

### Уровень 1: HTTP валидация (F2)
- Структура JSON
- Обязательные поля
- Типы данных

### Уровень 2: Бизнес-валидация (F8, F9)
- Длина строк
- Диапазоны значений
- Бизнес-правила (например, price_estimate >= 0)

### Уровень 3: БД ограничения (F11)
- Уникальность
- Внешние ключи
- Проверки целостности

## Связь с другими документами

- **STRIDE.md**: Все категории угроз (S, T, R, I, D, E)
- **RISKS.md**: Риски R1, R3, R5, R6, R7, R8
- **NFR-01**: Валидация и формат ошибок
- **NFR-02**: Аутентификация
- **NFR-03**: Rate limiting
- **DFD.md**: Общий контекст системы
- **DFD_AUTH.md**: Детализация аутентификации
- **DFD_ERRORS.md**: Детализация обработки ошибок
