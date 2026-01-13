from requests import Response
import json
import allure

class Assertions:

    @staticmethod
    @allure.step("Assert JSON value by name '{name}' equals expected '{expected_value}'")
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON does not contain {name} key"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    @allure.step("Assert JSON has key '{name}'")
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON does not contain {name} key"

    @staticmethod
    @allure.step("Assert JSON has keys {names}")
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON does not contain {name} key"

    @staticmethod
    @allure.step("Assert JSON does not have key '{name}'")
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response should not contain {name} key. But it's present."

    @staticmethod
    @allure.step("Assert JSON does not have keys {names}")
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name not in response_as_dict, f"Response should not contain {name} key. But it's present."

    @staticmethod
    @allure.step("Assert status code is {expected_status_code}")
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    @allure.step("Assert cookie '{cookie_name}' exists in response")
    def assert_cookie_has_name(response, cookie_name):
        cookies = response.cookies
        assert cookie_name in cookies, f"Cookie with name '{cookie_name}' is missing. All cookies: {cookies}"

    @staticmethod
    @allure.step("Assert header '{header_name}' exists in response")
    def assert_header_has_name(response, header_name):
        headers = response.headers
        assert header_name in headers, f"Header '{header_name}' is missing. All headers: {headers}"
