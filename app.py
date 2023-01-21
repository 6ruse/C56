import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter, Cryptocompare

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате: \n<имя валюты> \<в какую валюту переваести> \<количество переводимой валюты>' \
           '\nСписок доступных валют : /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        cc = CryptoConverter()
        cc.convert(message)
    except ConvertionException as e:
        bot.reply_to(message, f'Пользовательская ошибка:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду, текст ошибки:\n{e}')
    else:
        text = Cryptocompare.get_price(cc.quote, cc.base, cc.amount)
        bot.reply_to(message, text)

bot.polling();