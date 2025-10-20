import pytest
import allure
from helpers.api_client import ScooterApiClient
from data.test_data import TestData


@allure.feature("Создание курьера")
class TestCourierCreation:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        client = ScooterApiClient()
        courier_data = TestData.VALID_COURIER_DATA

        with allure.step("Отправить запрос на создание курьера"):
            response = client.create_courier(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        with allure.step("Проверить код ответа и тело ответа"):
            assert response.status_code == 201
            assert response.json() == TestData.SUCCESS_RESPONSE

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, registered_courier):
        client = ScooterApiClient()
        login = registered_courier["login"]
        password = registered_courier["password"]
        first_name = registered_courier["first_name"]

        with allure.step("Отправить запрос на создание дубликата курьера"):
            response = client.create_courier(login, password, first_name)

        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 409
            assert TestData.USER_EXISTS_MESSAGE in response.json()["message"]

    @pytest.mark.parametrize("courier_data", TestData.INVALID_COURIER_DATA)
    @allure.title("Создание курьера без обязательных полей")
    def test_create_courier_without_required_fields_fails(self, courier_data):
        client = ScooterApiClient()

        with allure.step("Отправить запрос на создание курьера без обязательных полей"):
            response = client.create_courier(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 400
            assert TestData.INSUFFICIENT_DATA_MESSAGE in response.json()["message"]


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, registered_courier):
        client = ScooterApiClient()
        login = registered_courier["login"]
        password = registered_courier["password"]

        with allure.step("Отправить запрос на логин курьера"):
            response = client.login_courier(login, password)

        with allure.step("Проверить код ответа и наличие ID"):
            assert response.status_code == 200
            assert "id" in response.json()

    @pytest.mark.parametrize("login,password", [
        ("", "password"),
        ("login", "")
    ])
    @allure.title("Логин курьера без обязательных полей")
    def test_login_courier_without_required_fields_fails(self, registered_courier, login, password):
        client = ScooterApiClient()
        test_login = registered_courier["login"] if login else ""
        test_password = registered_courier["password"] if password else ""

        with allure.step("Отправить запрос на логин без обязательных полей"):
            response = client.login_courier(test_login, test_password)

        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 400
            assert TestData.INSUFFICIENT_DATA_MESSAGE in response.json()["message"]

    @allure.title("Логин с неверным паролем")
    def test_login_courier_wrong_password_fails(self, registered_courier):
        client = ScooterApiClient()
        login = registered_courier["login"]

        with allure.step("Отправить запрос на логин с неверным паролем"):
            response = client.login_courier(login, "wrong_password")

        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert TestData.ACCOUNT_NOT_FOUND_MESSAGE in response.json()["message"]

    @allure.title("Логин несуществующего курьера")
    def test_login_nonexistent_courier_fails(self):
        client = ScooterApiClient()

        with allure.step("Отправить запрос на логин несуществующего курьера"):
            response = client.login_courier("nonexistent1231231221", "password")

        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert TestData.ACCOUNT_NOT_FOUND_MESSAGE in response.json()["message"]