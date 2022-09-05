# Эмулятор платежного сервиса (Golang)

### Запуск

docker-compose up<br>
создать venv, запустить<br>
python manage.py runserver<br>

### Эндпоинты
- #### /api/v1/auth/users/ POST (регистрация)
Пример запроса:<br>
{<br>
"username":"second123",<br>
"password":"password123",<br>
}<br>
Пример ответа: <br>
`{
    "email": "",
    "username": "second123",
    "id": 4
}`
- #### /auth/token/login POST (Получение токена авторизации)
Пример запроса:<br>
{<br>
"username":"username",<br>
"password":"password123",<br>
}<br>
Пример ответа: <br>
`{
    "auth_token": "d4520dc030f58d1b2c02742b6234eb6653672a50"
}`
- #### /api/v1/articles/ GET (Просматривать список постов других пользователей, отсортированный по дате создания, сначала свежие)
Пример ответа: <br>
`  [
    {
        "pk": 3,
        "title": "sdffdsfds",
        "content": "dfgfdgdgf",
        "user": 1,
        "time_create": "2022-09-03T08:32:53.995040Z",
        "time_update": "2022-09-03T08:32:53.995051Z"
    },
    {
        "pk": 2,
        "title": "dsasad",
        "content": "dsadsa",
        "user": 2,
        "time_create": "2022-09-03T07:45:08.441861Z",
        "time_update": "2022-09-03T07:45:08.441873Z"
    },`
- #### /api/v1/article/create/ POST (Авторизованным пользователям создавать посты. Пост имеет заголовок и текст поста)
Пример запроса: <br>
`
{
    "title":"title123",
    "content":"content123"
}
`<br>
Пример ответа: <br>
`{
    "pk": 4,
    "title": "title123",
    "content": "content123",
    "time_create": "2022-09-05T07:06:55.093257Z",
    "time_update": "2022-09-05T07:06:55.093277Z"
}`
- #### /api/v1/users/ ?ordering=posts GET (Просматривать список пользователей с возможностью сортировки по количеству постов)
Пример ответа: <br>
`[
    {
        "pk": 4,
        "username": "second123",
        "posts": []
    },
    {
        "pk": 3,
        "username": "second",
        "posts": [
            4
        ]
    },
    {
        "pk": 2,
        "username": "test",
        "posts": [
            2
        ]
    },
    {
        "pk": 1,
        "username": "123",
        "posts": [
            3,
            1
        ]
    }
]`
- #### /api/v1/sub/ POST (Авторизованным пользователям подписываться и отписываться на посты другихпользователей)
Пример запроса:<br>
`{
    "user_id":4,
    "sub_id":1
}
`<br>
Пример ответа: <br>
`{
    "status": "created"
}`
- #### /api/v1/sub/ DELETE
Пример запроса:<br>
`{
    "user_id":4,
    "sub_id":1
}
`<br>
Пример ответа: <br>
`{
    "status": "Object deleted"
}`
- #### /api/v1/sublist/ GET (Авторизованным пользователям формировать ленту из постов пользователей, на которые была осуществлена подписка.)
Пример ответа: <br>
`    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": 3,
            "title": "sdffdsfds",
            "content": "dfgfdgdgf",
            "user": 1,
            "time_create": "2022-09-03T08:32:53.995040Z",
            "time_update": "2022-09-03T08:32:53.995051Z"
        },
        {
            "pk": 1,
            "title": "123",
            "content": "123",
            "user": 1,
            "time_create": "2022-09-03T06:52:31.340000Z",
            "time_update": "2022-09-03T06:52:31.340049Z"
        }
    ]
}`

### Тесты
Тесты написаны для GET запросов, файл main_test.go. <br>
запуск тестов: <br> cd app <br> go test