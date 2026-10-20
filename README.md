# ⚔️ Chaos Campaign Manager (Draconis Reach)

**Chaos Campaign Manager** — это веб-сервис и REST API для автоматизации ведения наемнических отрядов в настольной стратегической игре **BattleTech Classic** (по правилам *Hot Spots: Draconis Reach* и системе *Chaos Campaign: Mercenaries*).

Сервис берет на себя всю рутину командира: отслеживание состояния боевой техники и пилотов, учет финансово-материальных ресурсов, проведение контрактов, ремонт и утилизацию лома.

---

## 🚀 Основные возможности

* **Архитектура Command Hub (Multi-Force):** Возможность владеть и одновременно управлять несколькими наемническими отрядами в одном аккаунте ($1 \rightarrow N$).


* **Единая экономика Support Points (SP):** Унифицированная финансовая система — покупка и ремонт мехов, вступительные взносы за миссии, оплата контрактов и конвертация в XP рассчитываются строго в SP.


* **Прокачка и управление пилотами:** Нелинейный расчет стоимости улучшения навыков (Gunnery/Piloting), Edge и специальных способностей (SPA).


* **Контракты и переговоры:** Генерация контрактов с учетом репутации отряда, гибкие условия выплат и командных прав.


* **Проведение миссий (Tracks):** Ввод итогов боя, отслеживание потерь/повреждений, распределение XP и наград, а также скрап уничтоженных мехов (возврат 25% стоимости в SP).


* **Логистика и RAT:** Генерация случайного состава техники по таблицам назначения (*Random Assignment Tables — RAT*) выбранной фракции и ремонтный док.


* **Экспорт документов:** Скачивание официальных листов отряда (*Mercenary Force Record Sheet*) в формате JSON.



---

## 🛠 Технологический стек

### Backend

* **Python 3.11+** / **FastAPI**

* **SQLAlchemy 2.0 (Async)** + `asyncpg` / `aiosqlite`

* **Pydantic v2** (DTO с валидацией стартового состава и BV2)


* **Alembic** (управление миграциями БД)


* **OAuth2 + JWT** (аутентификация пользователей)


* **uv** (высокопроизводительный менеджер пакетов Python)



### Frontend

* **React 18** + **Vite**

* **TypeScript 5.0+**

* **TanStack Query v5 (React Query)** + **Zustand 4**

* **Tailwind CSS** + **Radix UI / Shadcn UI**

* **Axios** (с JWT Interceptor)



---

## 📁 Структура проекта

```text
chaos_campaign_api/
├── app/                      # FastAPI Backend приложение[cite: 3, 5]
│   ├── api/v1/               # REST API роутеры (auth, forces, pilots, contracts, tracks, logistics)[cite: 1, 3]
│   ├── core/                 # Безопасность, исключения и логирование[cite: 1, 3]
│   ├── db/                   # Модели SQLAlchemy, сессии и JSON-справочники RAT[cite: 1, 3]
│   ├── schemas/              # Pydantic v2 DTO модели[cite: 1, 3]
│   └── services/             # Бизнес-логика правил BattleTech[cite: 1, 3]
├── frontend/                 # React + TypeScript SPA приложение[cite: 2, 5]
├── alembic/                  # Миграции структуры базы данных[cite: 1, 3]
├── docs/                     # Технические спецификации[cite: 5]
└── pyproject.toml            # Конфигурация проекта и зависимостей[cite: 1, 3, 5]

```

---

## 💻 Быстрый запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/MileshkinMaksim/chaos_campaign_api.git
cd chaos_campaign_api

```

### 2. Запуск Backend (FastAPI)

Проект использует менеджер пакетов `uv`:

```bash
# Установка зависимостей
uv sync

# Применение миграций базы данных
uv run alembic upgrade head

# Запуск веб-сервера разработки
uv run uvicorn app.main:app --reload

```

* **API доступен по адресу:** `http://localhost:8000`
* **Swagger UI документация:** `http://localhost:8000/docs`

### 3. Запуск Frontend (React)

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера Vite
npm run dev

```

* **Интерфейс доступен по адресу:** `http://localhost:5173`

---

## 📡 Основные эндпоинты REST API

| Раздел | Эндпоинт | Метод | Описание |
| --- | --- | --- | --- |
| **Auth** | `/api/v1/auth/register` | `POST` | Регистрация нового командира

 |
| **Auth** | `/api/v1/auth/token` | `POST` | Авторизация и получение JWT-токена

 |
| **Forces** | `/api/v1/forces/me` | `GET` | Получение списка всех отрядов пользователя

 |
| **Forces** | `/api/v1/forces/` | `POST` | Создание нового отряда наемников

 |
| **Forces** | `/api/v1/forces/{id}` | `DELETE` | Каскадное удаление (расформирование) отряда

 |
| **Pilots** | `/api/v1/pilots/{id}/upgrade` | `POST` | Прокачка навыков и очков пилота за XP

 |
| **Contracts** | `/api/v1/contracts/available` | `GET` | Поиск доступных контрактов

 |
| **Tracks** | `/api/v1/tracks/{id}/complete` | `POST` | Завершение миссии, расчет наград и конвертация SP $\rightarrow$ XP

 |
| **Logistics** | `/api/v1/logistics/repair` | `POST` | Ремонт поврежденной техники за SP

 |

---

## 📄 Лицензия

Проект распространяется под лицензией MIT.