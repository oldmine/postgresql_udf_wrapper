
# PostgreSQL UDF Wrapper
## wrapper.ini
#### [postgresql]
Данные для подключения к базе данных

**Пример**

    postgres_host = localhost
    postgres_database = tradingview
    postgres_username = postgres
    postgres_password =

### [wrapper]
Базовая настройка сервера
#### supported_resolutions
Поддерживаемые сервером разрешения. По умолчанию:

    1,5,15,30,60,240,1D
#### error_message
Сообщение в случае ошибки получения данных.
#### supports_search
Поддержка сервером поиска символов.
#### supports_time
Поддержка сервером трансляции времени.
#### supports_group_request
Не используется.
#### supports_marks
Не используется.