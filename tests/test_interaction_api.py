import unittest
from unittest.mock import patch, MagicMock
from src.extra_function import MyCustomError
from src.interaction_api import hh_ru

# Подразумевается, что класс hh_ru импортирован из вашего модуля, например:
# from your_module import hh_ru

class TestHhRuAPI(unittest.TestCase):

    def setUp(self):
        self.hh = hh_ru()

    @patch("src.interaction_api.requests.get")
    def test_connect_apy_success(self, mock_get):
        # Мокаем успешный ответ API с двумя страницами
        responses = []

        # Первая страница с 2 вакансиями
        page1 = MagicMock()
        page1.status_code = 200
        page1.text = '{"items": [{"id": 1}, {"id": 2}]}'
        page1.json.return_value = {"items": [{"id": 1}, {"id": 2}]}
        responses.append(page1)

        # Вторая страница с 1 вакансией
        page2 = MagicMock()
        page2.status_code = 200
        page2.text = '{"items": [{"id": 3}]}'
        page2.json.return_value = {"items": [{"id": 3}]}
        responses.append(page2)

        # Третья страница пустая (имитируем, что больше нет вакансий)
        page3 = MagicMock()
        page3.status_code = 200
        page3.text = '{"items": []}'
        page3.json.return_value = {"items": []}
        responses.append(page3)

        # Настройка side_effect для возврата ответов по очереди
        mock_get.side_effect = responses + [responses[-1]] * 18  # Всего 20 страниц

        vacancies = self.hh._connect_apy("python")
        self.assertIsInstance(vacancies, list)
        self.assertGreaterEqual(len(vacancies), 3)  # Должно быть минимум 3 вакансии
        self.assertEqual(vacancies[0]["id"], 1)
        self.assertEqual(vacancies[2]["id"], 3)
        self.assertEqual(self.hh._hh_params_page(), 20)  # Проверяем, что дошли до 20 страницы

    @patch("src.interaction_api.requests.get")
    def test_connect_apy_http_error(self, mock_get):
        response = MagicMock()
        response.status_code = 500
        response.text = "error"
        mock_get.return_value = response

        with self.assertRaises(MyCustomError) as context:
            self.hh._connect_apy("python")
        self.assertIn("Статус: 500", str(context.exception))

    @patch("src.interaction_api.requests.get")
    def test_connect_apy_invalid_json(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.text = "invalid json"
        response.json.side_effect = ValueError()
        mock_get.return_value = response

        with self.assertRaises(MyCustomError) as context:
            self.hh._connect_apy("python")
        self.assertIn("некорректный ответ", str(context.exception))

    @patch("src.interaction_api.requests.get")
    def test_connect_apy_missing_items(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.text = '{"no_items": []}'
        response.json.return_value = {"no_items": []}
        mock_get.return_value = response

        with self.assertRaises(MyCustomError) as context:
            self.hh._connect_apy("python")
        self.assertIn("Ключ 'items' отсутствует", str(context.exception))

    @patch("src.interaction_api.requests.get")
    def test_connect_apy_empty_response(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.text = ''
        mock_get.return_value = response

        with self.assertRaises(MyCustomError) as context:
            self.hh._connect_apy("python")
        self.assertIn("Пустой ответ от сервера", str(context.exception))

    def test_get_vacancies_returns_first(self):
        # Заполним приватный список вакансий вручную
        self.hh._hh_vacancies_set([{"id": 123}, {"id": 456}])
        vacancy = self.hh.get_vacancies()
        self.assertEqual(vacancy, {"id": 123})

# Вспомогательные методы для доступа к приватным атрибутам (если нет property)
def _hh_params_page(self):
    return self._hh_ru__params.get("page")

def _hh_vacancies_set(self, vacancies):
    self._hh_ru__vacancies = vacancies

# Добавляем методы в класс hh_ru для теста (т.к. атрибуты приватные)
setattr(hh_ru, "_hh_params_page", _hh_params_page)
setattr(hh_ru, "_hh_vacancies_set", _hh_vacancies_set)

if __name__ == "__main__":
    unittest.main()