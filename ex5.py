import json

json_text = "{\"messages\":[{\"message\":\"This is the first message\",\"timestamp\":\"2021-06-04 16:40:53\"},{\"message\":\"And this is a second message\",\"timestamp\":\"2021-06-04 16:41:01\"}]}"
obj = json.loads(json_text)
first_message = obj["messages"][0]
second_message = obj["messages"][1]
print(second_message["message"])