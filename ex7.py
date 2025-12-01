import requests

real_methods = ["POST", "GET", "PUT", "DELETE", "PATCH", "HEAD"]
expected_methods = ["POST", "GET", "PUT", "DELETE"]
not_expected_methods = ["HEAD", "PATCH"]

#1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.

response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
response_incorrect = response1.text
code_incorrect = response1.status_code
print(f'1. При запросе без параметра method выводится: "{response1.text}"')
print(f'Код ответа: {response1.status_code}')


#2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.

payload2 = {"method": "HEAD"}

response2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params = payload2 )

response_not_expected = response2.text
code_not_expected = response2.status_code

if response2.text is None or len(response2.text) == 0:
    print('2. При http-запросе не из списка выводится пустая строка')
    print(f'Код ответа: {response2.status_code}')
else:
    print(f'2.При http-запросе не из списка выводится: "{response2.text}"')
    print(f'Код ответа: {response2.status_code}')

#3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.

payload3 = {"method": "GET"}
response3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload3)
response_correct = response3.text
code_correct = response3.status_code
print(f'3. При запросе с правильным значением method выводится: "{response3.text}"')
print(f'Код ответа: {response3.status_code}')

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. Например,
# с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так
# для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

bug_counter = 0
bug_params1 = []
bug_params2 = []

for i in range(len(real_methods)):
    current_method = real_methods[i]

    for payload_method in real_methods:
        payload = {"method": payload_method}
        current_response = ''

        if current_method in not_expected_methods:
            if current_method == "PATCH":
                current_response = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type",data=payload)
            elif current_method == "HEAD":
                current_response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)

            if current_response.text != response_not_expected and current_response.status_code != code_not_expected:
                    bug_counter += 1
                    bug_params1.append(current_method)
                    bug_params2.append(payload_method)
            continue

        if current_method in expected_methods:

            if current_method == "GET":
                current_response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
            elif current_method == "POST":
                current_response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
            elif current_method == "PUT":
                current_response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
            elif current_method == "DELETE":
                current_response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
            if current_method == payload_method and current_response.text != response_correct:
                bug_counter += 1
                bug_params1.append(current_method)
                bug_params2.append(payload_method)
            elif current_method != payload_method and current_response.text != response_incorrect:
                bug_counter += 1
                bug_params1.append(current_method)
                bug_params2.append(payload_method)



response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
if response_get.text != response_incorrect and response_get.status_code != code_incorrect:
    bug_counter += 1
    bug_params1.append("GET")
    bug_params2.append("NO PAYLOAD")

response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
if response_post.text != response_incorrect and response_post.status_code != code_incorrect:
    bug_counter += 1
    bug_params1.append("POST")
    bug_params2.append("NO PAYLOAD")

response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
if response_put.text != response_incorrect and response_put.status_code != code_incorrect:
    bug_counter += 1
    bug_params1.append("PUT")
    bug_params2.append("NO PAYLOAD")

response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
if response_delete.text != response_incorrect and response_delete.status_code != code_incorrect:
    bug_counter += 1
    bug_params1.append("DELETE")
    bug_params2.append("NO PAYLOAD")

print(f'4. Количество ошибок - {bug_counter}')

if bug_counter > 0:
    print('В сочетаниях:')
    for n in range(len(bug_params1)):
        print(f'Метод запроса - {bug_params1[n]}, метод в параметре - {bug_params2[n]}')