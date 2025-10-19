import pytest
import requests
from helpers.api_client import ScooterApiClient
from utils.generators import generate_random_string, register_new_courier_and_return_login_password


@pytest.fixture
def api_client():
    return ScooterApiClient()


@pytest.fixture
def registered_courier():
    courier_data = register_new_courier_and_return_login_password()

    if not courier_data:
        pytest.skip("Не удалось зарегистрировать курьера для теста")

    login, password, first_name = courier_data

    yield {
        "login": login,
        "password": password,
        "first_name": first_name
    }

    client = ScooterApiClient()
    response = client.login_courier(login, password)
    if response.status_code == 200:
        courier_id = response.json()["id"]
        client.delete_courier(courier_id)


@pytest.fixture
def order_track(api_client):
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

    response = api_client.create_order(order_data)
    assert response.status_code == 201
    track = response.json()["track"]

    yield track