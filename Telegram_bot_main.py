import telebot
import apiai
import json

bot = telebot.TeleBot('1098357830:AAE5VuBOj2a4yhYobr_gfB5Zqh97zTfpDJk')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я тут!')

@bot.message_handler(content_types=['text'])
def send_mes(message):
    request = apiai.ApiAI('a4b7062f9fd347899f272dbe0365c11d')
    request.lang = 'ru'
    request.session_id = 'forecast_practice_bot'
    request.query = message.text
    response = json.loads(request.getresponse().read().decode('utf-8'))
    bot.send_message(response['result']['action'])
    print(message.text)
# def send_mes(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, 'Привет, товарищ!')
#     elif message.text.lower() == 'как дела?':
#         bot.send_message(message.chat.id, 'Все отлично, у Вас как?')
#     elif message.text.lower() in ['хорошо', 'отлично', 'лучше всех']:
#         bot.send_message(message.chat.id, 'Приятно слышать!')
#     elif message.text.lower() == 'пока':
#         bot.send_message(message.chat.id, 'Всего доброго!')

bot.polling()