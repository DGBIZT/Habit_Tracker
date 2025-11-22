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

#### Лицензия
Этот проект лицензирован по [лицензии MIT](LICENSE).