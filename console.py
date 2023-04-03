import requests
import argparse


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=7798, type=int)
    return parser


def ask_for(something):
    return input(f'Введите {something}: ')


def print_help():
    print("Чтобы выйти, введите команду exit\n"
          "Чтобы создать аккаунт, введите команду create_account\n"
          "Чтобы получить список всех продуктов, введите команду list_products\n"
          "Чтобы получить информацию о конкретном продукте, введите команду get_product\n"
          "Чтобы сформировать новый заказ, введите команду new_order\n"
          "Чтобы получить информацию о конкретном заказе, введите команду get_order\n"
          "Чтобы получить все заказы пользователя, введите команду list_orders\n"
          "Чтобы получить информацию о конкретной доставке, введите команду get_delivery\n"
          "Чтобы получить информацию о всех доставках клиента, введите команду list_deliveries\n"
          "Чтобы сформировать новую доставку, введите команду new_delivery\n"
          "Чтобы подтвердить, что доставка успешно завершена, введите команду complete_delivery\n"
          "Чтобы увидеть эту строку еще раз, введите команду help")


def graceful_exit():
    ack = input('Вы уверены, что хотите выйти (Y/N)? ')
    if ack == 'Y':
        print('До свидания!')
        exit()


def create_account(args):
    response = requests.post(f'http://{args.host}:{args.port}/accounts/create', params=dict(
        name=ask_for('ФИО клиента'),
        phone=ask_for('телефон'),
        address=ask_for('адрес')
    ))
    print('Новый клиент успешно создан')
    print(response.json())


def list_products(args):
    response = requests.get(f'http://{args.host}:{args.port}/products')
    print(response.json())


def get_product(args):
    response = requests.get(f'http://{args.host}:{args.port}/products/{ask_for("айди продукта")}')
    print(response.json())


def list_orders(args):
    response = requests.get(f'http://{args.host}:{args.port}/clients/{ask_for("айди клиента")}/orders')
    print(response.json())


def get_order(args):
    response = requests.get(f'http://{args.host}:{args.port}/clients/'
                            f'{ask_for("айди клиента")}/orders/{ask_for("айди заказа")}')
    print(response.json())


def new_order(args):
    params = {}
    client_id = ask_for('айди клиента')
    product_id = ask_for('айди продукта')
    while product_id != '':
        cnt = ask_for(f'количество продукта {product_id}')
        if f'prod{product_id}' in params.keys():
            params[f'prod{product_id}'] += cnt
        else:
            params[f'prod{product_id}'] = cnt
        product_id = ask_for('айди продукта (оставьте поле пустым, чтобы закончить заказ)')
    response = requests.post(f'http://{args.host}:{args.port}/clients/{client_id}/orders/new_order',
                             params=params)
    print('Новый заказ успешно создан')
    print(response.json())


def new_delivery(args):
    response = requests.post(f'http://{args.host}:{args.port}/clients/'
                             f'{ask_for("айди клиента")}/deliveries/new_delivery/{ask_for("айди заказа")}')
    print('Новая доставка успешно создана')
    print(response.json())


def complete_delivery(args):
    requests.post(f'http://{args.host}:{args.port}/clients/'
                  f'{ask_for("айди клиента")}/deliveries/{ask_for("айди доставки")}/complete')
    print('Доставка завершена')


def get_delivery(args):
    response = requests.get(f'http://{args.host}:{args.port}/clients/'
                            f'{ask_for("айди клиента")}/deliveries/{ask_for("айди доставки")}')
    print(response.json())


def list_deliveries(args):
    response = requests.get(f'http://{args.host}:{args.port}/clients/'
                            f'{ask_for("айди клиента")}/deliveries')
    print(response.json())


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()
    print_help()

    while True:
        try:
            cmd = input('Введите команду > ')
            if cmd == 'create_account':
                create_account(main_args)
            elif cmd == 'list_products':
                list_products(main_args)
            elif cmd == 'get_product':
                get_product(main_args)
            elif cmd == 'list_orders':
                list_orders(main_args)
            elif cmd == 'get_order':
                get_order(main_args)
            elif cmd == 'new_order':
                new_order(main_args)
            elif cmd == 'new_delivery':
                new_delivery(main_args)
            elif cmd == 'list_deliveries':
                list_deliveries(main_args)
            elif cmd == 'get_delivery':
                get_delivery(main_args)
            elif cmd == 'complete_delivery':
                complete_delivery(main_args)
            elif cmd == 'help':
                print_help()
            elif cmd == 'exit':
                graceful_exit()
            else:
                print(f'Неизвестная команда: {cmd}')
        except KeyboardInterrupt:
            graceful_exit()


if __name__ == '__main__':
    main()
