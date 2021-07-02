import pandas as pd
import telebot
import mysql.connector
import random
from recsys import *
from telebot import types
import random

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123qwe",
  port='3306',
  database='recsys'
)

cold_start_list = ['Madagascar',
"Pirates of the Caribbean: Dead Man's Chest",
'Iron Man',
'Cars',
'Spider-Man 2',
'Titanic',
"Harry Potter and the Philosopher's Stone",
'The Devil Wears Prada',
'Catch Me If You Can',
'The Prestige',
'Finding Nemo',
'Men in Black II',
'Monsters, Inc',
'Pirates of the Caribbean: The Curse of the Black Pearl',
'Ice Age: The Meltdown',
'Taxi 3',
'Astérix aux Jeux Olympiques',
'Ghost Rider',
'Harry Potter and the Prisoner of Azkaban',
'Night at the Museum',
'In Time',
'Taxi 4',
'Kill Bill: Vol. 1',
'The Lord of the Rings: The Return of the King',
'Batman Begins',
'X-Men Origins: Wolverine',
'Transformers: Revenge of the Fallen',
'The Matrix Revolutions',
"Ocean's Twelve",
'Kill Bill: Vol. 2',
'Star Wars: Episode II - Attack of the Clones',
'Terminator 3: Rise of the Machines',
'Star Wars: Episode III - Revenge of the Sith',
'National Treasure',
'American Pie 2',
'Silent Hill',
'The Chronicles of Narnia: Prince Caspian',
'War of the Worlds',
'Aliens vs Predator: Requiem',
'The Terminal',
'8 Mile',
'Rocky Balboa',
'The Departed',
'Hitman',
'The Aviator',
'The Wedding Planner']
mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE recsys")
# mycursor.execute('SELECT * FROM sql_100 WHERE userId=1327')
# mycursor.fetchall()
# df1 = pd.DataFrame(mycursor.fetchall())
# df1.columns=[x[0] for x in mycursor.description ]
# print(df1)

bot = telebot.TeleBot("1705637728:AAHNOLbvEJJ73IoazNgmkVWJwVU7wWKhgcQ")
user_data = {}
kb_start = types.ReplyKeyboardMarkup(True, True)
kb_start.row('/start')
kb2 = types.ReplyKeyboardMarkup(True)
kb2.row('1', '2', '3')
kb2.row('4', '5', 'Не смотрел(а)')
main_kb = types.ReplyKeyboardMarkup(True)
main_kb.row('Выставить оценку')
main_kb.row('Получить рекомендации')
main_kb.row('Посмотреть оцененные фильмы')
main_kb.row('/help')

@bot.message_handler(commands=['start', 'text'])
def send_welcome(message):
    flag = 0
    mycursor.execute('SELECT userId, real_name FROM users;')
    result = mycursor.fetchall()
    for row in result:
        if message.from_user.id == row[0]:
            flag = 1
            bot.send_message(message.chat.id, f'Привет, {row[1]}')
            msg = bot.send_message(message.chat.id, 'Выбери действие', reply_markup=main_kb)
            bot.register_next_step_handler(msg, main_buttons)
            break
    if flag != 1:
        msg = bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
        bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        global top_n
        cold_kb = types.ReplyKeyboardMarkup(True, True)
        cold_kb.row('Готов!')
        user_id = message.from_user.id
        sql = 'INSERT INTO users (userId, real_name) VALUES (%u, %s)'
        mycursor.execute('INSERT INTO users (userId, real_name) VALUES (%s, %s)', (user_id, message.text))
        mydb.commit()
        bot.reply_to(message, 'Приятно познакомиться! Так как ты новый пользователь, мне необходимо понять, что тебе нравится,'
                                  'поэтому я дам тебе оценить несколько фильмов. Готов?', reply_markup=cold_kb)
        print(mycursor.rowcount, "record inserted.")
        bot.register_next_step_handler(message, cold_start)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

def cold_start(message):
    global film, cold_start_list
    mycursor.execute('SELECT * FROM movie_info;')
    result = mycursor.fetchall()
    film = random.choice(cold_start_list)
    msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
    bot.register_next_step_handler(msg, first_rating)

