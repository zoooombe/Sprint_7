import pytest
import allure
from helpers.api_client import ScooterApiClient
from utils.generators import generate_random_string


@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, api_client):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = api_client.create_courier(login, password, first_name)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = api_client.login_courier(login, password)
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            api_client.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, registered_courier, api_client):
        login = registered_courier["login"]
        password = registered_courier["password"]
        first_name = registered_courier["first_name"]

        response = api_client.create_courier(login, password, first_name)

        assert response.status_code == 409
        assert "уже используется" in response.json()["message"]

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login_fails(self, api_client):
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = api_client.create_courier("", password, first_name)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password_fails(self, api_client):
        login = generate_random_string(10)
        first_name = generate_random_string(10)

        response = api_client.create_courier(login, "", first_name)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Создание курьера без имени")
    def test_create_courier_without_first_name_success(self, api_client):
        login = generate_random_string(10)
        password = generate_random_string(10)

        response = api_client.create_courier(login, password, "")

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = api_client.login_courier(login, password)
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            api_client.delete_courier(courier_id)


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, registered_courier, api_client):
        login = registered_courier["login"]
        password = registered_courier["password"]

        response = api_client.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Логин без пароля")
    def test_login_courier_without_password_fails(self, registered_courier, api_client):
        login = registered_courier["login"]

        response = api_client.login_courier(login, "")

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Логин без логина")
    def test_login_courier_without_login_fails(self, registered_courier, api_client):
        password = registered_courier["password"]

        response = api_client.login_courier("", password)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Логин с неверным паролем")
    def test_login_courier_wrong_password_fails(self, registered_courier, api_client):
        login = registered_courier["login"]

        response = api_client.login_courier(login, "wrong_password")

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Логин несуществующего курьера")
    def test_login_nonexistent_courier_fails(self, api_client):
        response = api_client.login_courier("nonexistent1231231221", "password")

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]