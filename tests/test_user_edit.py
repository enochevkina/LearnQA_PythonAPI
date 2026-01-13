import pytest
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@pytest.fixture
def user_data():
    user_data = BaseCase().create_and_login_user()
    return user_data


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):

    @allure.description("This test checks that just created user can edit own data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_edit_just_created_user(self, user_data):
        new_name = "Changed name"

        with allure.step("Edit user's first name"):
            response = MyRequests.put(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data["token"]},
                cookies={"auth_sid": user_data["auth_sid"]},
                data={"firstName": new_name}
            )

        Assertions.assert_code_status(response, 200)

        with allure.step("Get user data after edit"):
            response = MyRequests.get(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data["token"]},
                cookies={"auth_sid": user_data["auth_sid"]}
            )

        Assertions.assert_json_value_by_name(
            response,
            "firstName",
            new_name,
            "Wrong name after edit"
        )

    @allure.description("This test checks that unauthorized user cannot edit user data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_edit_user_not_authorised(self, user_data):

        with allure.step("Try to edit user data without authorization"):
            response = MyRequests.put(
                f"/user/{user_data['user_id']}",
                data={"firstName": "Changed name"}
            )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Auth token not supplied",
            f"Unexpected response content {response.content}"
        )

    @allure.description("This test checks that user cannot edit another user's data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_edit_user_as_different_user(self, user_data):

        user_data_2 = self.create_and_login_user()

        with allure.step("Try to edit user data using another user's credentials"):
            response = MyRequests.put(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data_2["token"]},
                cookies={"auth_sid": user_data_2["auth_sid"]},
                data={"firstName": "Changed name"}
            )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "This user can only edit their own data.",
            f"Unexpected response content {response.content}"
        )

    @allure.description("This test checks that user cannot set invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_edit_try_invalid_email(self, user_data):

        with allure.step("Try to edit user email with invalid format"):
            response = MyRequests.put(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data["token"]},
                cookies={"auth_sid": user_data["auth_sid"]},
                data={"email": "invalidemailexample.com"}
            )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Invalid email format",
            f"Unexpected response content {response.content}"
        )

    @allure.description("This test checks that user cannot set too short first name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_edit_try_invalid_first_name(self, user_data):

        with allure.step("Try to edit user first name with too short value"):
            response = MyRequests.put(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data["token"]},
                cookies={"auth_sid": user_data["auth_sid"]},
                data={"firstName": "n"}
            )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "The value for field `firstName` is too short",
            f"Unexpected response content {response.content}"
        )
