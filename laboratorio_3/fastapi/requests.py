import requests
import random
import time

SERVER_URL = "http://127.0.0.1:8000/login"  # URL del server FastAPI

def simulate_login(ip, success=True):
    params = {
        "ip": ip,
        "success": "true" if success else "false"
    }
    response = requests.get(SERVER_URL, params=params)
    print(f"Login {'success' if success else 'failed'} from {ip} -> {response.text}")

if __name__ == "__main__":
    test_ips = ["192.168.1.10", "10.0.0.5", "203.0.113.42"]
    
    # Simula eventi casuali
    for _ in range(20):
        ip = random.choice(test_ips)
        success = random.choice([True, False, False])  # più probabilità di fallimento
        simulate_login(ip, success)
        time.sleep(0.5)
