import requests
import json

# === Configuration ===
API_URL = "https://hybridwar.info/insert_data.php"  # Replace with your actual URL
API_KEY = "Zala2025Yane!"           # Must match what's in your PHP file

# === Example payload ===
payload = {
    "id": 1001,
    "head": "En Afrique, l'Ukraine accélère sa contre-offensive diplomatique",
    "url": "https://www.lepoint.fr/afrique/en-afrique-l-ukraine-accelere-sa-contre-offensive-diplomatique-22-07-2024-2566191_3826.php",
    "locations": "any",
    "authors": "news",
    "datetime": "2024-07-22 15:10:58",
    "summary": (
        "Résumé: L'Ukraine intensifie son engagement diplomatique en Afrique dans le contexte de la guerre avec la Russie, "
        "cherchant à renforcer ses liens économiques et politiques avec les pays africains. Elle vise à contrer l'influence russe "
        "sur le continent, faire valoir sa position sur le conflit et potentiellement développer des coopérations dans le domaine sécuritaire."
    ),
    "vectors": (
        "Based on the text, here are the main threat vectors I can identify:\n"
        "Russia -> Ukraine\n"
        "Russia -> West African countries (through influence operations)\n"
        "Russia -> Global grain markets (through blockade of Black Sea ports)\n"
        "Ukraine -> Russian influence in Africa (through counter-influence efforts)"
    )
}

# === Headers with API key ===
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# === Send the request ===
response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

# === Output response ===
print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw Response:", response.text)
