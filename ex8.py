import requests
import time
import json

# 1) создание задачи:
response1 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
obj1 = json.loads(response1.text)
token = ""
seconds = 0

token_key, seconds_key = "token", "seconds"

if token_key in obj1 and seconds_key in obj1:
    token = obj1[token_key]
    seconds = obj1[seconds_key]
    print(f"Token = {token},", f"seconds = {seconds}")
else:
    print("Error. Token and seconds not found.")

# 2) запрос с token ДО того, как задача готова, проверка правильности поля status:

payload = {"token": token}
response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params = payload)

obj2 = json.loads(response2.text)

status_key, error_key, result_key = "status", "error", "result"

if status_key in obj2:
    if result_key not in obj2:
        print(obj2[status_key])
    else:
        print(obj2[status_key], obj2[result_key])
elif error_key in obj2:
    print(obj2[error_key])
else:
    print(f"Error. No status or error. Response = {response2.text}")

#3) ожидание нужного количества секунд с помощью функции time.sleep():

print(f"Waiting {seconds} seconds...")
time.sleep(seconds)

#4) запрос c token ПОСЛЕ того, как задача готова, проверка правильности поля status и наличия поля result:

payload = {"token": token}
response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params = payload)

obj3 = json.loads(response3.text)

if status_key in obj3:
    if obj3[status_key] == "Job is ready" and result_key in obj3:
        print(f"{obj3[status_key]}, result = {obj3[result_key]}")
    elif obj3[status_key] == "Job is ready" and result_key not in obj3:
        print(f"Error. {obj3[status_key]}, no result.")
    elif obj3[status_key] == "Job is NOT ready" and result_key in obj3:
        print(f"Error. {obj3[status_key]}, result = {obj3[result_key]}.")
    elif obj3[status_key] == "Job is NOT ready" and result_key not in obj3:
        print(f"Error. {obj3[status_key]}.")
elif error_key in obj3:
    print(obj3[error_key])
else:
    print(f"Error. No status or error. Response = {response3.text}")