import requests

response = requests.get('http://127.0.0.1:8080/drinks/2')
print(response.json())