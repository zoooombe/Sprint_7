class Urls:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

    # Courier endpoints
    COURIER_CREATE = "/courier"
    COURIER_LOGIN = "/courier/login"
    COURIER_DELETE = "/courier/{courier_id}"

    # Order endpoints
    ORDER_CREATE = "/orders"
    ORDERS_LIST = "/orders"
    ORDER_TRACK = "/orders/track"