FROM python:3.13.2

WORKDIR /app

# Системные зависимости
#RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev python3-dev build-essential\
#    gcc \
#    libpq-dev \
#    python3-dev \
#    build-essential \
#    curl\
#    -o Acquire::http::Timeout=1200 \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/* \
#    curl

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Проверка файлов
#RUN if [ ! -f pyproject.toml ]; then echo "pyproject.toml not found!" && exit 1; fi
#RUN if [ ! -f poetry.lock ]; then echo "poetry.lock not found!" && exit 1; fi

# Установка зависимостей через Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root && \
    pip install celery[redis]==5.4.0


# Копируем код
COPY . .

# Директории для статики и медиа
RUN mkdir -p /app/staticfiles /app/media

# Переменные окружения (можно переопределить в .env)
#ENV SECRET_KEY="django-insecure-@s*q5imnj_d)vx%dfsb1%b3yyerkt#e$#p-$x@di1h8*smu2p="
#ENV CELERY_BROKER_URL="redis://redis:6379/1"
#ENV CELERY_RESULT_BACKEND="redis://redis:6379/1"


EXPOSE 8000

# Команда по умолчанию
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
