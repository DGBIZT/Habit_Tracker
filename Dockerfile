FROM python:3.13.2-slim

WORKDIR /app

# 1. Устанавливаем только необходимые системные зависимости (без компиляторов)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Проверяем наличие файлов
RUN if [ ! -f pyproject.toml ]; then echo "ERROR: pyproject.toml not found!" && exit 1; fi
RUN if [ ! -f poetry.lock ]; then echo "ERROR: poetry.lock not found!" && exit 1; fi

# 3. Устанавливаем Poetry безопасно (с проверкой версии)
ENV POETRY_VERSION=1.8.3
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# 4. Настраиваем Poetry и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# 5. Копируем код приложения (после установки зависимостей)
COPY . .

# 6. Создаём директории для статики и медиа
RUN mkdir -p /app/staticfiles /app/media

# 7. Экспонируем порт
EXPOSE 8000

# 8. Переменные окружения (переопределяются при запуске)
ENV SECRET_KEY=""  # Оставляем пустым — задаётся через .env или docker run
ENV CELERY_BROKER_URL="redis://redis:6379/1"
ENV CELERY_RESULT_BACKEND="redis://redis:6379/1"

# 9. Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
