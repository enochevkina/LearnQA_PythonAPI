import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
redirects_number = len(response.history)
print(redirects_number)
print(response.url)