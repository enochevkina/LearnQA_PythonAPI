import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):

    def test_user_delete_undeletable_user(self):
        # данные пользователя
        email = "vinkotov@example.com"
        password =  "1234"
        user_id = "2"

        #логин под этим пользователем
        user_data = self.login_user(email, password)

        # попытка удаления пользователя, id нам известен из задания
        response = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": user_data["token"]},
            cookies={"auth_sid": user_data["auth_sid"]}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Unexpected response content {response.content}"
        )

    def test_user_delete_just_created_user(self):
        # создание и логин с новым пользователем
        user_data = self.create_and_login_user()

        # удаление пользователя
        response = MyRequests.delete(
            f"/user/{user_data['user_id']}",
            headers={"x-csrf-token": user_data["token"]},
            cookies={"auth_sid": user_data["auth_sid"]}
        )

        Assertions.assert_code_status(response, 200)

        # попытка получения данных пользователя
        response = MyRequests.get(
            f"/user/{user_data['user_id']}",
            headers={"x-csrf-token": user_data["token"]},
            cookies={"auth_sid": user_data["auth_sid"]}
        )

        Assertions.assert_code_status(response, 404)
        assert response.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response.content}"

    def test_user_delete_user_as_different_user(self):

        # создание пользователей и логин
        user_data_1 = self.create_and_login_user()
        user_data_2 = self.create_and_login_user()

        # попытка удаления 1-го пользователя с данными 2-го
        response = MyRequests.delete(
            f"/user/{user_data_1['user_id']}",
            headers={"x-csrf-token": user_data_2["token"]},
            cookies={"auth_sid": user_data_2["auth_sid"]}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "This user can only delete their own account.",
            f"Unexpected response content {response.content}"
        )


