
# from flask import request
import requests

BASE = "http://127.0.0.1:5005/"

data = [

    {"name": "Radioactive", "views": 300000, "likes": 450000},
    {"name": "Birds", "views": 40000, "likes": 250000},
    {"name": "Shots", "views": 60000, "likes": 370000},
    {"name": "Speed the collapse", "views":35000, "likes":75000}

]


# for item in range(len(data)):
#     response = requests.put(BASE + "video/" + str(item), data[item])
#     print(response.json())

# input()

# response = requests.delete(BASE + "video/0")
# print(response)

input()

response = requests.patch(BASE + "video/2", {"name": "Firefly", "views":450000})
print(response.json())
