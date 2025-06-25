import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_company_with_score(company: dict):
    """
    company = {
        "name": str,
        "url": str,
        "description": str,
        "ai_score": int
    }
    """
    try:
        data = {
            "name": company.get("name"),
            "url": company.get("url"),
            "description": company.get("description"),
            "ai_score": company.get("ai_score")
        }
        result = supabase.table("companies").insert(data).execute()
        return result
    except Exception as e:
        print("Error saving to Supabase:", e)
        return None
