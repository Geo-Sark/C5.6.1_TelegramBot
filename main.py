import telebot
from config import TOKEN, exchanger
from extensions import Convertor, ConvertException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message:telebot.types.Message):
    text = '''Чтобы начать работу, введите команду в формате:\n <имя валюты>, \
<в какую валюту перевести>, <количество переводимой валюты> \n \
Увидеть список доступных валют: \n /values'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:\n'
    text += '\n'.join( f'{i+1}) {key}' for i, key in enumerate(exchanger.keys()))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message:telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        result = Convertor.get_prise(values)
    except ConvertException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, e)
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} -- {result}'
        bot.reply_to(message, text)


bot.polling(non_stop=True, interval=0)