FROM python:3.12-slim

# Установка менеджера пакетов uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock* ./

# Синхронизация ТОЛЬКО зависимостей (без сборки корневого пакета)
RUN uv sync --frozen --no-install-project || uv sync --no-install-project

# Копирование исходного кода приложения
COPY app/ ./app

EXPOSE 8000

# Запуск FastAPI через uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]