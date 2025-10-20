import random
import string
import requests


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def generate_order_data(color=None):
    base_data = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Пушкина, д. 10",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": "2023-12-15",
        "comment": "Тестовый заказ"
    }

    if color is not None:
        if isinstance(color, list):
            base_data["color"] = color
        else:
            base_data["color"] = [color]

    return base_data