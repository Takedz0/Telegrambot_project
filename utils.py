import requests
import json
from config import keys

class ExceptionHandling(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExceptionHandling(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExceptionHandling(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ExceptionHandling(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/c30227f6f740e951c76ac967/latest/{quote_ticker}')
        text = json.loads(r.content)
        total_base = round(text['conversion_rates'][base_ticker] * amount, 2)
        return total_base