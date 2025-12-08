import requests
import pytest

response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
print(response.cookies)

class TestHomeworkCookie:

    @pytest.fixture(autouse=True)
    def setup(self):
        response1 = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        print(response1.cookies)

        assert "HomeWork" in response1.cookies, 'Homework cookie is not present'

        self.cookie1 = response1.cookies.get('HomeWork')


    def test_homework_cookie(self):

        response2 = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        cookie2 = response2.cookies.get('HomeWork')

        assert cookie2 == self.cookie1, "Cookie values are not equal"
