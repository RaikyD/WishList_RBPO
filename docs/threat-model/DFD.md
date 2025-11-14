# DFD: Общий контекст системы

Высокоуровневая диаграмма потока данных для Wishlist API (контекстный уровень).

```mermaid
flowchart LR
  U[User / Browser / Mobile App] -->|F1: HTTPS| GW[API Gateway Router]

  subgraph Edge[Trust Boundary: Edge]
    GW -->|F2: Middleware | SVC[WishList application]
  end

  subgraph Core[Trust Boundary: Core]
    SVC -->|F3: Business Logic / Repository| DB[(Database: SQLite or Postgres)]
  end

  SVC -->|F4: JSON Response / Error Envelope| U

  style GW stroke-width:2px
  style SVC stroke-width:2px
  style DB stroke-width:2px
```

## Дополнительные DFD диаграммы

Для детального анализа безопасности созданы дополнительные диаграммы уровня процесса:

1. **DFD_AUTH.md** - Детализация процесса аутентификации и авторизации
2. **DFD_ERRORS.md** - Детализация обработки ошибок и логирования
3. **DFD_PROCESS.md** - Детализация бизнес-логики и CRUD операций

Все диаграммы содержат границы доверия (Trust Boundaries) и привязаны к угрозам STRIDE.
