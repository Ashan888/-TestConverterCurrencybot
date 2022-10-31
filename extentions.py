import json
import requests
from config import keys


class ExchangeException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote = quote.lower()
        base = base.lower()  # Перевод валют в нижний регистр позволяет писать их с большими буквами
        if quote == base:
            raise ExchangeException(
                f'Нельзя перевести одинаковые валюты {base}.')  # зачем же переводить одинаковые валюты?

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Не смог обработать валюту1 {quote}')  # при некорректном значении

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Не смог обработать валюту2 {base}')  # при некорректном значении

        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ExchangeException(f'Не смог обработать количество {amount}')  # при некорректном значении

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round((json.loads(r.content)[keys[base]] * amount), 2)  #высчитывает кол-во искомой валюты с округлением
        return total_base