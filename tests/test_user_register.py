import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@pytest.fixture
def email():
    return "vinkotov@example.com"


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    missing_params = [
        "password",
        "username",
        "firstName",
        "lastName",
        "email"
    ]

    @allure.description("This test checks that user can be created successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        with allure.step("Create new user"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test checks that user cannot be created with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self, email):
        data = self.prepare_registration_data(email=email)

        with allure.step("Try to create user with existing email"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.description("This test checks that user cannot be created with invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_invalid_email(self, email):
        data = self.prepare_registration_data(email="vinkotov.example.com")

        with allure.step("Try to create user with invalid email"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('missing_param', missing_params)
    @allure.description("This test checks that user cannot be created with missing required parameters")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_missing_param(self, missing_param, email):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        data.pop(missing_param, None)

        with allure.step(f"Try to create user with missing parameter: {missing_param}"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_param}"

    @allure.description("This test checks that user cannot be created with too short username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_short_name(self, email):
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        with allure.step("Try to create user with too short username"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short"

    @allure.description("This test checks that user cannot be created with too long username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_long_name(self, email):
        data = {
            'password': '123',
            'username': 'learnqa'*50,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        with allure.step("Try to create user with too long username"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long"
