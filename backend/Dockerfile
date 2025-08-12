# СОБОР ЗАВИСИМОСТЕЙ
# выбираем базовый образ
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# создаём рабочую директорию
WORKDIR /app/backend

# устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# копируем файл зависимостей
COPY backend/requirements.txt ./requirements.txt

# устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# СОБОР STARIC
# выбираем базовый образ
FROM builder AS get_static

# создаём рабочую директорию
WORKDIR /app/backend

# копируем зависимости
COPY --from=builder /usr/local /usr/local

# копируем backend и frontend
COPY backend /app/backend
COPY frontend /app/frontend

# собираем статику
RUN python manage.py collectstatic --noinput

# СБОР ФИНАЛЬНОГО ОБРАЗА STATIC
# выбираем используемый базовый образ
FROM alpine:3.18 AS static

# создаём рабочую директорию
WORKDIR /app/static

# копируем static
COPY --from=get_static /app/static /app/static

# СБОР ФИНАЛЬНОГО ОБРАЗА MIGRATE
# выбираем используемый базовый образ
FROM python:3.10-slim AS migrate

# создаём рабочую директорию
WORKDIR /app/backend

# копируем зависимости
COPY --from=builder /usr/local /usr/local

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# копируем backend
COPY backend /app/backend

CMD ["python", "manage.py", "migrate", "--noinput"]


# СБОР ФИНАЛЬНОГО ОБРАЗА WEB_PROD
# выбираем используемый базовый образ
FROM python:3.10-slim AS web_prod

# создаём рабочую директорию
WORKDIR /app/backend

# копируем зависимости
COPY --from=builder /usr/local /usr/local

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# копируем backend и frontend
COPY backend /app/backend
COPY frontend /app/frontend

# СБОР ФИНАЛЬНОГО ОБРАЗА WEB_DEV
# выбираем используемый базовый образ
FROM python:3.10-slim AS web_dev

# создаём рабочую директорию
WORKDIR /app/backend

# копируем зависимости
COPY --from=builder /usr/local /usr/local

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
