CREATE DATABASE store_db;

CREATE TABLE client (
    id serial primary key,
    name varchar(100) not null,
    phone_number varchar(15) not null unique,
    address text not null
);

CREATE TABLE orders (
    id serial primary key,
    client_id serial references client (id),
    order_time timestamp not null,
    cost numeric(8, 2) check (cost > 0)
);

CREATE TABLE product (
    id serial primary key,
    name varchar(40) not null unique,
    price numeric(6, 2) check (price > 0)
);

CREATE TABLE order_products (
    id serial primary key,
    order_id serial references orders (id),
    product_id serial references product (id),
    number int not null
);

CREATE TABLE courier (
    id serial primary key,
    name varchar(40) not null,
    phone_number varchar(15) not null unique
);

CREATE TABLE delivery (
    id serial primary key,
    order_id serial references orders (id),
    courier_id serial references courier (id),
    delivery_time timestamp,
    arrived bool
);