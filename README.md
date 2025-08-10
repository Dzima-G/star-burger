# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](/frontend/assets/menu.png)

Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и
одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам
ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро
оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы
и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт
туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит
менеджер, чтобы обновить меню ресторанов Star Burger.

## Для запуска необходимы переменные окружения:
Cоздать файл `backend/.env` в корневом каталоге и запишите туда данные в формате: ПЕРЕМЕННАЯ=значение.
```
.
├── .env
└── backend
...
```
Обязательные переменные окружения:
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. [см. документацию Django](https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-SECRET_KEY).
- `DEBUG` — логическое значение, включает/выключает режим отладки, [см. документацию Django](https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-DEBUG).
- `ALLOWED_HOSTS` — Список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django. [см. документацию Django](https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts).
- `POSTGRES_USER` - пользователь PostgreSQL (например: `admin`);
- `POSTGRES_PASSWORD` - пароль пользователя PostgreSQL (например: `9369992_admin`);
- `POSTGRES_DB` — имя базы данных PostgreSQL (например: `starburger`).
- `POSTGRES_HOST` - адрес хоста PostgreSQL. По умолчанию `localhost`, для запуска в контейнере укажите `db`. Если используется сторонний сервер - укажите IP или доменное имя;
- `POSTGRES_PORT` - порт подключения к PostgreSQL. По умолчанию — `5432`;
- `YANDEX_GEOCODE_API_KEY` - ключ Yandex geocoder, API. Пример: `YANDEX_GEOCODE_API_KEY=d1000000f-3ce6-4344-bfe0-00vv21698888` [см. документацию Yandex](https://developer.tech.yandex.ru/services).

Только при развертывании на сервере prod-версии сайта:
- `REPO_URL`= url для клонирования репозитория (по умолчанию `https://github.com/Dzima-G/star-burger.git`).

Не обязательные переменные окружения:
- `DJANGO_ENV` - настройка профиля Rollbar (профиль по умолчанию 'development').
- `ROLLBAR_ACCESS_TOKEN` - токен Rollbar (логирование организовано с помощью Rollbar) [см. документацию Rollbar](https://rollbar.com).
- `ROLLBAR_DEPLOY_TOKEN` - токен для записи деплоя в Rollbar [см. Rollbar deploy tracking](https://docs.rollbar.com/docs/deploy-tracking), [см. Rollbar source sontrol integration](https://docs.rollbar.com/docs/source-control).



## Запуск dev-версии сайта в Docker
Используйте `star-burger/docker-compose.yml` из корня репозитория.
1. Установите [Docker](https://www.docker.com/get-started) и [Docker Compose](https://docs.docker.com/compose/).
2. Клонируйте репозиторий и перейдите в каталог проекта:
   ```sh
   git clone https://github.com/Dzima-G/star-burger
   ```
3. Перейдите в каталог проекта:
   ```sh
   cd star-burger
   ```
4. Соберите и запустите контейнеры:
    ```sh
    docker compose up --build
    ```
5. После запуска сайт будет доступен по адресу: [http://localhost:8000/](http://localhost:8000/).

![скриншот сайта](/frontend/assets/index.png)

* Создать административную учетную запись:

    ```sh
    docker compose exec web sh -lc 'python manage.py createsuperuser'
    ```

## Быстрое развертывание на сервере prod-версии сайта в Docker
1. Скопируйте файл `stage/deploy` и `.env` в папку на сервере (например `opt`).
2. Запустите Bash скрипт деплоя:
    ```sh
    ./deploy
    ```
    Если у файла нет прав на исполнение выполните команду:

    ```sh
    chmod +x deploy
    ```
* Создать административную учетную запись:

  - Перейдите в каталог проекта:
     ```sh
     cd star-burger/stage
     ```
  - запустите команду:

      ```sh
      docker compose exec web sh -lc 'python manage.py createsuperuser'
      ```
Настройте Nginx указав пути к stsic и media (с учетом расположения проекта `opt/star-burger/`):

`/star-burger/static/`

`/star-burger/media/`

Пример сайта можно посмотреть: https://starburger.site
