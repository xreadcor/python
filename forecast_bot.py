# Импорт необходимых модулей и настроек
import telebot
from telebot import types
import requests
import \
    cities_dict  # словарь с наименования городов, где ключ - название города на русском языке, а значение словаря - на английском
from bs4 import BeautifulSoup as bs

# Установка связи с телеграм-ботом
bot = telebot.TeleBot('1098357830:AAE5VuBOj2a4yhYobr_gfB5Zqh97zTfpDJk')

# Настройка интерактивной клавиатуры
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/start', '/help')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('/start')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('1', '2', '3')
keyboard3.row('4', '5', '6')
keyboard3.row('/help')


@bot.message_handler(commands=['start'])
def start_talking(message):
    '''
    Функция, которая запускает бота по команде /start. Приветствует пользователя и объясняет свой функционал
    '''
    bot.send_message(message.chat.id, 'Привет, я бот, который может подсказать погоду в твоем городе!')
    bot.send_message(message.chat.id, 'Выбери цифру, которая соответствует твоему запросу:\n'
                                      '1 - Узнать температуру\n'
                                      '2 - Узнать наличие осадков\n'
                                      '3 - Узнать скорость и направление ветра\n'
                                      '4 - Узнать влажность воздуха\n'
                                      '5 - Узнать атмосферное давление\n'
                                      '6 - Узнать все сразу\n', reply_markup=keyboard3)
    bot.send_message(message.chat.id, 'Либо просто введи в чат запрос по типу "Погода Москва"\т'
                                      'или "Влажность Санкт-Петербург"\n'
                                      'Какие запросы я могу обработать:\n'
                                      '"Погода" - вывести всю информацию о погоде\n'
                                      '"Осадки" - вывести информацию об осадках в городе\n'
                                      '"Влажность" - вывести информацию о влажности воздуха\n'
                                      '"Давление" или "АД" - вывести информацию об атм. давлении\n'
                                      '"Ветер" - информация о направлении и скорости ветра\n'
                                      '"Температура" - текущая температура и ощущаемая температура')


@bot.message_handler(commands=['help'])
def help_message(message):
    '''
    Функция, которая реагирует на команду /help и вызывает меню помощи.
    '''
    bot.send_message(message.chat.id, 'Имя бота: forecast_bot.\n'
                                      'Для чего: рассказать тебе о погоде в твоем городе.\n'
                                      'Что для этого нужно: достаточно ввести команду \start\n'
                                      'выбрать нужную цифру и ввести название города, погода в котором тебя интересует.\n'
                                      'Либо ввести запрос по типу: ПАРАМЕТР + ГОРОД, например, Температура Москва\n'
                                      'Возможные параметры:\n'
                                      '"Погода" - вывести всю информацию о погоде\n'
                                      '"Осадки" - вывести информацию об осадках в городе\n'
                                      '"Влажность" - вывести информацию о влажности воздуха\n'
                                      '"Давление" - вывести информацию об атм. давлении\n'
                                      '"Ветер" - информация о направлении и скорости ветра\n'
                                      '"Температура" - текущая температура и ощущаемая температура\n'
                                      'Посмотреть погоду и решить как одеться.\n'
                                      'Готово!', reply_markup=keyboard2)