def first_rating(message):
    global cold_start_list, film
    if message.text == 'Не смотрел(а)':
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, first_rating)
    else:
        mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                        'VALUES (%s, %s, %s, %s);',
                         (message.from_user.id, df_100.loc[df_100['title'] == film].values[0][2],
                                                     int(message.text), film))
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, second_rating)


def second_rating(message):
    global cold_start_list, film
    if message.text == 'Не смотрел(а)':
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, second_rating)
    else:
        mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                         'VALUES (%s, %s, %s, %s);',
                         (message.from_user.id, df_100.loc[df_100['title'] == film].values[0][2],
                          int(message.text), film))
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, third_rating)

def third_rating(message):
    global cold_start_list, film
    if message.text == 'Не смотрел(а)':
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, third_rating)
    else:
        mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                        'VALUES (%s, %s, %s, %s);', (message.from_user.id, df_100.loc[df_100['title'] == film].values[0][2],
                                                     int(message.text), film))
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, fourth_rating)


def fourth_rating(message):
    global cold_start_list, film
    if message.text == 'Не смотрел(а)':
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, fourth_rating)
    else:
        mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                        'VALUES (%s, %s, %s, %s);', (message.from_user.id, df_100.loc[df_100['title'] == film].values[0][2],
                                                     int(message.text), film))
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, fifth_rating)


def fifth_rating(message):
    global cold_start_list, film
    if message.text == 'Не смотрел(а)':
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, fifth_rating)
    else:
        mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                         'VALUES (%s, %s, %s, %s);',
                         (message.from_user.id, df_100.loc[df_100['title'] == film].values[0][2],
                          int(message.text), film))
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, last_rating)


def last_rating(message):
    global cold_start_list, film
    if message.text == 'Не смотрел(а)':
        cold_start_list.remove(film)
        film = random.choice(cold_start_list)
        msg = bot.send_message(message.chat.id, f'Фильм: {film}. Твоя оценка?', reply_markup=kb2)
        bot.register_next_step_handler(msg, last_rating)
    else:
        mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                        'VALUES (%s, %s, %s, %s);', (message.from_user.id, df_100.loc[df_100['title'] == film].values[0][2],
                                                     int(message.text), film))
        mydb.commit()
        rec_kb = types.ReplyKeyboardMarkup(True, True)
        rec_kb.row("Рекомендации")
        msg = bot.send_message(message.chat.id, 'Спасибо! Теперь я могу порекомендовать 5 фильмов, '
                                                'которые тебе должны понравиться. Для этого нажми "Рекомендации"',
                               reply_markup=rec_kb)
        bot.register_next_step_handler(msg, display_recs)


def display_recs(message):
    try:
        if int(message.text) in range(1, 11):
            mycursor.execute('SELECT * FROM opros_100;')
            df1 = pd.DataFrame(mycursor.fetchall())
            df1.columns = [x[0] for x in mycursor.description]
            print(df1)
            data1 = Dataset.load_from_df(df1[['userId', 'movieId', 'rating']], reader2)
            trainset__ = data1.build_full_trainset()
            testset__ = trainset__.build_anti_testset()
            pred_list = algo.test(testset__)
            top_n = get_top_n_movies(message.from_user.id, pred_list, int(message.text), df_100)
            rec_list = top_n[:int(message.text)]['title'].tolist()
            rec_string = '\n'.join(rec_list)
            print(top_n[['title', 'rating']])
            bot.send_message(message.chat.id, "Рекомендация для тебя")
            bot.send_message(message.chat.id,
                             f'{rec_string}')
            msg = bot.send_message(message.chat.id, 'Выбери действие', reply_markup=main_kb)
            bot.register_next_step_handler(msg, main_buttons)
        else:
            bot.send_message(message.chat.id, 'Количество фильмов должно быть от 1 до 10.')
            bot.register_next_step_handler(message, display_recs)
    except ValueError:
        bot.send_message(message.chat.id, 'Укажите количество фильмов числом.')
        bot.register_next_step_handler(message, display_recs)



