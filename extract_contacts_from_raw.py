import os
import re
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def extract_contacts(text):
    phones = re.findall(r"\+?\d[\d\-\s]{7,}\d", text)
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    names = re.findall(r"(?:Mr\.|Ms\.|Mrs\.|Dr\.)?\s?[A-Z][a-z]+\s[A-Z][a-z]+", text)
    positions = re.findall(
        r"\b(?:CEO|Manager|Director|Head|Owner|President|Founder|Executive|Coordinator|Consultant|Officer)\b",
        text, re.IGNORECASE)

    return {
        "phones": list(set(phones)),
        "emails": list(set(emails)),
        "names": list(set(names)),
        "positions": list(set(positions))
    }

def main():
    response = supabase.table("contacts").select("id, company_url, raw_text").is_("email", "null").is_("phone", "null").execute()
    contacts = response.data

    parsed = []

    for contact in contacts:
        extracted = extract_contacts(contact["raw_text"])
        for i in range(max(len(extracted["phones"]), len(extracted["emails"]), 1)):
            parsed.append({
                "company_url": contact["company_url"],
                "email": extracted["emails"][i] if i < len(extracted["emails"]) else None,
                "phone": extracted["phones"][i] if i < len(extracted["phones"]) else None,
                "full_name": extracted["names"][i] if i < len(extracted["names"]) else None,
                "position": extracted["positions"][i] if i < len(extracted["positions"]) else None
            })

    print(f"🧠 Извлечено {len(parsed)} новых контактов\n")
    for p in parsed:
        print(p)

    # Если нужно — можно сразу отправить в Supabase:
    if parsed:
        result = supabase.table("contacts").insert(parsed).execute()
        print(f"✅ Сохранено: {len(result.data)}")

if __name__ == "__main__":
    main()
