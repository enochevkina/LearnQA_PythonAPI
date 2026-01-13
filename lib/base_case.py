from requests import Response
import json
import allure
from datetime import datetime
from lib.my_requests import MyRequests
from lib.assertions import Assertions

class BaseCase:
    @allure.step("Get cookie '{cookie_name}' from response")
    def get_cookie (self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with  name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    @allure.step("Get header '{headers_name}' from response")
    def get_header (self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with  name {headers_name} in the last response"
        return response.headers[headers_name]

    @allure.step("Get JSON value '{name}' from response")
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Ressponse text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON does not contain {name} key"

        return response_as_dict[name]

    @allure.step("Prepare registration data")
    def prepare_registration_data(self, email = None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S") + f"{datetime.now().microsecond:06d}"
            email = f"{base_part}{random_part}@{domain}"
        return  {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    @allure.step("Create new user")
    def create_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        return {
            "user_id": response.json()["id"],
            "email": register_data["email"],
            "password": register_data["password"]
        }

    @allure.step("Login user '{email}'")
    def login_user(self, email, password):

        response = MyRequests.post(
            "/user/login",
            data={"email": email, "password": password}
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_cookie_has_name(response, "auth_sid")
        Assertions.assert_header_has_name(response, "x-csrf-token")

        return {
            "auth_sid": response.cookies["auth_sid"],
            "token": response.headers["x-csrf-token"]
        }

    @allure.step("Create and login new user")
    def create_and_login_user(self):
        user = self.create_user()
        auth = self.login_user(user["email"], user["password"])

        return {**user, **auth}
