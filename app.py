import telebot
from config import keys, TOKEN
from extentions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Приветствую! Чтобы начать работу, введите комманду боту в следующем формате:\n<имя валюты>, \
    <в какую валюту перевести>, <количество переводимой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message,text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        asset_id_base, asset_id_quote, amount = values
        total_base = CurrencyConverter.get_price(asset_id_base, asset_id_quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {asset_id_base} в {asset_id_quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
