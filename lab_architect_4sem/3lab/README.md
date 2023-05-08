# WEB-API для отчетов о курсе валют относительно чешской кроны

## Установка:
```console
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Использование:
### 1) Базовая команда
```console
usage: main.py [-h] {fill,schedule,launch} ...

Console client for synchronizing and retrieving data about currencies

options:
  -h, --help            show this help message and exit

commands:
  CLI commands

  {fill,schedule,launch}
    fill                Fills the database with exchange rate data for a certain period
    schedule            Start a scheduled task, which will save the current course in the database.
    launch              Start a web API, which provides reports on different currencies over a period of time
```
### 2) Команда fill
Наполняет базу данных курсами валюты за определенный год
Параметр *--year* - год, данные о котором нужно загрузить в базу данных.
```console
usage: main.py fill [-h] --year YEAR

options:
  -h, --help            show this help message and exit
  --year YEAR, -y YEAR  The year you want to fill in the information about
```
### 3) Команда schedule
Запускает фоновую задачу, которая раз в несколько дней загружает новые данные о курсе валюты (по дням)
Параметр *--interval* - период выполнения в днях (раз в *n* дней текущие данные будут загружаться в базу)
```console
usage: main.py schedule [-h] --interval INTERVAL

options:
  -h, --help            show this help message and exit
  --interval INTERVAL, -i INTERVAL
                        Interval between filling database (in days)
```
### 4) Команда launch
Запускает веб-сервер для получения отчетов через API в формате JSON
Параметр *--config* - путь к файлу конфигурации, в котором задаются названия обслуживаемых валют (через пробел).
Список доступных валют:
```aud, brl, bgn, cad, cny, dkk, eur, hkd, huf, isk, xdr, inr, idr, ils, jpy, myr, mxn, nzd, nok, php, pln, ron, sgd, zar, krw, sek, chf, thb, try, gpb, usd```
Пример файла - default.cfg в корне проекта.
```console
usage: main.py launch [-h] --config CONFIG

options:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to server's config file
```
Описание API:
```
/ - получить список всех доступных валют
/currencies/{currency_name}?from={from_date}&to={to_date} - получить отчет о курсе валюты 
за период с from_date до to_date
```