@bot.message_handler(content_types=['text'])
def buttons(message):
    '''
    Функция обеспечивает регаирование бота на сообщение от пользователя
    Обеспечивает работу бота и вывод погоды с помощью интерактивной клавиатуры
    Если же пользователь решает ввести запрос из 2 слов, переводит действие на другую функцию - zapros()
    '''
    if message.text == '6':
        message_6 = bot.send_message(message.chat.id, 'Введи свой город')
        bot.register_next_step_handler(message_6, send_message_6)
    if message.text == '1':
        message_1 = bot.send_message(message.chat.id, 'Введи свой город')
        bot.register_next_step_handler(message_1, send_message_1)
    if message.text == '2':
        message_2 = bot.send_message(message.chat.id, 'Введи свой город')
        bot.register_next_step_handler(message_2, send_message_2)
    if message.text == '3':
        message_3 = bot.send_message(message.chat.id, 'Введи свой город')
        bot.register_next_step_handler(message_3, send_message_3)
    if message.text == '4':
        message_4 = bot.send_message(message.chat.id, 'Введи свой город')
        bot.register_next_step_handler(message_4, send_message_4)
    if message.text == '5':
        message_5 = bot.send_message(message.chat.id, 'Введи свой город')
        bot.register_next_step_handler(message_5, send_message_5)
    if message.text not in ['1', '2', '3', '4', '5', '6']:
        sps = message.text.lower().split(' ')
        if len(sps) > 2:
            bot.send_message(message.chat.id,
                             'Неверный запрос. Следует вводить так: Погода Москва или Влажность Пермь\n'
                             'или воспользуйтесь клавиатурой')
        elif sps[0] in ['погода', 'осадки', 'влажность', 'давление', 'ад', 'ветер', 'температура']:
            zapros(message, sps[0], sps[1])


