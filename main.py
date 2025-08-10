from src.interaction_api import hh_ru
from src.interaction_vacancies import WorkVacancies


def user_menu():
    print("Добро пожаловать! Выберите опцию:")
    print("1. Поиск вакансий по ключевому слову")
    print("2. Получить топ N вакансий по зарплате")
    print("3. Найти вакансии с ключевым словом в описании")
    print("4. Выйти")

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Пожалуйста, введите положительное число.")
                continue
            return value
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")

def main():
    api = hh_ru()
    while True:
        user_menu()
        choice = input("Введите номер опции: ").strip()

        if choice == '1':
            keyword = input("Введите поисковый запрос для поиска вакансий: ").strip()
            try:
                vacancies = api._connect_apy(keyword)
                if not vacancies:
                    print("Вакансии не найдены.")
                else:
                    for vac in vacancies:
                        name = vac.get('name', 'Нет названия')
                        url = vac.get('alternate_url', 'Нет ссылки')
                        salary_info = vac.get('salary')
                        requirement_raw = vac.get('snippet', {}).get('requirement')

                        print("Перед созданием вакансии")
                        vacancy_obj = WorkVacancies(
                            name=name,
                            alternate_url=url,
                            salary=salary_info,
                            requirement=requirement_raw
                        )
                        print("Объект создан")

                        salary_display = vacancy_obj._validate_salary()

                        print(f"Вакансия: {name}")
                        print(f"Ссылка: {url}")
                        print(f"Требования: {vacancy_obj.requirement}")  # Используем свойство класса
                        print(f"Зарплата: {salary_display}")
                        print("-" * 40)
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '2':
            N = get_integer_input("Введите количество топ вакансий по зарплате: ")
            keyword = input("Введите поисковый запрос для фильтрации (оставьте пустым для всех): ").strip()
            try:
                vacancies = api._connect_apy(keyword)
                # Создаем список объектов WorkVacancies
                vacancy_objects = []
                for vac in vacancies:
                    name = vac.get('name', 'Нет названия')
                    url = vac.get('alternate_url', 'Нет ссылки')
                    salary_info = vac.get('salary')
                    vacancy_obj = WorkVacancies(name, url, salary_info, requirement="")
                    vacancy_objects.append(vacancy_obj)
                sorted_vacancies = sorted(vacancy_objects, key=lambda v: v.salary if isinstance(v.salary, int) else 0, reverse=True)
                top_vacancies = sorted_vacancies[:N]
                for vac in top_vacancies:
                    print(f"Вакансия: {vac.name}")
                    print(f"Ссылка: {vac.alternate_url}")
                    salary_display = vac._validate_salary()
                    print(f"Зарплата: {salary_display}")
                    print("-" * 40)
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '3':
            keyword_in_desc = input("Введите ключевое слово для поиска в описании вакансии: ").strip().lower()
            keyword_search_results = []
            try:
                vacancies = api._connect_apy("")
                for vac in vacancies:
                    description = vac.get('description', '')
                    if description and keyword_in_desc in description.lower():
                        name = vac.get('name', 'Нет названия')
                        url = vac.get('alternate_url', 'Нет ссылки')
                        salary_info = vac.get('salary')
                        vacancy_obj = WorkVacancies(name, url, salary_info, requirement="")
                        keyword_search_results.append(vacancy_obj)
                if not keyword_search_results:
                    print("Вакансии с указанным ключевым словом в описании не найдены.")
                else:
                    for vac in keyword_search_results:
                        print(f"Вакансия: {vac.name}")
                        print(f"Ссылка: {vac.alternate_url}")
                        salary_display = vac._validate_salary()
                        print(f"Зарплата: {salary_display}")
                        print("-" * 40)
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()