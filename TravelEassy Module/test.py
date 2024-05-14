import requests

response = requests.get("http://127.0.0.1:5500/home.html")
response = response.text

with open("")