# StarNavi Project

#####Для настройки данного програмного продукта необходимо:
1. Установить Python 3.7+, PostgreSQL.
2. Установить зависимости выполнив команду `pip3 install -r requirements.txt`.
3. Настроить конфигурационный файл. Для этого необходимо в корне проекта создать директорию `configs` и поместить в нее файл `main.ini` со следующим содержанием:
```ini
[MAIN]

# string
server_host = 0.0.0.0

# integer
server_port = 12345

# string (randomly string)
secret_key = your_secret_key

[DATABASE]

# string
username = your_username

# string
password = your_password

# string
db_name = database

# string
host = localhost

# integer
port = 5432
```

#####Для запуска необходимо выполнить следующую команду: `python3 app.py`.

#####Описание API:
1\. Регистрация `/api/registration/`, метод - `POST`:

Тело запроса: 
```json
{
    "username": "имя_пользователя", 
    "password": "пароль"
}
```
Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": null
}
```
2\. Авторизация `/api/login/`, метод - `POST`:

Тело запроса: 
```json
{
    "username": "имя_пользователя", 
    "password": "пароль"
}
```
Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": {
        "access_token": "токен"
    }
}
```
В случае ошибки авторизации - `status_code = 401`

3\. Создание поста `/api/create_post/`, метод - `POST`:

Заголовок:
```json
{
    "Authorization": "Bearer токен_для_авторизации"
}
```
Тело запроса: 
```json
{
    "title": "название_поста", 
    "text": "содержимое",
    "timestamp": "unix_time"
}
```
Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": null
}
```
4\. Сохранение положительной отметки (лайк) `/api/like_post/`, метод - `POST`:

Заголовок:
```json
{
    "Authorization": "Bearer токен_для_авторизации"
}
```
Тело запроса: 
```json
{
    "post_id": "идентификатор_поста", 
    "timestamp": "unix_time"
}
```
Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": null
}
```
5\. Сохранение отрицательной отметки (дизлайк) `/api/dislike_post/`, метод - `POST`:

Заголовок:
```json
{
    "Authorization": "Bearer токен_для_авторизации"
}
```
Тело запроса: 
```json
{
    "post_id": "идентификатор_поста", 
    "timestamp": "unix_time"
}
```
Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": null
}
```
6\. Активность пользователя `/api/user_activity/{user_id}`, метод - `GET`:

Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": {
        "last_login_time": "дата, время (datetime)",
        "last_action_time": "дата, время (datetime)"
    }
}
```
7\. Аналитика лайков/дизлайков во временном диапазоне `/api/analytics/from/{yyyy-mm-dd}/to/{yyyy-mm-dd}`, метод - `GET`:

Ответ (успешное выполнение): 
```json
{
    "success": true, 
    "message": "OK", 
    "data": {
        "posts": {
            "идентификатор_поста1": {
                "number_of_likes": "количество_лайков",
                "number_of_dislikes": "количество_дизлайков"
            },
            "идентификатор_поста2": {
                "number_of_likes": "количество_лайков",
                "number_of_dislikes": "количество_дизлайков"
            },
            ...
        }   
    }
}
```

#####В случае возникновени ошибок при обработке запросов ответ будет выглядить след. образом:
```json
{
    "success": false, 
    "message": "сообщение_об_ошибке", 
    "data": null
}
```
