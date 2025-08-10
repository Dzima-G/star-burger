# СОБОР FRONTEND

# выбираем используемый базовый образ
FROM node:17.6.0-slim AS builder

# создаём рабочую директорию
WORKDIR /app/static

# копируем файлы конфигурации frontend
COPY package*.json ./

# устанавливаем зависимости frontend
RUN npm ci

# Копируем исходники frontend
COPY bundles-src ./bundles-src

# собираем frontend
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"


# СБОР ФИНАЛЬНОГО ОБРАЗА

# выбираем используемый базовый образ
FROM alpine:3.18

# создаём рабочую директорию
WORKDIR /app/static

# копируем файлы frontend
COPY --from=builder /app/static/bundles ./bundles
