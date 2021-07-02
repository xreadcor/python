from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json

updater = Updater(token='1157559531:AAFnSz6KexSk2Wo4frN_jx1w3KAtLDA8oOw')
dispatcher = updater.dispatcher

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Приветствую!')

def textMessage(bot, update):
    request = apiai.ApiAI('6adb493405f74a0d8cbec93a6a78cbc4').text_request()
    request.lang = 'ru'
    request.session_id = 'practice_mpei_bot'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text = 'IDK')

start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
updater.start_polling(clean=True)