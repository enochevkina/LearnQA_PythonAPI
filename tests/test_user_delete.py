import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):

    @allure.description("This test checks that undeletable system user cannot be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_undeletable_user(self):
        email = "vinkotov@example.com"
        password = "1234"
        user_id = "2"

        user_data = self.login_user(email, password)

        with allure.step("Try to delete undeletable system user"):
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

    @allure.description("This test checks that just created user can be successfully deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_just_created_user(self):

        user_data = self.create_and_login_user()

        with allure.step("Delete created user"):
            response = MyRequests.delete(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data["token"]},
                cookies={"auth_sid": user_data["auth_sid"]}
            )

        Assertions.assert_code_status(response, 200)

        with allure.step("Try to get deleted user data"):
            response = MyRequests.get(
                f"/user/{user_data['user_id']}",
                headers={"x-csrf-token": user_data["token"]},
                cookies={"auth_sid": user_data["auth_sid"]}
            )

        Assertions.assert_code_status(response, 404)
        assert response.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response.content}"

    @allure.description("This test checks that user cannot delete another user's account")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_delete_user_as_different_user(self):

        user_data_1 = self.create_and_login_user()
        user_data_2 = self.create_and_login_user()

        with allure.step("Try to delete first user using second user's credentials"):
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
