import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from dotenv import load_dotenv
from src.extra_function import convert_salary, MyCustomError


class MyCustomError(Exception):
    """Пользовательское исключение"""
    pass


def convert_salary(convert_numb: float, currency: str) -> float:
    """Функция, которая конвертирует сумму транзакции в рубли."""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise MyCustomError("API_KEY не задан в переменном окружении.")
    headers = {"apikey": api_key}
    amount = convert_numb
    conv_from = currency
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={conv_from}&amount={amount}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise MyCustomError(f"Ошибка запроса API {response.status_code}")
    result = response.json()
    if "result" not in result:
        raise MyCustomError("Результат преобразования не найден в ответе API.")
    return result["result"]


class TestConvertSalary(unittest.TestCase):

    @patch("src.extra_function.load_dotenv")
    @patch("src.extra_function.os.getenv")
    @patch("src.extra_function.requests.get")
    def test_successful_conversion(self, mock_get, mock_getenv, mock_load_dotenv):

        mock_load_dotenv.return_value = None
        mock_getenv.return_value = "fake_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 123.45}
        mock_get.return_value = mock_response

        result = convert_salary(100, "USD")
        self.assertEqual(result, 123.45)
        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        self.assertIn("from=USD", called_url)
        self.assertIn("amount=100", called_url)

    @patch("src.extra_function.load_dotenv")
    @patch("src.extra_function.os.getenv")
    def test_missing_api_key(self, mock_getenv, mock_load_dotenv):
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = None
        with self.assertRaises(MyCustomError) as context:
            convert_salary(100, "USD")
        self.assertIn("API_KEY не задан", str(context.exception))

    @patch("src.extra_function.load_dotenv")
    @patch("src.extra_function.os.getenv")
    @patch("src.extra_function.requests.get")
    def test_api_response_error(self, mock_get, mock_getenv, mock_load_dotenv):
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = "fake_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 500  # Server error
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        with self.assertRaises(MyCustomError) as context:
            convert_salary(100, "USD")
        self.assertIn("Ошибка запроса API 500", str(context.exception))

    @patch("src.extra_function.load_dotenv")
    @patch("src.extra_function.os.getenv")
    @patch("src.extra_function.requests.get")
    def test_missing_result_in_response(self, mock_get, mock_getenv, mock_load_dotenv):
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = "fake_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # No 'result' key
        mock_get.return_value = mock_response
        with self.assertRaises(MyCustomError) as context:
            convert_salary(100, "USD")
        self.assertIn("Результат преобразования не найден", str(context.exception))


if __name__ == "__main__":
    unittest.main()