def zapros(message, param, town):
    '''
    Функция обеспечивает работу бота посредством обработки текстового запроса из 2 слов
    message - параметр, хранящий информацию о сообщении, необходим для корректной работы бота
    param - хранит информацию о необходимой информации по погоде. Например: температура, влажность, давление. Первое слово в запросе
    town - хранит название города, в котором надо узнать погоду. Второе слово в запросе пользователя
    '''
    if param == 'погода':
        try:
            city = cities_dict.rus_cities[town.lower()]
            req = requests.get('https://yandex.ru/pogoda/' + str(city))
            html = bs(req.content, 'html.parser')
            current_temp = html.select('.content__row .temp__value')[1].text
            feel_temp = html.select('.term__value .temp__value')[1].text
            wind = html.select('.fact__props .term__value')[0].text
            humidity = html.select('.fact__props .term__value')[1].text
            pressure = html.select('.fact__props .term__value')[2].text
            state = html.select('.link__feelings .link__condition')[0].text
            bot.send_message(message.chat.id, f'Итак, вот какая погода в твоем городе\n'
                                              f'Город:{town}\n'
                                              f'Текушая температура:{current_temp}\n'
                                              f'Ощущается как:{feel_temp}\n'
                                              f'{state}\n'
                                              f'Ветер:{wind}\n'
                                              f'Влажность:{humidity}\n'
                                              f'Давление:{pressure}')
            bot.send_message(message.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                              '1 - Узнать температуру\n'
                                              '2 - Узнать наличие осадков\n'
                                              '3 - Узнать скорость и направление ветра\n'
                                              '4 - Узнать влажность воздуха\n'
                                              '5 - Узнать атмосферное давление\n'
                                              '6 - Узнать все сразу\n'
                                              'Или просто введи запрос из 2 слов. Подробности в /help',
                             reply_markup=keyboard3)
        except (AttributeError, KeyError):
            bot.send_message(message.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
            pass

    if param == 'температура':
        try:
            city = cities_dict.rus_cities[town.lower()]
            req = requests.get('https://yandex.ru/pogoda/' + str(city))
            html = bs(req.content, 'html.parser')
            current_temp = html.select('.content__row .temp__value')[1].text
            feel_temp = html.select('.term__value .temp__value')[1].text
            bot.send_message(message.chat.id, f'Итак, вот что с температурой в твоем городе\n'
                                              f'Город:{town}\n'
                                              f'Текушая температура:{current_temp}\n'
                                              f'Ощущается как:{feel_temp}\n')
            bot.send_message(message.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                              '1 - Узнать температуру\n'
                                              '2 - Узнать наличие осадков\n'
                                              '3 - Узнать скорость и направление ветра\n'
                                              '4 - Узнать влажность воздуха\n'
                                              '5 - Узнать атмосферное давление\n'
                                              '6 - Узнать все сразу\n'
                                              'Или просто введи запрос из 2 слов. Подробности в /help',
                             reply_markup=keyboard3)
        except (AttributeError, KeyError):
            bot.send_message(message.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
            pass

    if param == 'осадки':
        try:
            city = cities_dict.rus_cities[town.lower()]
            req = requests.get('https://yandex.ru/pogoda/' + str(city))
            html = bs(req.content, 'html.parser')
            state = html.select('.link__feelings .link__condition')[0].text
            bot.send_message(message.chat.id, f'Итак, вот что с осадками в твоем городе\n'
                                              f'{state}\n')
            bot.send_message(message.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                              '1 - Узнать температуру\n'
                                              '2 - Узнать наличие осадков\n'
                                              '3 - Узнать скорость и направление ветра\n'
                                              '4 - Узнать влажность воздуха\n'
                                              '5 - Узнать атмосферное давление\n'
                                              '6 - Узнать все сразу\n'
                                              'Или просто введи запрос из 2 слов. Подробности в /help',
                             reply_markup=keyboard3)
        except (AttributeError, KeyError):
            bot.send_message(message.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
            pass

    if param == 'ветер':
        try:
            city = cities_dict.rus_cities[town.lower()]
            req = requests.get('https://yandex.ru/pogoda/' + str(city))
            html = bs(req.content, 'html.parser')
            wind = html.select('.fact__props .term__value')[0].text
            bot.send_message(message.chat.id, f'Итак, вот что с ветром в твоем городе\n'
                                              f'Ветер:{wind}\n')
            bot.send_message(message.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                              '1 - Узнать температуру\n'
                                              '2 - Узнать наличие осадков\n'
                                              '3 - Узнать скорость и направление ветра\n'
                                              '4 - Узнать влажность воздуха\n'
                                              '5 - Узнать атмосферное давление\n'
                                              '6 - Узнать все сразу\n'
                                              'Или просто введи запрос из 2 слов. Подробности в /help',
                             reply_markup=keyboard3)
        except (AttributeError, KeyError):
            bot.send_message(message.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
            pass

    if param == 'влажность':
        try:
            city = cities_dict.rus_cities[town.lower()]
            req = requests.get('https://yandex.ru/pogoda/' + str(city))
            html = bs(req.content, 'html.parser')
            humidity = html.select('.fact__props .term__value')[1].text
            bot.send_message(message.chat.id, f'Итак, вот что с влажностью в твоем городе\n'
                                              f'Влажность:{humidity}\n')
            bot.send_message(message.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                              '1 - Узнать температуру\n'
                                              '2 - Узнать наличие осадков\n'
                                              '3 - Узнать скорость и направление ветра\n'
                                              '4 - Узнать влажность воздуха\n'
                                              '5 - Узнать атмосферное давление\n'
                                              '6 - Узнать все сразу\n'
                                              'Или просто введи запрос из 2 слов. Подробности в /help',
                             reply_markup=keyboard3)
        except (AttributeError, KeyError):
            bot.send_message(message.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
            pass

    if param == 'давление':
        try:
            city = cities_dict.rus_cities[town.lower()]
            req = requests.get('https://yandex.ru/pogoda/' + str(city))
            html = bs(req.content, 'html.parser')
            pressure = html.select('.fact__props .term__value')[2].text
            bot.send_message(message.chat.id, f'Итак, вот что с давлением в твоем городе\n'
                                              f'Давление:{pressure}\n')
            bot.send_message(message.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                              '1 - Узнать температуру\n'
                                              '2 - Узнать наличие осадков\n'
                                              '3 - Узнать скорость и направление ветра\n'
                                              '4 - Узнать влажность воздуха\n'
                                              '5 - Узнать атмосферное давление\n'
                                              '6 - Узнать все сразу\n'
                                              'Или просто введи запрос из 2 слов. Подробности в /help',
                             reply_markup=keyboard3)
        except (AttributeError, KeyError):
            bot.send_message(message.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
            pass


def send_message_6(message_6):
    '''
    Функция, производящая парсинг сайта с погодой и выводящая найденную информацию
    Номер функции соответствует номеру запроса с интерактивной клавиаутуры
    '''
    try:
        city = cities_dict.rus_cities[message_6.text.lower()]
        req = requests.get('https://yandex.ru/pogoda/' + str(city))
        html = bs(req.content, 'html.parser')
        current_temp = html.select('.content__row .temp__value')[1].text
        feel_temp = html.select('.term__value .temp__value')[1].text
        wind = html.select('.fact__props .term__value')[0].text
        humidity = html.select('.fact__props .term__value')[1].text
        pressure = html.select('.fact__props .term__value')[2].text
        state = html.select('.link__feelings .link__condition')[0].text
        bot.send_message(message_6.chat.id, f'Итак, вот какая погода в твоем городе\n'
                                            f'Город:{message_6.text}\n'
                                            f'Текущая температура:{current_temp}\n'
                                            f'Ощущается как:{feel_temp}\n'
                                            f'{state}\n'
                                            f'Ветер:{wind}\n'
                                            f'Влажность:{humidity}\n'
                                            f'Давление:{pressure}')

        bot.send_message(message_6.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                            '1 - Узнать температуру\n'
                                            '2 - Узнать наличие осадков\n'
                                            '3 - Узнать скорость и направление ветра\n'
                                            '4 - Узнать влажность воздуха\n'
                                            '5 - Узнать атмосферное давление\n'
                                            '6 - Узнать все сразу\n'
                                            'Или просто введи запрос из 2 слов. Подробности в /help',
                         reply_markup=keyboard3)
    except (AttributeError, KeyError):
        bot.send_message(message_6.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
        pass


def send_message_1(message_1):
    '''
        Функция, производящая парсинг сайта с погодой и выводящая найденную информацию
        Номер функции соответствует номеру запроса с интерактивной клавиаутуры
    '''
    try:
        city = cities_dict.rus_cities[message_1.text.lower()]
        req = requests.get('https://yandex.ru/pogoda/' + str(city))
        html = bs(req.content, 'html.parser')
        current_temp = html.select('.content__row .temp__value')[1].text
        feel_temp = html.select('.term__value .temp__value')[1].text
        bot.send_message(message_1.chat.id, f'Итак, вот что с температурой в твоем городе\n'
                                            f'Город:{message_1.text}\n'
                                            f'Текущая температура:{current_temp}\n'
                                            f'Ощущается как:{feel_temp}\n')
        bot.send_message(message_1.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                            '1 - Узнать температуру\n'
                                            '2 - Узнать наличие осадков\n'
                                            '3 - Узнать скорость и направление ветра\n'
                                            '4 - Узнать влажность воздуха\n'
                                            '5 - Узнать атмосферное давление\n'
                                            '6 - Узнать все сразу\n'
                                            'Или просто введи запрос из 2 слов. Подробности в /help',
                         reply_markup=keyboard3)
    except (AttributeError, KeyError):
        bot.send_message(message_1.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
        pass


def send_message_2(message_2):
    '''
        Функция, производящая парсинг сайта с погодой и выводящая найденную информацию
        Номер функции соответствует номеру запроса с интерактивной клавиаутуры
    '''
    try:
        city = cities_dict.rus_cities[message_2.text.lower()]
        req = requests.get('https://yandex.ru/pogoda/' + str(city))
        html = bs(req.content, 'html.parser')
        state = html.select('.link__feelings .link__condition')[0].text
        bot.send_message(message_2.chat.id, f'Итак, вот что с осадками в твоем городе\n'
                                            f'{state}\n')
        bot.send_message(message_2.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                            '1 - Узнать температуру\n'
                                            '2 - Узнать наличие осадков\n'
                                            '3 - Узнать скорость и направление ветра\n'
                                            '4 - Узнать влажность воздуха\n'
                                            '5 - Узнать атмосферное давление\n'
                                            '6 - Узнать все сразу\n'
                                            'Или просто введи запрос из 2 слов. Подробности в /help',
                         reply_markup=keyboard3)
    except (AttributeError, KeyError):
        bot.send_message(message_2.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
        pass


def send_message_3(message_3):
    '''
        Функция, производящая парсинг сайта с погодой и выводящая найденную информацию
        Номер функции соответствует номеру запроса с интерактивной клавиаутуры
    '''
    try:
        city = cities_dict.rus_cities[message_3.text.lower()]
        req = requests.get('https://yandex.ru/pogoda/' + str(city))
        html = bs(req.content, 'html.parser')
        wind = html.select('.fact__props .term__value')[0].text
        bot.send_message(message_3.chat.id, f'Итак, вот что с ветром в твоем городе\n'
                                            f'Ветер:{wind}\n')
        bot.send_message(message_3.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                            '1 - Узнать температуру\n'
                                            '2 - Узнать наличие осадков\n'
                                            '3 - Узнать скорость и направление ветра\n'
                                            '4 - Узнать влажность воздуха\n'
                                            '5 - Узнать атмосферное давление\n'
                                            '6 - Узнать все сразу\n'
                                            'Или просто введи запрос из 2 слов. Подробности в /help',
                         reply_markup=keyboard3)
    except (AttributeError, KeyError):
        bot.send_message(message_3.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
        pass


def send_message_4(message_4):
    '''
        Функция, производящая парсинг сайта с погодой и выводящая найденную информацию
        Номер функции соответствует номеру запроса с интерактивной клавиаутуры
    '''
    try:
        city = cities_dict.rus_cities[message_4.text.lower()]
        req = requests.get('https://yandex.ru/pogoda/' + str(city))
        html = bs(req.content, 'html.parser')
        humidity = html.select('.fact__props .term__value')[1].text
        bot.send_message(message_4.chat.id, f'Итак, вот что с влажностью в твоем городе\n'
                                            f'Влажность:{humidity}\n')
        bot.send_message(message_4.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                            '1 - Узнать температуру\n'
                                            '2 - Узнать наличие осадков\n'
                                            '3 - Узнать скорость и направление ветра\n'
                                            '4 - Узнать влажность воздуха\n'
                                            '5 - Узнать атмосферное давление\n'
                                            '6 - Узнать все сразу\n'
                                            'Или просто введи запрос из 2 слов. Подробности в /help',
                         reply_markup=keyboard3)
    except (AttributeError, KeyError):
        bot.send_message(message_4.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
        pass


def send_message_5(message_5):
    '''
        Функция, производящая парсинг сайта с погодой и выводящая найденную информацию
        Номер функции соответствует номеру запроса с интерактивной клавиаутуры
    '''
    try:
        city = cities_dict.rus_cities[message_5.text.lower()]
        req = requests.get('https://yandex.ru/pogoda/' + str(city))
        html = bs(req.content, 'html.parser')
        pressure = html.select('.fact__props .term__value')[2].text
        bot.send_message(message_5.chat.id, f'Итак, вот что с давлением в твоем городе\n'
                                            f'Давление:{pressure}\n')
        bot.send_message(message_5.chat.id, 'Назови цифру, которая соответствует твоему запросу:\n'
                                            '1 - Узнать температуру\n'
                                            '2 - Узнать наличие осадков\n'
                                            '3 - Узнать скорость и направление ветра\n'
                                            '4 - Узнать влажность воздуха\n'
                                            '5 - Узнать атмосферное давление\n'
                                            '6 - Узнать все сразу\n'
                                            'Или просто введи запрос из 2 слов. Подробности в /help',
                         reply_markup=keyboard3)
    except (AttributeError, KeyError):
        bot.send_message(message_5.chat.id, 'Видимо, твоего города я не знаю, но я еще учусь')
        pass


bot.polling()
