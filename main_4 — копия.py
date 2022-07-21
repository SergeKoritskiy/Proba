import telebot
from extensions import APIException, Convertor
from config import TOKEN, keys
# import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой надо узнать> \
< имя валюты, в которой надо узнать цену первой валюты > \
< количество первой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        base, sym, amount = values
        result = Convertor.get_price(base, sym, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        stroka = f"Цена {amount} {base} в {sym} : {result}"
        bot.reply_to(message, stroka)


bot.polling(none_stop=True, interval=0)
