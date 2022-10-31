import telebot
from config import TOKEN, keys
from extentions import ExchangeException, Exchange


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):   # ответ бота на команду /start
    text = 'Привет! Я Бот-Конвертер валют и я могу: \n- Показать список доступных валют через команду /values \n \
- Вывести конвертацию валюты через команду <имя валюты1 (на русском языке)> <в какую валюту2 перевести> <количество переводимой валюты (число в формате 99.99)>\n \
- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):  # ответ бота на команду /help
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n' \
'<имя валюты1 (на русском языке)> <в какую валюту2 перевести> <количество переводимой валюты (число в формате 99.99)>\n' \
'Чтобы увидеть список всех доступных валют, введите команду\n' \
'/values \n' \
'Если бот не отвечает, попробуйте ввести команду еще раз. Сервера телеграмм иногда не отвечают'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):  # ответ бота на команду /values
    text = 'Доступные валюты:'
    for key in keys.keys():                  # цикл сканирует доступные валюты
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:            # если в строке не 3 записи - валюта валюта число
            raise ExchangeException('Введите команду или 3 параметра')
        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')  # ответ бота при некоректном вводе данных
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')  # ответ бота на ошибки внутри скрипта extentions.py
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'  # ответ бота при правильном вводе
        bot.send_message(message.chat.id, text)


bot.infinity_polling(none_stop=True)  # бот работает даже если серверы Телеграмм нет. Остановка только через ctrl+f2
