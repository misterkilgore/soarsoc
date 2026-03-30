import requests

# ESEMPI DI RICHIESTE GET DA BROWSER (commentate):
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/log?username=mario&esito=successo
# http://127.0.0.1:8000/saluta?nome=Marco
# http://127.0.0.1:8000/greet?name=Alice
# http://127.0.0.1:8000/greet
# http://127.0.0.1:8000/sum?a=5&b=3

BASE_URL = "http://127.0.0.1:8000"

# GET /
response = requests.get(f"{BASE_URL}/")
print("GET /:", response.json())

# GET /log con parametri
response = requests.get(f"{BASE_URL}/log", params={"username": "mario", "esito": "successo"})
print("GET /log:", response.json())

# GET /saluta
response = requests.get(f"{BASE_URL}/saluta", params={"nome": "Marco"})
print("GET /saluta:", response.json())

# GET /greet (con e senza parametro)
response = requests.get(f"{BASE_URL}/greet", params={"name": "Alice"})
print("GET /greet with name:", response.json())

response = requests.get(f"{BASE_URL}/greet")
print("GET /greet default:", response.json())

# GET /sum
response = requests.get(f"{BASE_URL}/sum", params={"a": 5, "b": 3})
print("GET /sum:", response.json())

# POST /log
response = requests.post(f"{BASE_URL}/log", params={"username": "anna", "esito": "fallito"})
print("POST /log:", response.status_code)
