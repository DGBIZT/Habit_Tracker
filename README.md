# Бэкенд-часть SPA веб-приложения.

1. Описание:
```
 В 2018 году Джеймс Клир написал книгу «Атомные привычки», 
 которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Заказчик прочитал книгу, 
 впечатлился и обратился к нам с запросом реализовать трекер полезных привычек.
 В рамках учебного курсового проекта реализована бэкенд-часть SPA веб-приложения.
```
2. Клонируйте репозиторий:
```
    1) HTTPS 
            https://github.com/DGBIZT/Habit_Tracker.git
    2) SHH
            git@github.com:DGBIZT/Habit_Tracker.git
```
###### №1 Разработка сервиса
```

1. Добавление необходимых моделей привычек.
2. Реализация эндпоинтов для работы с фронтендом.
3. Создание приложения для работы с Telegram и рассылками напоминаний.
    
```
###### №2 Расширение функциональности
```
4. Регистрация и аутентификация пользователей
5. Настройка прав доступа
6. Создание, редактирование и удаления привычек
7. Пагинация с выводом по 5 привычек на страницу


```
###### №3 Практическая часть
```
    1) Создайте БД в PostgreSQL (CREATE -> DATABASE -> SAVE)
    2) В pycharm клонируете репозиторий указанный выше.
    3) Переименнуйте файл .env.exemple в .env и внесите свои данные.
    4) Введите команду python manage.py migrate.
        Благодаря этой команде вы сконектитесь с вашей БД.
    5) Обязательно обновите все зависимости: введите команду poetry update
                       
```
###### №4 Запуск приложения
```
    В терминале нажмите на + и создаcтся Local(2)
        Введите команду python manage.py runserver 
        У вас появится сообщение:
            Watching for file changes with StatReloader
            Performing system checks...

            System check identified no issues (0 silenced).
            September 16, 2025 - 20:04:45
            Django version 5.2.6, using settings 'config.settings'
            Starting development server at http://127.0.0.1:8000/
            Quit the server with CTRL-BREAK.

            WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
            For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/
        
```
# Habit Tracker
```Веб‑приложение для отслеживания привычек.```

#### Локальный запуск проекта
1. Подготовка окружения
```
Установите Docker и Docker Compose.

Клонируйте репозиторий:

bash
git clone https://github.com/DGBIZT/Habit_Tracker.git
cd Habit_Tracker
Создайте файл .env в корне проекта (пример содержимого ниже).
```
2. Настройка переменных окружения
```
Создайте файл .env со следующим содержимым (замените значения на свои):

env
DATABASE_NAME=habit_tracker
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EMAIL_HOST_USER=test@example.com
EMAIL_HOST_PASSWORD=test
3. Запуск сервисов
Выполните команду:

bash
docker-compose up -d --build
```
4. Миграция базы данных
```
После запуска контейнеров выполните миграцию:
bash
docker-compose exec web python manage.py migrate
```
5. Сбор статических файлов
```
bash
docker-compose exec web python manage.py collectstatic --noinput
```
6. Доступ к приложению
```
Откройте в браузере:

158.160.212.149
Развёртывание на удалённом сервере
```
1. Требования к серверу
```
Ubuntu 22.04 или новее;

Установленные Docker и Docker Compose;

Открытый порт 80 (HTTP);

SSH‑доступ с ключом.
```
2. Подготовка сервера
```
Подключитесь к серверу по SSH:

bash
ssh your_username@your_server_ip
Установите Docker:

bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
Создайте директорию для проекта:

bash
mkdir -p /home/your_username/Habit_Tracker
cd /home/your_username/Habit_Tracker
```
3. Развёртывание
```
Клонируйте репозиторий:

bash
git clone https://github.com/DGBIZT/Habit_Tracker.git .
git checkout feature/webtracker
Создайте файл .env (см. шаблон выше).

Запустите сервисы:

bash
docker-compose up -d --build
Выполните миграцию:

bash
docker-compose exec web python manage.py migrate
Соберите статические файлы:

bash
docker-compose exec web python manage.py collectstatic --noinput
```
4. Проверка работы
```
Проверьте статус контейнеров:

bash
docker-compose ps
Проверьте логи:

bash
docker-compose logs web
Адрес сервера с развёрнутым приложением
Приложение доступно по адресу:
http://your_server_ip

(Замените your_server_ip на реальный IP‑адрес сервера.)
```
#### Настройка CI/CD
1. Необходимые секреты GitHub
```В настройках репозитория (Settings → Secrets and variables → Actions) создайте следующие секреты:

POSTGRES — имя пользователя и пароль PostgreSQL (одинаковые);

SECRETKEY — секретный ключ Django;

DOCKER_HUB_USERNAME — имя пользователя Docker Hub;

DOCKERTOKEN — токен Docker Hub;

SERVER_SSH_KEY — приватный SSH‑ключ сервера (в формате PEM);

SERVER_USERNAME — имя пользователя на сервере;

SERVER_HOST — IP‑адрес или домен сервера.
```
2. Процесс CI/CD
```
Тестирование (test):

Запуск PostgreSQL и Redis в контейнерах;

Установка зависимостей Python;

Проверка кода (flake8, black, isort);

Миграция базы данных;

Запуск тестов с покрытием.

Сборка (build):

Создание файла .env;

Авторизация в Docker Hub;

Сборка Docker‑образа с тегом ${{ github.sha }};

Отправка образа в Docker Hub.

Деплой (deploy):

Подключение к серверу по SSH;

Загрузка нового образа из Docker Hub;

Остановка и удаление старого контейнера;

Запуск нового контейнера на порту 80.
```
3. Триггеры workflow
```
Автоматически при:

Push в ветку feature/webtracker;

Pull Request в ветку develop.

Вручную через интерфейс GitHub (кнопка «Run workflow»).
```
4. Статус деплоя
```
После успешного выполнения workflow приложение будет доступно по указанному адресу сервера.

Дополнительные команды
Остановка всех сервисов:

bash
docker-compose down
Перезагрузка без перестройки:

bash
docker-compose restart
Просмотр логов:

bash
docker-compose logs -f
```
#### Дополнительные команды для управления проектом
###### Ниже приведены полезные команды для работы с Docker Compose, которые помогут управлять приложением, диагностировать проблемы и оптимизировать работу.

