import telebot
from config import keys, TOKEN
from utils import ExceptionHandling, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}! Меня зовут CyberPima!\n\
Я умею объективно оценивать картинки и показываю обменные курсы валют.\n\
Я понимаю команды /start, /help \n\
Чтобы посмотреть список валют введите команду /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def handle_start_help(message: telebot.types.Message):
    text = "Чтобы узнать курс валюты введите три значения через пробел:\n<Ваша валюта> <Валюта обмена> <Количество вашей валюты>"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    # есть рубль (quote), покупаю доллар (base) 100 единиц (amount)
    values = message.text.split(" ")

    if len(values) != 3:
        raise ExceptionHandling('Количество параметров должно быть равно трём.')

    quote, base, amount = values

    total_base = CurrencyConverter.convert(quote, base, amount)
    text = f'Текущий курс: {amount} {keys[quote]} = {total_base} {keys[base]}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, "Ха-ха, какая глупая картинка")


bot.polling(none_stop=True)  # команда запуска бота
