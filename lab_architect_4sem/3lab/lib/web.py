from flask import Flask, jsonify, request
from datetime import datetime

from lib.cnb import API


def config_server(app, api_instance, offered_currencies):
    @app.route('/', methods=['GET'])
    def index():
        return jsonify(
            currencies=offered_currencies
        )

    @app.route('/currencies/<string:currency_name>', methods=['GET'])
    def get_currency_info(currency_name):
        if currency_name not in offered_currencies:
            return jsonify(
                error='At the moment it is not possible to see information about this currency'
            )
        from_date_str = request.args.get('from')
        to_date_str = request.args.get('to')
        if from_date_str is None or to_date_str is None:
            return jsonify(
                error='Please, provide \'from\' and \'to\' params within the URL'
            )
        from_date = datetime.strptime(from_date_str, '%d.%m.%Y').date()
        to_date = datetime.strptime(to_date_str, '%d.%m.%Y').date()
        return jsonify(
            api_instance.get_currency_info(currency_name, from_date, to_date)
        )


def start_server(config_file_path):
    app = Flask(__name__)
    api_instance = API()
    api_instance.fill_amounts()

    with open(config_file_path, 'r') as file:
        offered_currencies = file.readline().strip().split(' ')
    config_server(app, api_instance, offered_currencies)

    app.run(host='0.0.0.0', port=8080, debug=False)
