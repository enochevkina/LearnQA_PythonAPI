import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@pytest.fixture
def user_data():
    user_data = BaseCase().create_and_login_user()
    return user_data


class TestUserEdit(BaseCase):

    def test_user_edit_just_created_user(self, user_data):
        new_name = "Changed name"

        response = MyRequests.put(
            f"/user/{user_data['user_id']}",
            headers={"x-csrf-token": user_data["token"]},
            cookies={"auth_sid": user_data["auth_sid"]},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 200)

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

    def test_user_edit_user_not_authorised(self, user_data):
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

    def test_user_edit_user_as_different_user(self, user_data):
        # Создание второго пользователя
        user_data_2 = self.create_and_login_user()

        # Попытка изменить данные первого пользователя (user_data) другим пользователем (user_data_2)
        response = MyRequests.put(
            f"/user/{user_data['user_id']}",  # Используем user_data["user_id"]
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

    def test_user_edit_try_invalid_email(self, user_data):
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

    def test_user_edit_try_invalid_first_name(self, user_data):
        response = MyRequests.put(
            f"/user/{user_data['user_id']}",
            headers={"x-csrf-token": user_data["token"]},
            cookies={"auth_sid": user_data["auth_sid"]},
            data={"firstName": "n"}  # Слишком короткое имя
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "The value for field `firstName` is too short",
            f"Unexpected response content {response.content}"
        )
