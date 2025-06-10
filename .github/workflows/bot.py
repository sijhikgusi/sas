import telebot
import random
from telebot import types

TOKEN = "8023700865:AAHpZVbXpKG5ElWYYjn_k-2yzNrKSMIrqg0"  
bot = telebot.TeleBot(TOKEN)

FACTS = [
    "Коты спят 70% жизни 😴",
    "Python назван в честь комедийного шоу 🎭",
    "Сердце кита бьется 9 раз в минуту 💙"
]

WEATHER = {
    "москва": "☀️ +22°C, солнечно",
    "сочи": "🌊 +28°C, жара",
    "спб": "🌧 +18°C, дождь",
    "хабаровск" :"🌧 +18°C, дождь"
}
MOODS = {
    "happy": {
        "state": "😊 Радостный",
        "phrases": ["Отлично!", "Я счастлив!", "Всё прекрасно!"]
    },
    "neutral": {
        "state": "😐 Нейтральный", 
        "phrases": ["Нормально", "Всё как обычно", "Ничего нового"]
    },
    "sad": {
        "state": "😢 Грустный",
        "phrases": ["Не очень", "Мне грустно", "Хочется спать"]
    }
}

current_mood = "neutral" 

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Узнать настроение')
    btn2 = types.KeyboardButton('Изменить настроение')
    markup.add(btn1, btn2)
    bot.reply_to(message, "Привет! Я простой бот. Вот что я умею:\n"
                          "/weather - погода\n"
                          "/fact - интересный факт\n"
                          "/game - играть в камень-ножницы-бумага")
    bot.send_message(
        message.chat.id,
        "Привет! Я бот с настроением.\n"
        "Можешь узнать мое настроение или изменить его!",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == 'Узнать настроение')
def get_mood(message):
    mood = MOODS[current_mood]
    bot.send_message(message.chat.id,f"Мое настроение: {mood['state']}\n"
                     f"Что я думаю: {random.choice(mood['phrases'])}")

@bot.message_handler(func=lambda m: m.text == 'Изменить настроение')
def change_mood(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_happy = types.KeyboardButton('Сделать радостным')
    btn_neutral = types.KeyboardButton('Сделать нейтральным') 
    btn_sad = types.KeyboardButton('Сделать грустным')
    markup.add(btn_happy, btn_neutral, btn_sad)
    
    bot.send_message(
        message.chat.id,
        "Какое настроение мне установить?",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in [
    'Сделать радостным', 
    'Сделать нейтральным',
    'Сделать грустным'
])
def set_mood(message):
    global current_mood
    
    if message.text == 'Сделать радостным':
        current_mood = "happy"
    elif message.text == 'Сделать нейтральным':
        current_mood = "neutral"
    else:
        current_mood = "sad"
    
    mood = MOODS[current_mood]
    bot.send_message(
        message.chat.id,
        f"Мое новое настроение: {mood['state']}!\n"
        f"{random.choice(mood['phrases'])}",
           reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['weather'])
def weather(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for city in WEATHER.keys():
        markup.add(city)
    msg = bot.send_message(message.chat.id, "Выберите город:", reply_markup=markup)
    bot.register_next_step_handler(msg, send_weather)
def send_weather(message):
    city = message.text.lower()
    if city in WEATHER:
        bot.send_message(message.chat.id, WEATHER[city])
    else:
        bot.send_message(message.chat.id, "Город не найден. Попробуйте /weather")
@bot.message_handler(commands=['fact'])
def fact(message):
    bot.send_message(message.chat.id, random.choice(FACTS))

@bot.message_handler(commands=['game'])
def game(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    items = ["Камень", "Ножницы", "Бумага"]
    markup.add(*items)
    
    bot.send_message(message.chat.id, "Выбирайте:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text in ["Камень", "Ножницы", "Бумага"])
def game_result(message):
    user_choice = message.text.lower()
    bot_choice = random.choice(["камень", "ножницы", "бумага"])
    
    result = "Ничья! 🤝"
    if (user_choice == "камень" and bot_choice == "ножницы") or \
       (user_choice == "ножницы" and bot_choice == "бумага") or \
       (user_choice == "бумага" and bot_choice == "камень"):
        result = "Вы победили! 🎉"
    elif user_choice != bot_choice:
        result = "Я выиграл! 💻"
    
    bot.send_message(
        message.chat.id,
        f"Вы: {user_choice}\nЯ: {bot_choice}\n{result}",
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )

print("Бот запущен...")
bot.polling()