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

# копируем backend
COPY backend /app/backend

# копируем frontend
COPY frontend /app/frontend

RUN python manage.py collectstatic --noinput

# СБОР ФИНАЛЬНОГО ОБРАЗА

# выбираем используемый базовый образ
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# создаём рабочую директорию
WORKDIR /app/backend

# копируем зависимости
COPY --from=builder /usr/local /usr/local

# копируем backend и frontend
COPY backend /app/backend
COPY frontend /app/frontend

# копируем static
COPY --from=builder /app/static /app/static
