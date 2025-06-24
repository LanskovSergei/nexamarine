# backend/app/core/serper_client.py
import requests

API_KEY = "a039b5e1bba82d68b0557cdc3169afca8d2a6bf9"
API_URL = "https://google.serper.dev/search"

def search_serper(query: str):
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query}

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()
