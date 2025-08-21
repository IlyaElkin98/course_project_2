import unittest
from unittest.mock import patch, MagicMock
import os


from src.extra_function import convert_salary, MyCustomError

class TestEnvVar(unittest.TestCase):

    @patch.dict(os.environ, {"API_KEY": "test_key_value"})
    def test_api_key_env(self):
        api_key = os.getenv("API_KEY")
        self.assertEqual(api_key, "test_key_value")

    @patch.dict(os.environ, {}, clear=True)
    def test_api_key_env_none(self):
        api_key = os.getenv("API_KEY")
        self.assertIsNone(api_key)


def convert_salary(convert_numb: int, currency: int) -> int:
    import requests
    api_key = os.getenv("API_KEY")
    header = {"apikey": api_key}
    amount = convert_numb
    conv_from = currency
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={conv_from}&amount={amount}"
    result = requests.get(url, headers=header).json()
    return result.get("result")

class MyCustomError(Exception):
    pass


class TestConvertSalary(unittest.TestCase):

    @patch("src.extra_function.requests.get")
    @patch.dict(os.environ, {"API_KEY": "test_key"})
    def test_convert_salary_success(self, mock_get):
        # Мокаем ответ requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 12345}
        mock_get.return_value = mock_response

        amount = 100
        currency = "USD"
        result = convert_salary(amount, currency)

        self.assertEqual(result, 12345)
        mock_get.assert_called_once()
        called_url = mock_get.call_args[1]['url'] if 'url' in mock_get.call_args[1] else None
        # Проверяем, что URL сформирован корректно (можно проверить частично)
        self.assertIn("from=USD", mock_get.call_args[0][0])
        self.assertIn("amount=100", mock_get.call_args[0][0])

    @patch.dict(os.environ, {}, clear=True)
    @patch("src.extra_function.requests.get")
    def test_convert_salary_no_api_key(self, mock_get):
        # Проверяем, что при отсутствии API_KEY запрос всё равно выполняется с apikey=None
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 0}
        mock_get.return_value = mock_response

        result = convert_salary(10, "EUR")
        self.assertEqual(result, 0)
        mock_get.assert_called_once()
        headers = mock_get.call_args[1]["headers"]
        self.assertIsNone(headers.get("apikey"))

    def test_custom_error(self):
        with self.assertRaises(MyCustomError):
            raise MyCustomError("Ошибка")


if __name__ == "__main__":
    unittest.main()