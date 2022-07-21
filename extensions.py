import json
import requests
from config import keys


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base: str, sym: str, amount: str):
        if base == sym:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            currency_1 = keys[base]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            currency_2 = keys[sym]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        zapros = f'https://min-api.cryptocompare.com/data/price?fsym={currency_1}&tsyms={currency_2}'
        r = requests.get(zapros)

        resp = json.loads(r.content)
        new_price = resp[currency_2] * amount
        new_price = round(new_price, 3)

        return new_price
