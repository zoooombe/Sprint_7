import pytest
import allure
from helpers.api_client import ScooterApiClient
from data.test_data import TestData


@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order_with_different_colors(self, color):
        client = ScooterApiClient()
        order_data = TestData.ORDER_DATA.copy()

        if color is not None:
            order_data["color"] = color

        with allure.step("Отправить запрос на создание заказа"):
            response = client.create_order(order_data)

        with allure.step("Проверить код ответа и наличие трека"):
            assert response.status_code == 201
            assert "track" in response.json()

    @allure.title("Создание заказа с обязательными полями")
    def test_create_order_required_fields(self):
        client = ScooterApiClient()
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Пушкина, д. 10",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 5,
            "deliveryDate": "2023-12-15"
        }

        with allure.step("Отправить запрос на создание заказа с обязательными полями"):
            response = client.create_order(order_data)

        with allure.step("Проверить код ответа и наличие трека"):
            assert response.status_code == 201
            assert "track" in response.json()

@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        client = ScooterApiClient()

        with allure.step("Отправить запрос на получение списка заказов"):
            response = client.get_orders_list()

        with allure.step("Проверить код ответа и структуру ответа"):
            assert response.status_code == 200
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)

    @allure.title("Получение заказа по треку")
    def test_get_order_by_track(self, order_track):
        client = ScooterApiClient()

        with allure.step("Отправить запрос на получение заказа по треку"):
            response = client.get_order_by_track(order_track)

        with allure.step("Проверить код ответа и данные заказа"):
            assert response.status_code == 200
            assert "order" in response.json()
            assert response.json()["order"]["track"] == order_track

    @allure.title("Получение заказа по несуществующему треку")
    def test_get_order_by_nonexistent_track_fails(self):
        client = ScooterApiClient()

        with allure.step("Отправить запрос на получение заказа по несуществующему треку"):
            response = client.get_order_by_track(999999)

        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert "Заказ не найден" in response.json()["message"]