def display_rated(message):
    mycursor.execute('SELECT title, rating FROM opros_100 WHERE userId=%s', (message.from_user.id,))
    result = mycursor.fetchall()
    temp = []
    for i in range(len(result)):
        temp.append(f'{result[i][0]} -- {result[i][1]}')
    rated = '\n'.join(temp)
    bot.send_message(message.chat.id, f'Оцененные фильмы:\n{rated}')
    message = bot.send_message(message.chat.id, 'Выбери действие', reply_markup=main_kb)
    bot.register_next_step_handler(message, main_buttons)

def to_rate(message):
    global result
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Отменяю...')
        bot.send_message(message.chat.id, 'Выбери действие',reply_markup=main_kb)
        bot.register_next_step_handler(message, main_buttons)
    else:
        mycursor.execute("SELECT * FROM movie_info WHERE title LIKE %s", ('%' + message.text,))
        result = mycursor.fetchone()
        print(result)
        if result is None:
            bot.send_message(message.chat.id, 'Такого фильма я не знаю', reply_markup=main_kb)
            bot.register_next_step_handler(message, main_buttons)
        else:
            to_rate_kb = types.ReplyKeyboardMarkup(True)
            to_rate_kb.row('1', '2', '3')
            to_rate_kb.row('4', '5', 'Отмена')
            msg = bot.send_message(message.chat.id, f'Ваша оценка фильму {result[1]}?', reply_markup=to_rate_kb)
            bot.register_next_step_handler(msg, to_rate_db)


def to_rate_db(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Отменяю...')
        bot.send_message(message.chat.id, 'Выбери действие', reply_markup=main_kb)
        bot.register_next_step_handler(message, main_buttons)
    else:
        mycursor.execute('SELECT * FROM opros_100 where userId=%s AND title=%s', (message.from_user.id, result[1]))
        res = mycursor.fetchall()
        if len(res) == 0:
            mycursor.execute('INSERT INTO opros_100 (userId, movieId, rating, title)' \
                         'VALUES (%s, %s, %s, %s);', (message.from_user.id, result[0], int(message.text), result[1]))
            mydb.commit()
            print('recordeed')
            bot.send_message(message.chat.id, 'Оценка поставлена')
            bot.send_message(message.chat.id, 'Выбери действие', reply_markup=main_kb)
            bot.register_next_step_handler(message, main_buttons)
        elif len(res) != 0:
            mycursor.execute('UPDATE opros_100 SET rating=%s WHERE userId=%s AND title=%s',
                             (int(message.text), message.from_user.id, result[1]))
            mydb.commit()
            bot.send_message(message.chat.id, 'Оценка поставлена')
            bot.send_message(message.chat.id, 'Выбери действие', reply_markup=main_kb)
            bot.register_next_step_handler(message, main_buttons)


def main_buttons(message):
    if message.text == 'Получить рекомендации':
        msg = bot.send_message(message.chat.id, 'Какое количество фильмов вам порекомендовать? (до 10 фильмов)')
        bot.register_next_step_handler(message, display_recs)
    elif message.text == 'Посмотреть оцененные фильмы':
        display_rated(message)
    elif message.text == 'Выставить оценку':
        cancel = types.ReplyKeyboardMarkup(True)
        cancel.row('Отмена')
        bot.send_message(message.chat.id, 'Укажите в чате фильм, который хотите оценить',reply_markup=cancel)
        bot.register_next_step_handler(message, to_rate)
    elif message.text == '/help':
        help_message(message)
    else:
        bot.send_message(message.chat.id, 'Такой команды не знаю')
        bot.register_next_step_handler(message, main_buttons)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Это бот, который может рекомендовать фильмы к просмотру. Рекомендации строятся '
                                      'на основе твоих выставленных оценках.\nПри первом использовании будет '
                                      'предложенно оценить 6 фильмов, чтобы система могла ознакомится с твоими'
                                      ' предпочтениями. Оценивание ведется по 5-бальной шкале.\n'
                                      'Есть возможность выставить/изменить оценку. Для этого следует нажать'
                                      ' соответствующую кнопку в интерактивном меню, назвать наименование фильма и '
                                      'указать оценку, которую хотите выставить фильму. Эти оценки в дальнейшем будут '
                                      'учитываться в построении рекомендаций\n'
                                      'Также можно просмотреть какие оценки Вы уже поставили фильмам', reply_markup=main_kb)
    bot.register_next_step_handler(message, main_buttons)






























bot.polling()