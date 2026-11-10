# Chaos Campaign Manager (Draconis Reach)

**Chaos Campaign Manager** — это веб-сервис и REST API для автоматизации ведения расчетов кампаний в настольной игре **Classic BattleTech** (по правилам *Hot Spots: Draconis Reach* и системе *Chaos Campaign: Mercenaries*).

Сервис полностью избавляет от необходимости вручную заполнять бумажные бланки и вести учет в электронных таблицах. Он автоматизирует отслеживание состояния боевой техники и пилотов, учет финансово-материальных ресурсов, проведение контрактов, ремонт, утилизацию и покупку мехов.

---

## 🛠 Технологический стек

### Backend
* **Python 3.11+** / **FastAPI**
* **PostgreSQL 16** (Production/Docker) + `asyncpg` / **SQLite** (`aiosqlite` в Dev/Test)
* **SQLAlchemy 2.0 (Async)** + **Alembic** (асинхронный ORM и миграции схемы БД)
* **Pydantic v2** (DTO-схемы с кастомной валидацией $BV2 \le 3000$ и лимитов)
* **OAuth2 + JWT** (`PyJWT`, `passlib[bcrypt]`)
* **uv** (высокопроизводительный менеджер пакетов Python)

### Frontend
* **React 18** + **Vite**
* **TypeScript 5.0+**
* **Zustand 4** (глобальное состояние авторизации и отрядов) + **TanStack Query v5** (серверный кэш)
* **Tailwind CSS** + **Radix UI / Shadcn UI**
* **Axios** (с авторизационным Interceptor и префиксом API `/api/v1`)

### Инфраструктура
* **Docker** & **Docker Compose** (многоконтейнерное развертывание: Database + Backend + Frontend/Nginx)

---

## 📁 Структура проекта

```text
chaos_campaign_api/
├── app/                        # Backend приложения на FastAPI
│   ├── api/v1/                 # REST API маршруты (auth, forces, pilots, contracts, tracks, logistics)
│   ├── core/                   # JWT, хеширование паролей, логирование и кастомные исключения
│   ├── db/                     # ORM-модели SQLAlchemy, подключение к СУБД и seed-данные RAT
│   │   ├── data/factions_rat.json # Динамический JSON справочник фракций и RAT
│   │   └── models/             # Модели UserModel, ForceModel, PilotModel, MechUnitModel и др.
│   ├── schemas/                # Pydantic v2 DTO модели валидации
│   ├── services/               # Бизнес-логика (калькулятор XP, переговоры, логистика, треки)
│   ├── config.py               # Конфигурация приложения (Pydantic Settings)
│   └── main.py                 # Точка входа: FastAPI app, lifespan, CORS и обработчики ошибок
├── frontend/                   # Frontend SPA приложение на React
│   ├── src/
│   │   ├── api/                # Axios-клиент c JWT interceptor и сервисы вызов API
│   │   ├── components/         # Radix / Shadcn UI компоненты (отряды, пилоты, логистика)
│   │   ├── pages/              # Страницы (Auth, Command Hub, Dashboard, Logistics, Hub)
│   │   ├── store/              # Состояние Zustand (authStore, forceStore)
│   │   └── types/              # TypeScript интерфейсы и DTO-типы
│   ├── nginx.conf              # Nginx конфигурация для Docker frontend
│   └── Dockerfile              # Сборка фронтенда в Nginx контейнере
├── alembic/                    # Скрипты и истории миграций СУБД
├── docs/                       # Паспорта проекта, архитектуры и спецификации
├── docker-compose.yml          # Многоконтейнерный запуск (PostgreSQL + FastAPI + Frontend)
├── Dockerfile                  # Dockerfile бэкенда
└── pyproject.toml              # Управление зависимостями Python (uv)
```

---

## 💻 Быстрый запуск

### Вариант 1. Запуск через Docker Compose (Рекомендуемый)

Для полного запуска всей инфраструктуры (СУБД PostgreSQL 16, бэкенд FastAPI и фронтенд Nginx) одной командой:

```bash
# Клонирование репозитория
git clone https://github.com/MileshkinMaksim/chaos_campaign_api.git
cd chaos_campaign_api

# Запуск в фоновом режиме со сборкой контейнеров
docker compose up -d --build
```

При старте контейнер FastAPI автоматически создаст необходимые таблицы в PostgreSQL через `lifespan` и загрузит справочники из `factions_rat.json`.

* **Веб-интерфейс (Frontend):** `http://localhost` (порт 80)
* **Swagger UI (Backend API):** `http://localhost:8000/docs`

Для остановки контейнеров:
```bash
docker compose down
```

---

### Вариант 2. Локальная разработка (Без Docker)

#### 1. Запуск Backend (FastAPI + SQLite/aiosqlite)

```bash
# Установка зависимостей с помощью uv
uv sync

# Применение миграций базы данных Alembic
uv run alembic upgrade head

# Запуск dev-сервера Uvicorn
uv run uvicorn app.main:app --reload
```

* **API доступен по адресу:** `http://localhost:8000`
* **Интерактивная документация:** `http://localhost:8000/docs`

#### 2. Запуск Frontend (React + Vite)

```bash
cd frontend

# Установка зависимостей Node.js
npm install

# Запуск сервера разработки Vite
npm run dev
```

* **Интерфейс доступен по адресу:** `http://localhost:5173`

---

## 📡 Основные эндпоинты REST API

| Раздел | Эндпоинт | Метод | Описание |
| --- | --- | --- | --- |
| **Auth** | `/api/v1/auth/register` | `POST` | Регистрация нового командира |
| **Auth** | `/api/v1/auth/token` | `POST` | Авторизация и получение JWT-токена |
| **Forces** | `/api/v1/forces/starting-options` | `GET` | Получение списка доступных фракций и стартовых RAT из JSON |
| **Forces** | `/api/v1/forces/me` | `GET` | Получение всех отрядов текущего пользователя |
| **Forces** | `/api/v1/forces/` | `POST` | Создание нового отряда с валидацией состава |
| **Forces** | `/api/v1/forces/{id}` | `DELETE` | Каскадное расформирование отряда со всеми пилотами и мехами |
| **Forces** | `/api/v1/forces/{id}/export` | `GET` | Экспорт листа отряда (*Record Sheet*) в формате JSON |
| **Forces** | `/api/v1/forces/{id}/assign-pilot` | `POST` | Привязка или отвязка пилота от меха |
| **Pilots** | `/api/v1/pilots/{id}/upgrade` | `POST` | Улучшение навыков (*Gunnery/Piloting*), *Edge* или *SPA* за XP |
| **Contracts** | `/api/v1/contracts/available` | `GET` | Поиск и фильтрация доступных контрактов |
| **Contracts** | `/api/v1/contracts/{id}/negotiate` | `POST` | Изменение условий контракта с учетом репутации |
| **Tracks** | `/api/v1/tracks/{id}/complete` | `POST` | Фиксация итогов боя, изменение статуса мехов, начисление SP и XP |
| **Logistics** | `/api/v1/logistics/repair` | `POST` | Ремонт поврежденной техники за SP |
| **Logistics** | `/api/v1/logistics/rat-roll` | `GET` | Генерация случайной техники по таблицам RAT выбранной фракции |
| **Logistics** | `/api/v1/logistics/buy-unit` | `POST` | Покупка выбранного меха за SP |
| **Logistics** | `/api/v1/logistics/scrap` | `POST` | Списание/утилизация техники с возвратом доли стоимости в SP |

---

## 📄 Лицензия

Проект распространяется под лицензией MIT.