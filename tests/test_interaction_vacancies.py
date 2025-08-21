import unittest
from unittest.mock import patch
from src.interaction_vacancies import WorkVacancies


class TestWorkVacancies(unittest.TestCase):

    def setUp(self):
        # Пример корректных данных для вакансии
        self.valid_data = {
            "name": "Программист",
            "alternate_url": "http://example.com/job",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "requirement": "Опыт работы от 3 лет"
        }
        self.valid_data_foreign_currency = {
            "name": "Developer",
            "alternate_url": "https://example.com/job",
            "salary": {"from": 3000, "to": 4000, "currency": "USD"},
            "requirement": None
        }

    @patch('src.interaction_vacancies.convert_salary')
    def test_salary_validation_rub(self, mock_convert):
        # Для RUR конвертация не вызывается
        vacancy = WorkVacancies(**self.valid_data)
        avg_salary = vacancy._validate_salary()
        expected_avg = (self.valid_data["salary"]["from"] + self.valid_data["salary"]["to"]) // 2
        self.assertEqual(avg_salary, expected_avg)
        mock_convert.assert_not_called()

    @patch('src.interaction_vacancies.convert_salary')
    def test_salary_validation_foreign_currency(self, mock_convert):
        # Для другой валюты вызывается convert_salary
        mock_convert.return_value = "Converted Salary"
        vacancy = WorkVacancies(**self.valid_data_foreign_currency)
        result = vacancy._validate_salary()
        self.assertEqual(result, "Converted Salary")
        mock_convert()

    def test_name_validation_raises(self):
        bad_data = self.valid_data.copy()
        bad_data["name"] = 123  # Неверный тип
        with self.assertRaises(ValueError):
            WorkVacancies(**bad_data)

    def test_url_validation_raises(self):
        bad_data = self.valid_data.copy()
        bad_data["alternate_url"] = "ftp://example.com"
        with self.assertRaises(ValueError):
            WorkVacancies(**bad_data)

    def test_requirement_default(self):
        data = self.valid_data.copy()
        data["requirement"] = None
        vacancy = WorkVacancies(**data)
        self.assertEqual(vacancy.requirement, "требования не указаны")

    def test_eq_with_same_salary(self):
        vac1 = WorkVacancies(**self.valid_data)
        vac2 = WorkVacancies(**self.valid_data)
        vac1.salary = {"from": 100, "to": 200, "currency": "RUR"}
        vac2.salary = {"from": 100, "to": 200, "currency": "RUR"}
        self.assertTrue(vac1 == vac2)


if __name__ == "__main__":
    unittest.main()