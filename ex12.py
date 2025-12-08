import requests
import pytest

class TestHomeworkCookie:

    @pytest.fixture(autouse=True)
    def setup(self):
        response1 = requests.get('https://playground.learnqa.ru/api/homework_header')
        print(response1.headers)

        assert "x-secret-homework-header" in response1.headers, 'Homework header is not present'

        self.header1 = response1.headers.get("x-secret-homework-header")

    def test_homework_header(self):

        resposne2 = requests.get('https://playground.learnqa.ru/api/homework_header')
        header2 = resposne2.headers.get("x-secret-homework-header")

        assert header2 == self.header1, 'Header values are different'