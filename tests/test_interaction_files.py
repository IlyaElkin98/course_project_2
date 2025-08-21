import unittest
from unittest.mock import mock_open, patch
import json
from src.interaction_files import work_with_json

class TestWorkWithJson(unittest.TestCase):
    def setUp(self):
        self.filename = "test_vacancies.json"
        self.worker = work_with_json(self.filename)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "Python Developer"}]')
    def test_get_data_success(self, mock_file):
        data = self.worker.get_data()
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["name"], "Python Developer")
        mock_file.assert_called_once_with(self.filename, "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_data_file_not_found(self, mock_file):
        data = self.worker.get_data()
        self.assertEqual(data, [])
        mock_file.assert_called_once_with(self.filename, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_get_data_json_decode_error(self, mock_file):

        # json.load вызовет JSONDecodeError, нужно замокать
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
            data = self.worker.get_data()
            self.assertEqual(data, [])
        mock_file.assert_called_once_with(self.filename, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_addition_data_new_vacancy(self, mock_file):
        vacancy = {"name": "New Vacancy"}

        # Замокать get_data чтобы вернуть пустой список
        with patch.object(self.worker, "get_data", return_value=[]):
            with patch("json.dump") as mock_json_dump:
                self.worker.addition_data(vacancy)
                mock_json_dump.assert_called_once()
                args = mock_json_dump.call_args[0][0]
                self.assertIn(vacancy, args)
        mock_file.assert_called()

    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "Existing Vacancy"}]')
    def test_addition_data_duplicate_vacancy(self, mock_file):
        vacancy = {"name": "Existing Vacancy"}

        # Замокать get_data чтобы вернуть список с уже существующей вакансией
        with patch.object(self.worker, "get_data", return_value=[vacancy]):
            with patch("json.dump") as mock_json_dump:
                self.worker.addition_data(vacancy)
                mock_json_dump.assert_not_called()
        mock_file.assert_not_called()  # не должно открываться для записи

    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "Vac1"}, {"name": "Vac2"}]')
    def test_del_data(self, mock_file):
        initial_data = [{"name": "Vac1"}, {"name": "Vac2"}]
        with patch.object(self.worker, "get_data", return_value=initial_data):
            with patch("json.dump") as mock_json_dump:
                self.worker.del_data("name", "Vac1")
                mock_json_dump.assert_called_once()
                written_data = mock_json_dump.call_args[0][0]
                self.assertNotIn({"name": "Vac1"}, written_data)
                self.assertIn({"name": "Vac2"}, written_data)
        mock_file.assert_called()

if __name__ == "__main__":
    unittest.main()