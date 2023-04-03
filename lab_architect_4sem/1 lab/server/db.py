from sqlalchemy.engine import create_engine
from sqlalchemy.sql import text
import random


class DBInstance:
    def __init__(self, user, passwd, db_name):
        engine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@localhost/{db_name}')
        self.conn = engine.connect()

    def _get_courier(self):
        query = text("SELECT id FROM courier")
        data_raw = self.conn.execute(query)
        ids = []
        for id, in data_raw.fetchall():
            ids.append(id)
        return random.choice(ids)

    def _calculate_cost(self, products):
        total_cost = 0
        query = text(f'SELECT id, price FROM product')
        result = self.conn.execute(query).fetchall()
        for product_id, price in result:
            if product_id in products.keys():
                total_cost += float(price) * int(products[product_id])
        return total_cost

    def get_all_products(self):
        query = text('SELECT * FROM product')
        result = self.conn.execute(query)
        return result.fetchall()

    def get_product(self, product_id):
        query = text(f'SELECT * FROM product WHERE id = {product_id}')
        result = self.conn.execute(query)
        return result.fetchone()

    def add_client(self, name, phone, address):
        query = text(f"INSERT INTO client (name, phone_number, address) "
                     f"VALUES ('{name}', '{phone}', '{address}') RETURNING id")
        result = self.conn.execute(query)
        self.conn.commit()
        return int(result.fetchone()[0])

    def get_order_info(self, order_id):
        query = text(f"SELECT product.name, order_products.number, product.price FROM order_products "
                     f"INNER JOIN product ON product.id = order_products.product_id "
                     f"WHERE order_id = {order_id}")
        result = self.conn.execute(query)
        return result.fetchall()

    def get_client_orders(self, client_id):
        query = text(f"SELECT * FROM orders "
                     f"WHERE client_id = {client_id}")
        result = self.conn.execute(query)
        return result.fetchall()

    def new_order(self, client_id, timestamp, products):
        sum_cost = self._calculate_cost(products)
        query = text(f"INSERT INTO orders (client_id, order_time, cost) "
                     f"VALUES ({client_id}, '{timestamp}', {sum_cost}) RETURNING id")
        order_id_raw = self.conn.execute(query).fetchone()
        order_id = int(order_id_raw[0])
        for product_id, quantity in products.items():
            query = text(f"INSERT INTO order_products (order_id, product_id, number) "
                         f"VALUES ({order_id}, {product_id}, {quantity})")
            self.conn.execute(query)
        self.conn.commit()
        return order_id

    def new_delivery(self, order_id):
        courier_id = self._get_courier()
        query = text(f"INSERT INTO delivery (order_id, courier_id, arrived) "
                     f"VALUES ('{order_id}', '{courier_id}', FALSE) "
                     f"RETURNING id")
        result = self.conn.execute(query)
        self.conn.commit()
        return int(result.fetchone()[0])

    def get_delivery(self, delivery_id):
        query = text(f"SELECT delivery.order_id, courier.name, courier.phone_number FROM delivery INNER JOIN "
                     f"courier ON courier.id = delivery.courier_id "
                     f"WHERE delivery.id = {delivery_id}")
        result = self.conn.execute(query)
        return result.fetchone()

    def complete_delivery(self, delivery_id, timestamp):
        query = text(f"UPDATE delivery "
                     f"SET (delivery_time, arrived) = ('{timestamp}', TRUE) "
                     f"WHERE id = {delivery_id}")
        self.conn.execute(query)
        self.conn.commit()

    def list_deliveries(self, client_id):
        query = text(f'SELECT delivery.id, delivery.delivery_time, delivery.arrived FROM delivery '
                     f'INNER JOIN orders ON orders.id = delivery.order_id '
                     f'WHERE orders.client_id = {client_id}')
        result = self.conn.execute(query)
        return result.fetchall()
