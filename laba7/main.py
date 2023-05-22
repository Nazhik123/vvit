import telebot
from telebot import types
import datetime
def get_date():
    starting_date = datetime.date(2023, 4, 24)
    current_datetime = datetime.datetime.now().date()
    passed_days = (current_datetime - starting_date).days
    if 0 <= (passed_days % 14) <= 6:
        week = 'Нечётная'
    elif 7 <= (passed_days % 14) <= 13:
        week = 'Чётная'
    return week

import psycopg2
conn = psycopg2.connect(database="postgres", user="postgres",
    password="paketik123", host="localhost", port=5432)
cursor = conn.cursor()

token = "6016577093:AAEdgRQxAj4KeEHMgTBNBbK3tUd6k7ftSXU"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Узнать о МТУСИ", "/help", 'Расписание')
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте, я бот с рассписанием. Я могу вывести ссылку на офф. сайт МТУСИ с помощью кнопки "Узнать о МТУСИ", также можно перейти в раздел "Расписание". В нём, с помощью кнопки "Неделя" , можно узнать чётная или нечётная неделя, узнать рассписание на конкретный день недели или вывести расписание на всю неделю.')

@bot.message_handler(content_types=['text'])
def answer(message):
    tek='Текущая'
    sled='Следующая'
    spi=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    if message.text.lower() == "узнать о мтуси":
        bot.send_message(message.chat.id, 'Вам сюда - https://mtuci.ru/')

    elif message.text.lower() == "расписание":
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        pon = types.InlineKeyboardButton(text='Понедельник')
        vto = types.InlineKeyboardButton(text='Вторник')
        sre = types.InlineKeyboardButton(text='Среда')
        che = types.InlineKeyboardButton(text='Четверг')
        pya = types.InlineKeyboardButton(text='Пятница')
        n_ch = types.InlineKeyboardButton(text=f'{tek} неделя')
        n_nch = types.InlineKeyboardButton(text=f'{sled} неделя')
        back = types.InlineKeyboardButton(text='Назад')
        ned = types.InlineKeyboardButton(text='Неделя')
        keyboard1.add(pon, vto)
        keyboard1.add(sre, che)
        keyboard1.add(pya, ned)
        keyboard1.add(n_nch, n_ch, back)
        bot.send_message(message.chat.id, 'Выберите день', reply_markup=keyboard1)

    elif message.text in spi:
        dayy=message.text
        cursor.execute("SELECT timetable.subject, timetable.room_numb, timetable.start_time, teacher.full_name FROM timetable right join teacher on timetable.subject=teacher.subject WHERE day=%s and week=%s ORDER BY timetable.id;", (str(dayy), str(get_date())))
        record = list(cursor.fetchall())
        n=len(record)
        st=''
        for i in range (0,n):
            st=st+f'\n• {record[i][0]}   {record[i][1]}   {record[i][2]}   {record[i][3]}'
        if st == '':
            st = '\nПар нет'
        bot.send_message(message.chat.id, f'{dayy}' f'\n__________________________' f'{st}')
    elif message.text.lower() == "неделя":
        bot.send_message(message.chat.id, f'{get_date()}')

    elif message.text.lower() == "назад":
        start(message)

    elif message.text == f"{tek} неделя" or message.text == f"{sled} неделя":
        fin = ''
        week = get_date()
        if message.text == f"{sled} неделя":
            if week == 'Чётная':
                week = 'Нечётная'
            elif week == 'Нечётная':
                week = 'Чётная'
        for dayy in spi:
            cursor.execute(
                "SELECT timetable.subject, timetable.room_numb, timetable.start_time, teacher.full_name FROM timetable right join teacher on timetable.subject=teacher.subject WHERE day=%s and week=%s ORDER BY timetable.id;",
                (str(dayy), str(week)))
            record = list(cursor.fetchall())
            n = len(record)
            k=len(dayy)
            p='_' * 2 * k + '__'
            r='¯' * 2 * k
            st = ''
            for i in range(0, n):
                st = st + f'\n• {record[i][0]}   {record[i][1]}   {record[i][2]}   {record[i][3]}'
            if st == '':
                st='\nПар нет'
            fin=fin+f'\n{dayy}' f'\n{p}' f'{st}' f'\n{r}'
        bot.send_message(message.chat.id, f'{fin}')
    else:
        bot.send_message(message.chat.id, f'Извините, я вас не понял.')
bot.infinity_polling()