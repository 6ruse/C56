import requests
import json
from config import keys
import telebot

class ConvertionException(Exception):
    pass

class CryptoConverter:
    quote: str
    base: str
    amount: str

    def __int__(self, quote="", base="", amount=""):
        self.quote= quote
        self.base= base
        self.amount= amount

    # @staticmethod
    def convert(self, message: telebot.types.Message):
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')

        if len(values) > 3:
            raise ConvertionException('Слишком мало параметров')

        self.quote, self.base, self.amount = values

        if self.quote == self.base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты: {self.base}.')

        try:
            quote_ticker = keys[self.quote]
        except KeyError:
            raise ConvertionException(f'Не удалось найти валюту: {self.quote}.')

        try:
            base_ticker = keys[self.base]
        except KeyError:
            raise ConvertionException(f'Не удалось найти валюту: {self.base}.')

        try:
            self.amount = float(self.amount)
        except ValueError:
            raise ConvertionException(f'Не удалось получить количество {self.amount}')

class Cryptocompare:
    @staticmethod
    def get_price(quote: str, base: str, amount: float, ):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        if r.status_code == 200:
            total_base = json.loads(r.content)[keys[base]]
            return f'цена {amount} {quote} в {base} - {total_base}'
        else:
            return 'Возникла ошибка на сервере cryptocompare.com'
