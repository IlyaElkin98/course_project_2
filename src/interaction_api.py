from abc import ABC, abstractmethod

import requests

from src.extra_function import MyCustomError


class HeadHunterAPI(ABC):
    """
    Абстрактный класс для работы с API.

    Класс содержит методы, которые будут реализованы в классах наследниках.

    А именно:
    Абстрактный метод _connect_apy, выполняющий подкючение к api.
    Абстрактный метод get_vacancies, получает вакансии.
    """

    def __init__(self):
        pass

    @abstractmethod
    def _connect_apy(self, keyword):
        """Метод подключения к api"""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Метод получения вакансий"""


class hh_ru(HeadHunterAPI):
    """
    Класс для работы с hh.ru

    Класс для подключения к api и получения вакансий.

    Метод _connect_apy, выполняющий подкючение к api.
    Метод get_vacancies, получает вакансии.
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100, "area": 113}
        self.__vacancies = []
        super().__init__()

    def _connect_apy(self, keyword: str) -> list[dict]:
        """Метод подключения к api"""
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            # Проверка статуса ответа
            if response.status_code != 200:
                raise MyCustomError(
                    f"Ошибка! Запрос не выполнен. Статус: {response.status_code}"
                )
            if response.text:
                try:
                    data = response.json()
                except ValueError:
                    raise MyCustomError(
                        "Ошибка: получен некорректный ответ."
                    )
                # Проверка наличия ключа 'items'
                if "items" not in data:
                    raise MyCustomError("Ключ 'items' отсутствует в ответе.")
                vacancies = data["items"]
                self.__vacancies.extend(vacancies)
            else:
                raise MyCustomError("Пустой ответ от сервера.")
            self.__params["page"] += 1
        return self.__vacancies

    def get_vacancies(self) -> dict:
        """Метод получения вакансий"""
        for vacancy in self.__vacancies:
            return vacancy