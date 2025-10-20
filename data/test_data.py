from utils.generators import generate_random_string


class TestData:
    VALID_COURIER_DATA = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    INVALID_COURIER_DATA = [
        {"login": "", "password": generate_random_string(10), "firstName": generate_random_string(10)},
        {"login": generate_random_string(10), "password": "", "firstName": generate_random_string(10)}
    ]

    ORDER_DATA = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Пушкина, д. 10",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": "2023-12-15",
        "comment": "Тестовый заказ 1"
    }


    SUCCESS_RESPONSE = {"ok": True}
    INSUFFICIENT_DATA_MESSAGE = "Недостаточно данных"
    ACCOUNT_NOT_FOUND_MESSAGE = "Учетная запись не найдена"
    USER_EXISTS_MESSAGE = "Этот логин уже используется"