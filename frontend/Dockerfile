# СОБОР FRONTEND
# выбираем используемый базовый образ
FROM node:17.6.0-slim AS node-deps

# создаём рабочую директорию
WORKDIR /app/frontend

# копируем файлы конфигурации frontend
COPY package*.json ./

# устанавливаем зависимости frontend
RUN npm ci

# сборка бандлов
FROM node-deps AS prod-build

# создаём рабочую директорию
WORKDIR /app/frontend

# копируем исходники frontend
COPY bundles-src ./bundles-src

# собираем frontend
RUN npx parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

# СБОР ФИНАЛЬНОГО ОБРАЗА PROD
# выбираем используемый базовый образ
FROM alpine:3.18 AS prod

# создаём рабочую директорию
WORKDIR /app/frontend/bundles

# копируем файлы frontend
COPY --from=prod-build /app/frontend/bundles .

# СБОР ФИНАЛЬНОГО ОБРАЗА DEV
# выбираем используемый базовый образ
FROM node-deps AS dev

# создаём рабочую директорию
WORKDIR /app/frontend

# копируем исходники frontend
COPY bundles-src ./bundles-src

# запускаем Parcel с отслеживанием
CMD ["npx", "parcel", "watch", "bundles-src/index.js", "--dist-dir", "/app/frontend/bundles", "--public-url", "./"]
