import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User get cases")
class TestUserGet(BaseCase):

    @allure.description("This test checks that unauthorized user can see only username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_not_auth(self):

        with allure.step("Get user data without authorization"):
            response = MyRequests.get("/user/2")

        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, unexpected_fields)

    @allure.description("This test checks that authorized user can see all own user data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        with allure.step("Login as user"):
            response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Get user data as same authorized user"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks that authorized user cannot see private data of another user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_auth_as_different_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        with allure.step("Login as user"):
            response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        with allure.step("Get another user's data"):
            response = MyRequests.get(
                "/user/1",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, unexpected_fields)
