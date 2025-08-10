# СОБОР ЗАВИСИМОСТЕЙ

# выбираем используемый базовый образ
FROM python:3.7-slim AS builder

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

# СБОР ФИНАЛЬНОГО ОБРАЗА

# выбираем используемый базовый образ
FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000"

# создаём рабочую директорию
WORKDIR /app/backend

# копируем зависимости
COPY --from=builder /usr/local /usr/local

# копируем файлы backend
COPY backend /app/backend

# копируем папку frontend
COPY frontend /app/frontend
#
#EXPOSE 8000
#
#CMD [ "gunicorn", "star_burger.wsgi:application", "--bind 0.0.0.0:8000"]
