import requests
import json
from config import exchanger, api_key

class ConvertException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_prise(values):

        if len(values) !=3:
            raise ConvertException('Неверное количество параметров')

        base, quote, amount = values

        if base == quote:
            raise ConvertException(f'Невозможно перевести одинаковые валюты: {base}')

        try:
            base_val = exchanger[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}')

        try:
            quote_val = exchanger[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')

        res = requests.get(f'https://free.currconv.com/api/v7/convert?q={base_val}_{quote_val}&'
                           f'compact=ultra&apiKey={api_key}')

        sale = json.loads(res.content)[f'{base_val}_{quote_val}']

        total = round(sale * amount, 3)

        return total
