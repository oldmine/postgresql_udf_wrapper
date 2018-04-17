

# PostgreSQL UDF Wrapper

UDF сервер для [библиотеки графиков](https://ru.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/)

## Getting Started
### Зависимости
```
postgresql 10.1
python 2.7
pip 10.0.0
psycopg2 2.7.4
Flask 0.12.2
Flask-Cors 3.0.3
```

### Запуск

 - Создать базу данных и импортировать таблицы.
 - В файле wrapper.ini в секции [postgresql] указать доступы к базе данных.
 - Перейти в директорию с проектом и выполнить:
    FLASK_APP=wrapper.py flask run --host=0.0.0.0 --port=5001

### Проверка работы
-   `/config`  -  http://127.0.0.1:5001/config

-   `/symbols`  -  http://127.0.0.1:5001/symbols?symbol=NewSymbol

-   `/history`  -  http://127.0.0.1:5001/history?symbol=NewSymbol&resolution=1&from=1523837493&to=1523923953

-   `/search`  -  http://127.0.0.1:5001/search?limit=30&query=NEWSYMBOL&type=&exchange=

-   `/time`  -  http://127.0.0.1:5001/time

### Настройка библиотеки
В TradingView.onready() установить datafeed на
`new Datafeeds.UDFCompatibleDatafeed("http://127.0.0.1:5001")`