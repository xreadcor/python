from flask import Flask, request, Response
from db import DBInstance
from datetime import datetime
import json


app = Flask(__name__)
db = DBInstance('postgres', 'postgres', 'store_db')
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def validate_product_data(product):
    return {
        'id': int(product[0]),
        'name': str(product[1]),
        'price': float(product[2])
    }


def validate_order_data(order):
    return {
        'id': int(order[0]),
        'client_id': int(order[1]),
        'order_time': order[2].strftime(TIME_FORMAT),
        'cost': float(order[3])
    }


def validate_order_info(order_id, order):
    items_list = []
    for name, cnt, price in order:
        items_list.append({
            'name': str(name),
            'count': int(cnt),
            'price (for one)': float(price)
        })
    return {
        'order_id': order_id,
        'items': items_list
    }


def validate_delivery(delivery):
    return {
        'order_id': int(delivery[0]),
        'courier_name': str(delivery[1]),
        'courier_phone': str(delivery[2])
    }


def validate_delivery_info(delivery):
    return {
        'id': delivery[0],
        'delivery_time': delivery[1].strftime(TIME_FORMAT) if delivery[1] is not None else '',
        'arrived': delivery[2] if delivery[2] is not None else ''
    }


@app.route('/accounts/create', methods=['POST'])
def create_account():
    """
    Register a new client
    :return: 200 OK HTTP response
    """
    name = str(request.args.get('name'))
    phone_number = str(request.args.get('phone'))
    address = str(request.args.get('address'))
    client_id = int(db.add_client(name, phone_number, address))
    response = {
        'client_id': client_id
    }
    return Response(response=json.dumps(response), status=200)


@app.route('/products', methods=['GET'])
def get_all_products():
    """
    Get all products in the store, fields - (id, name, price)
    :return: list of products in json format
    """
    products_raw = db.get_all_products()
    products = json.dumps(
        {'products': [json.dumps(validate_product_data(product), ensure_ascii=False) for product in products_raw]},
        ensure_ascii=False
    )
    return Response(response=products, status=200)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get info about the product, fields - (id, name, price)
    :param product_id: product id
    :return: product info in json format
    """
    product_raw = db.get_product(product_id)
    product = json.dumps(validate_product_data(product_raw), ensure_ascii=False)
    return Response(response=product, status=200)


@app.route('/clients/<int:client_id>/orders', methods=['GET'])
def list_orders(client_id):
    """
    List all client orders, fields - (id, client id, order time, cost)
    :param client_id: client id
    :return: list of orders info in json format
    """
    orders_raw = db.get_client_orders(client_id)
    orders = json.dumps(
        {'orders': [json.dumps(validate_order_data(order)) for order in orders_raw]},
        ensure_ascii=False
    )
    return Response(response=orders, status=200)


@app.route('/clients/<int:client_id>/orders/<int:order_id>', methods=['GET'])
def get_order(client_id, order_id):
    """
    Get client order by id, fields - (order id, items)
    Item format - (product name, count, price for one product)
    :param order_id: order id
    :return: order info in json format
    """
    order_raw = db.get_order_info(order_id)
    order = json.dumps(validate_order_info(order_id, order_raw), ensure_ascii=False)
    return Response(response=order, status=200)


@app.route('/clients/<int:client_id>/orders/new_order', methods=['POST'])
def new_order(client_id):
    """
    Creates new order for a client
    URL format: http://.../new_order/prod{product_id}={count}&prod{product_id}={count}&...
    :param client_id: id of the client making order
    :return: 200 OK HTTP response
    """
    timestamp = datetime.now().strftime(TIME_FORMAT)
    order_data = {}
    for prod_id_raw, product_cnt in request.args.items():
        if prod_id_raw.startswith('prod'):
            order_data[int(prod_id_raw[4:])] = product_cnt
    order_id = int(db.new_order(client_id, timestamp, order_data))
    response = {
        'order_id': order_id
    }
    return Response(response=json.dumps(response), status=200)


@app.route('/clients/<int:client_id>/deliveries/new_delivery/<int:order_id>', methods=['POST'])
def new_delivery(client_id, order_id):
    """
    Creates new delivery for the order
    :param order_id: order id
    :return: 200 OK HTTP response
    """
    delivery_id = int(db.new_delivery(order_id))
    response = {
        'delivery_id': delivery_id
    }
    return Response(response=json.dumps(response), status=200)


@app.route('/clients/<int:client_id>/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(client_id, delivery_id):
    """
    Get info about delivery, fields - (order id, courier name, courier phone)
    :param delivery_id: delivery id
    :return: delivery info in json format
    """
    delivery_raw = db.get_delivery(delivery_id)
    delivery = json.dumps(validate_delivery(delivery_raw), ensure_ascii=False)
    return Response(response=delivery, status=200)


@app.route('/clients/<int:client_id>/deliveries/<int:delivery_id>/complete', methods=['POST'])
def complete_delivery(client_id, delivery_id):
    """
    Mark delivery as complete, sets timestamp in db
    :param delivery_id: delivery id
    :return: 200 OK HTTP response
    """
    timestamp = datetime.now().strftime(TIME_FORMAT)
    db.complete_delivery(delivery_id, timestamp)
    return Response(response='OK', status=200)


@app.route('/clients/<int:client_id>/deliveries', methods=['GET'])
def list_deliveries(client_id):
    """
    Get list of all clients deliveries, fields - (id, delivery time, arrived)
    :param client_id: client id
    :return: list of deliveries in json format
    """
    deliveries_raw = db.list_deliveries(client_id)
    deliveries = json.dumps(
        {
            'deliveries': [json.dumps(validate_delivery_info(delivery), ensure_ascii=False)
                           for delivery in deliveries_raw]
        },
        ensure_ascii=False
    )
    return Response(response=deliveries, status=200)


if __name__ == '__main__':
    app.run('127.0.0.1', 7798)
