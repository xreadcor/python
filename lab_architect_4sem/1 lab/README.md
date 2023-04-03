# Задание 1. Клиент-серверное приложение

### Установка зависимостей и запуск:
0) *Скрипты для создания бд находятся в папке scripts*
1) python -m venv .
2) pip install -r requirements.txt
3) python server/main.py - *запуск сервера*
4) python client/console.py - *запуск консольного клиента*

### Функционал API:
1) POST /accounts/create?name={name}&phone={phone}&address={address} - регистрация нового клиента
2) GET /products - получить список всех доступных товаров
3) GET /products/{product_id} - получить информацию о товаре
4) GET /clients/{clients_id}/orders - получить информацию о заказах пользователя
5) GET /clients/{clients_id}/orders/{order_id} - получить информацию о конкретном заказе пользователя
6) POST /clients/{client_id}/orders/new_order?prod{prod_id}={prod_count}&prod{prod_id}={prod_count}&... - оформить заказ от имени пользователя
7) POST /clients/{client_id}/deliveries/new_delivery/{order_id} - создать доставку заказа
8) GET /clients/{client_id}/deliveries/{delivery_id} - получить информацию о доставке
9) POST /clients/{client_id}/deliveries/{delivery_id}/complete - отметить, что доставка пришла
10) GET /clients/{client_id}/deliveries - получить информацию обо всех доставках клиента