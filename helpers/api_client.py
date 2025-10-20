import requests
import allure
from urls import Urls


class ScooterApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.urls = Urls()

    @allure.step("Создание курьера")
    def create_courier(self, login, password, first_name):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return self.session.post(f"{self.urls.BASE_URL}{self.urls.COURIER_CREATE}", json=payload)

    @allure.step("Логин курьера")
    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        return self.session.post(f"{self.urls.BASE_URL}{self.urls.COURIER_LOGIN}", json=payload)

    @allure.step("Удаление курьера")
    def delete_courier(self, courier_id):
        return self.session.delete(f"{self.urls.BASE_URL}{self.urls.COURIER_DELETE.format(courier_id=courier_id)}")

    @allure.step("Создание заказа")
    def create_order(self, order_data):
        return self.session.post(f"{self.urls.BASE_URL}{self.urls.ORDER_CREATE}", json=order_data)

    @allure.step("Получение списка заказов")
    def get_orders_list(self):
        return self.session.get(f"{self.urls.BASE_URL}{self.urls.ORDERS_LIST}")

    @allure.step("Получение заказа по треку")
    def get_order_by_track(self, track):
        return self.session.get(f"{self.urls.BASE_URL}{self.urls.ORDER_TRACK}", params={"t": track})