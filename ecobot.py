import telebot
import random
import requests
from bs4 import BeautifulSoup
TOKEN = 'ВАШ_ТОКЕН_БОТА'
bot = telebot.TeleBot(TOKEN)

API_KEY = 'ВАШ_ТОКЕН_OpenWeatherMap'
CITY = 'Moscow'


facts = [
    '🌍 Средняя температура Земли выросла на 1,1 градусов за последние 100 лет.',
    'Ледники Гренландии теряют 280 миллиардов тонн льда каждый год.',
    '🌊 За последние 50 лет уровень моря поднялся на 20 см.',
    '🔥 2020 год стал одним из самых жарких в истории наблюдений.',
    '🌾 Изменение климата влияет на урожай и продовольственную безопасность.',
    'Частота и сила ураганов и штормов увеличивается.',
    '🔥 Арктика нагревается почти в два раза быстрее, чем остальная Земля.',
    '🐧 Из-за таяния льдов страдают животные: пингвины и белые медведи.',
    '💧 Засухи становятся более частыми и продолжительными.',
    '🌱 Деревья поглощают CO2, поэтому вырубка лесов усиливает потепление.'
]

soveti = [
    '💡 Выключай свет, когда уходишь из комнаты.',
    'Пользуйся общественным транспортом вместо машины, когда это возможно',
    '♻️ Сортируй мусор: бумагу, пластик, стекло.',
    '🥤 Используй многоразовую бутылку вместо пластиковой.',
    '🌿 Сажай деревья или ухаживай за растениями дома.',
    '🛍️ Используй сумки многоразового использования.',
    '🚶 Ходи пешком или на велосипеде, когда это возможно.',
    '💧 Экономь воду — не оставляй кран открытым.',
    '🔌 Выключай лишние электроприборы и зарядки из сети.'
]


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        'Привет! Я EcoHelper 🌍\n'
        'Напиши /help чтобы узнать команды.'
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
        '📌 Команды:\n'
        '📖 /fact — случайный факт\n'
        '💡 /sovet — полезный совет\n'
        '☁️ /co2 — калькулятор углеродного следа\n'
        '📰 news - Свежие новости об экологии'
        '🚗💨 /weather — погода в Москве\n'
        '📖 /help — список команд'
    )

@bot.message_handler(commands=['fact'])
def send_fact(message):
    bot.reply_to(message, random.choice(facts))

@bot.message_handler(commands=['news'])
def eco_news(message):
    url = 'https://ria.ru/ecology/  '
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")

    temp = bs.find_all('a', class_='list-item__title color-font-hover-only', limit=5)
    text = ""
    for news in temp:
        novosti = news.get_text()
        link = news.get('href')
        text += f"🌿 {novosti}\n🔗 {link}\n"

    bot.reply_to(message, text)
@bot.message_handler(commands=['sovet'])
def send_advice(message):
    bot.send_message(message.chat.id, random.choice(soveti))

@bot.message_handler(commands=['co2'])
def co2_start(message):
    bot.reply_to(message, 'Сколько км ты проехал на машине? 🚗')
    bot.register_next_step_handler(message, calc_co2)

def calc_co2(message):
    try:
        km = float(message.text)
        co2 = km * 0.12
        bot.reply_to(message, f'Поездка на {km} км примерно равна {co2} кг углекислого газа')
    except:
        bot.reply_to(message, 'Попробуй еще раз, но напиши число, например 15')

@bot.message_handler(commands=['weather'])
def weather(message):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url).json()

    try:
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        wind_speed = response['wind']['speed']
        gust = response['wind']['gust']
        humidity = response['main']['humidity']

        bot.reply_to(message,
            f'Погода в Москве:\n'
            f'Температура: {temp}°C\n'
            f'Погода: {desc}\n'
            f'Скорость ветра: {wind_speed}м/с, порывы ветра до {gust}м/с\n'
            f'Влажность: {humidity}%'

        )
    except:
        bot.reply_to(message, 'Не удалось получить погоду 😔')


bot.polling()
