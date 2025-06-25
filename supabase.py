# 📁 backend/app/db/supabase.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # загрузка .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_company_with_score(company: dict):
    try:
        data = {
            "name": company.get("name"),
            "url": company.get("url"),
            "description": company.get("description"),
            "ai_score": company.get("ai_score")  # тип в Supabase теперь text
        }
        result = supabase.table("companies").insert(data).execute()
        print(f"Saved company: {data['name']} with score: {data['ai_score']}")
        return result
    except Exception as e:
        print("Error saving to Supabase:", e)
        return None

def save_contacts_for_company(url: str, contacts: list[dict]):
    try:
        enriched_contacts = []
        for contact in contacts:
            contact["company_url"] = url
            enriched_contacts.append(contact)

        result = supabase.table("contacts").insert(enriched_contacts).execute()
        print(f"Saved {len(enriched_contacts)} contacts for company: {url}")
        return result
    except Exception as e:
        print("Error saving contacts:", e)
        return None

