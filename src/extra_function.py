import os

import requests
from dotenv import load_dotenv


def convert_salary(convert_numb: int, currency: int) -> int:
    """Функция, которая конвертирует сумму транзакции в рубли."""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    header = {"apikey": api_key}
    amount = convert_numb
    conv_from = currency
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={conv_from}&amount={amount}"
    result = requests.get(url, headers=header).json()
    return result.get("result")


class MyCustomError(Exception):
    """Пользовательское исключение"""

    pass