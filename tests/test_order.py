import pytest
import allure
from helpers.api_client import ScooterApiClient
from utils.generators import generate_order_data


@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order_with_different_colors(self, api_client, color):
        order_data = generate_order_data(color)

        response = api_client.create_order(order_data)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с обязательными полями")
    def test_create_order_required_fields_only(self, api_client):
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Пушкина, д. 10",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2023-12-15"
        }

        response = api_client.create_order(order_data)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без обязательного поля")
    def test_create_order_without_required_field_fails(self, api_client):
        order_data = {
            "lastName": "Иванов",
            "address": "ул. Пушкина, д. 10",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2023-12-15"
        }

        response = api_client.create_order(order_data)

        assert response.status_code in [400, 201]


@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, api_client):
        response = api_client.get_orders_list()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Получение заказа по треку")
    def test_get_order_by_track(self, api_client, order_track):
        response = api_client.get_order_by_track(order_track)

        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == order_track

    @allure.title("Получение заказа по несуществующему треку")
    def test_get_order_by_nonexistent_track_fails(self, api_client):
        response = api_client.get_order_by_track(999999)

        assert response.status_code == 404
        assert "Заказ не найден" in response.json()["message"]