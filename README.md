# Система управления заказами и расчетами строительной компании («ДОМОСТРОЙ»)

Микросервисная система для автоматизации приема заказов, расчета смет на строительные работы, сохранения данных и отправки уведомлений. Проект разработан в рамках финальной работы по дисциплине «Информационные системы и программирование».

## Архитектура

~~~text
               ┌──────────────────────┐
  Клиент ────► │     API Gateway      │ :8080
  (cURL/UI)    │ (Маршрутизатор /     │
               │   Координатор)       │
               └────┬────────────┬────┘
                    │            │
             /api/v1/orders   /api/v1/notify
                    ▼            ▼
               ┌─────────┐  ┌──────────────────────┐
               │ Orders  │  │ Notifications        │
               │ Service │  │ Service              │
               │  :8002  │  │ :8003                │
               └───┬─────┘  └──────────────────────┘
                   │
                   ▼
            ┌──────────────┐
            │  PostgreSQL  │
            │    :5432     │
            │ (volume data)│
            └──────────────┘
~~~

### Компоненты системы
| Компонент | Порт | Назначение |
| :--- | :--- | :--- |
| **API Gateway** | `8080` | Единая точка входа, маршрутизация и оркестрация запросов |
| **Orders Service** | `8002` | Управление строительными заказами, расчет стоимости и работа с БД |
| **Notifications Service** | `8003` | Обработка и логирование уведомлений клиентам |
| **PostgreSQL** | `5432` | Реляционная база данных для хранения заказов (`db_data`) |

## Технологии
- **Язык:** Python 3.11
- **Фреймворк:** FastAPI + Uvicorn
- **База данных:** PostgreSQL 16 (драйвер `psycopg2-binary`)
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions (`.github/workflows/ci.yml`)

## Структура репозитория
~~~text
domostroy-microservices/
├── .github/workflows/       # CI пайплайн проверки кода
├── api-gateway/             # Шлюз (порт 8080)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── orders-service/          # Сервис заказов (порт 8002)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── notifications-service/   # Сервис уведомлений (порт 8003)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── docs/                    # Документация и архитектура C4
│   └── architecture_c4.md
├── .gitignore
├── docker-compose.yml
└── README.md
~~~

## Быстрый старт
~~~bash
cd domostroy-microservices
docker compose up --build -d
docker compose ps
~~~

## Сценарий проверки (cURL)

1. Создать строительный заказ:
~~~bash
curl -X 'POST' \
  'http://localhost:8080/api/v1/process-order' \
  -H 'Content-Type: application/json' \
  -d '{
  "client_name": "Антон Хламов",
  "service_type": "Строительство монолитного фундамента",
  "total_price": 250000.0,
  "email": "hlamov@domostroy.ru"
}'
~~~

2. Получить список всех заказов:
~~~bash
curl -X 'GET' 'http://localhost:8080/api/v1/orders'
~~~

## Архитектура C4
Подробное описание по уровням C4 (Context, Container, Component) находится в файле [docs/architecture_c4.md](docs/architecture_c4.md).

## Остановка проекта
~~~bash
docker compose down        # Остановить контейнеры
docker compose down -v     # Остановить и удалить данные БД (volume)
~~~
