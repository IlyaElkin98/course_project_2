from src.extra_function import convert_salary


class WorkVacancies:
    """
    Класс для работы с вакансиями.

    Класс содержит следующие методы:

    Магический метод __eq__ определяет, являются ли два объекта равными.
    Магический метод __le__ определяет, меньше ли или равен self объект other.
    Магический метод __ge__ определяет, больше ли или равен self объект other
    _validate_name, метод валидации name.
    _validate_url, метод валидации url.
    _validate_requirement, метод валидации requirement.
    _validate_salary, метод выводит среднюю заработную плату.
    """

    __slots__ = (
        "name",
        "alternate_url",
        "salary",
        "requirement",
    )

    def __init__(self, name, alternate_url, salary, requirement=""):
        self.name = name
        self.alternate_url = alternate_url
        self.salary = salary
        self.requirement = requirement

        if not isinstance(self.requirement, str):
            if self.requirement is None:
                self.requirement = "требования не указаны"
            else:
                self.requirement = str(self.requirement)
        else:
            self.requirement = self.requirement

        self._validate_name()
        self._validate_url()
        self._validate_salary()

    def __eq__(self, other) -> bool:
        """Метод определяет, являются ли два объекта равными."""
        return self.salary == other.salary

    def __le__(self, other) -> bool:
        """Метод определяет, меньше ли или равен self объект other"""
        return self.salary <= other.salary

    def __ge__(self, other) -> bool:
        """Метод определяет, больше ли или равен self объект other"""
        return self.salary >= other.salary

    def _validate_name(self):
        """Метод валидации name"""
        if not isinstance(self.name, str):
            raise ValueError("name должен быть строкой")

    def _validate_url(self):
        """Метод валидации url"""
        if not isinstance(self.alternate_url, str) or not self.alternate_url.startswith(
            "http"
        ):
            raise ValueError("Некорректный url")

    def _validate_salary(self) -> int | str:
        """Метод валидации salary - выводит среднюю заработную плату"""
        salary_info = self.salary
        if not isinstance(salary_info, dict):
            return "Зарплата не указана"
        currency = salary_info.get("currency")
        if currency not in ["RUR", "RUB"]:
            from_value = salary_info.get("from")
            to_value = salary_info.get("to")
            if from_value is None:
                from_value = 0
            if to_value is None:
                to_value = 0
            result = (from_value + to_value) // 2
            return convert_salary(result, currency)
        else:
            from_value = salary_info.get("from")
            to_value = salary_info.get("to")
            if from_value is None:
                from_value = 0
            if to_value is None:
                to_value = 0
            result = (from_value + to_value) // 2
            return result

