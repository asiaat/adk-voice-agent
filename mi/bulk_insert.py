import json
import requests

# === Configuration ===
API_URL = "https://hybridwar.info/bulk_insert.php"  # Replace with your real endpoint
API_KEY = "Zala2025Yane!"                     # Replace with your real key
JSON_FILE = "test1.json"                         # Path to your sample file

# === Load JSON from file ===
with open(JSON_FILE, "r", encoding="utf-8") as f:
    payload = json.load(f)

# === Send POST request ===
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

response = requests.post(API_URL, headers=headers, json=payload)

# === Print result ===
print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw Response:", response.text)
