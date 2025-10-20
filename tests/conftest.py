import pytest
from helpers.api_client import ScooterApiClient
from utils.generators import generate_random_string


@pytest.fixture
def registered_courier():
    client = ScooterApiClient()

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    response = client.create_courier(login, password, first_name)

    if response.status_code != 201:
        pytest.skip("Не удалось зарегистрировать курьера для теста")

    courier_data = {
        "login": login,
        "password": password,
        "first_name": first_name
    }

    yield courier_data

    login_response = client.login_courier(login, password)
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        client.delete_courier(courier_id)


@pytest.fixture
def order_track():
    client = ScooterApiClient()

    order_data = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "ул. Тестовая, д. 1",
        "metroStation": 1,
        "phone": "+79998887766",
        "rentTime": 3,
        "deliveryDate": "2023-12-20",
        "comment": "Тестовый заказ из фикстуры",
        "color": ["BLACK"]
    }

    response = client.create_order(order_data)
    assert response.status_code == 201
    track = response.json()["track"]

    yield track