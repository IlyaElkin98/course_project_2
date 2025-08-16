import unittest
from unittest.mock import patch
from src.interaction_vacancies import WorkVacancies


class TestWorkVacancies(unittest.TestCase):

    def setUp(self):
        self.valid_salary_rub = {"from": 100000, "to": 200000, "currency": "RUB"}
        self.valid_salary_usd = {"from": 1000, "to": 2000, "currency": "USD"}
        self.invalid_salary = "not a dict"

    def test_validate_name_with_non_string(self):
        with self.assertRaises(ValueError) as context:
            WorkVacancies(123, "http://example.com", self.valid_salary_rub)
        self.assertIn("name должен быть строкой", str(context.exception))

    def test_validate_url_with_invalid_url(self):
        with self.assertRaises(ValueError) as context:
            WorkVacancies("Job Name", "ftp://example.com", self.valid_salary_rub)
        self.assertIn("Некорректный url", str(context.exception))

    def test_requirement_conversion_none(self):
        job = WorkVacancies("Job Name", "http://example.com", self.valid_salary_rub, requirement=None)
        self.assertEqual(job.requirement, "требования не указаны")

    def test_requirement_conversion_non_string(self):
        job = WorkVacancies("Job Name", "http://example.com", self.valid_salary_rub, requirement=123)
        self.assertEqual(job.requirement, "123")

    def test_validate_salary_rub(self):
        job = WorkVacancies("Job Name", "http://example.com", self.valid_salary_rub)
        expected_avg = (self.valid_salary_rub["from"] + self.valid_salary_rub["to"]) // 2
        # _validate_salary возвращает среднюю заработную плату в рублях/RUB
        self.assertEqual(job._validate_salary(), expected_avg)

    @patch("src.interaction_vacancies.convert_salary", return_value=150000)
    def test_validate_salary_other_currency(self, mock_convert_salary):
        job = WorkVacancies("Job Name", "http://example.com", self.valid_salary_usd)
        expected_avg = (self.valid_salary_usd["from"] + self.valid_salary_usd["to"]) // 2
        result = job._validate_salary()
        mock_convert_salary(expected_avg, "USD")
        self.assertEqual(result, 150000)

    def test_validate_salary_not_dict(self):
        job = WorkVacancies("Job Name", "http://example.com", self.invalid_salary)
        self.assertEqual(job._validate_salary(), "Зарплата не указана")


if __name__ == "__main__":
    unittest.main()