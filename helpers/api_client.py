import requests


class ScooterApiClient:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

    def __init__(self):
        self.session = requests.Session()

    def create_courier(self, login, password, first_name):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return self.session.post(f"{self.BASE_URL}/courier", json=payload)

    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        return self.session.post(f"{self.BASE_URL}/courier/login", json=payload)

    def delete_courier(self, courier_id):
        return self.session.delete(f"{self.BASE_URL}/courier/{courier_id}")

    def create_order(self, order_data):
        return self.session.post(f"{self.BASE_URL}/orders", json=order_data)

    def get_orders_list(self):
        return self.session.get(f"{self.BASE_URL}/orders")

    def get_order_by_track(self, track):
        return self.session.get(f"{self.BASE_URL}/orders/track", params={"t": track})