1. Управление контейнерами
```Запуск всех сервисов (в фоновом режиме):

bash
docker-compose up -d
Перезапуск всех контейнеров (остановка → запуск):

bash
docker-compose restart
Остановка контейнеров (без удаления):

bash
docker-compose stop
Запуск остановленных контейнеров:

bash
docker-compose start
Полное удаление контейнеров, сетей и объёмов:

bash
docker-compose down
Пересоздание контейнеров (даже если конфигурация не изменилась):

bash
docker-compose up --force-recreate
```
2. Мониторинг и диагностика
```
Просмотр списка запущенных контейнеров (статус, порты):

bash
docker-compose ps
Просмотр логов всех контейнеров:

bash
docker-compose logs
Просмотр логов конкретного сервиса (например, web):

bash
docker-compose logs web
Слежение за логами в реальном времени (всех контейнеров):

bash
docker-compose logs -f
Слежение за логами конкретного сервиса в реальном времени:

bash
docker-compose logs -f web
Просмотр запущенных процессов в контейнерах:

bash
docker-compose top
```
3. Работа с образами и сборкой
```
Сборка образов (без использования кэша):

bash
docker-compose build --no-cache
Загрузка актуальных образов из реестра перед запуском:

bash
docker-compose pull
Проверка конфигурации проекта (вывод итоговых параметров):

bash
docker-compose config
```
4. Выполнение команд внутри контейнеров
```
Выполнение команды в контейнере (например, ls в сервисе web):

bash
docker-compose exec web ls
Открытие интерактивной оболочки в контейнере:

bash
docker-compose exec web bash
Выполнение миграций Django внутри контейнера:

bash
docker-compose exec web python manage.py migrate
Сбор статических файлов Django:

bash
docker-compose exec web python manage.py collectstatic --noinput
```
5. Управление сетями и объёмами
```
Просмотр списка сетей проекта:

bash
docker-compose network ls
Просмотр списка объёмов проекта:

bash
docker-compose volume ls
```
6. Оптимизация и очистка
```
Удаление остановленных контейнеров и неиспользуемых образов:

bash
docker system prune -f
Очистка неиспользуемых объёмов:

bash
docker volume prune -f
Очистка неиспользуемых сетей:

bash
docker network prune -f
```
7. Полезные опции для docker-compose up
```
Сборка перед запуском:

bash
docker-compose up --build
Запуск в фоновом режиме (демонизация):

bash
docker-compose up -d
Игнорирование пересборки (если образы уже есть):

bash
docker-compose up --no-build
Принудительное пересоздание контейнеров:

bash
docker-compose up --force-recreate
8. Отладка и тестирование
Проверка доступности сервиса (например, web на порту 8000):

bash
curl http://localhost:8000
Просмотр переменных окружения в контейнере:

bash
docker-compose exec web env
Проверка подключения к БД (внутри контейнера):

bash
docker-compose exec web python -c "import django; django.setup(); from django.db import connection; print(connection.queries)"
```

#### Лицензия
Этот проект лицензирован по [лицензии MIT](LICENSE).