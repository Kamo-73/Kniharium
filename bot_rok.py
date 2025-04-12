import requests
from urllib.parse import quote
import random

def ziskaj_rok_vydania(nazov_knihy):
    query = quote(nazov_knihy)
    url = f"https://openlibrary.org/search.json?title={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Chyba pri načítaní OpenLibrary.")
        return random.randint(2000, 2025)

    data = response.json()
    if not data.get("docs"):
        print("❌ Žiadna zhoda pre knihu.")
        return random.randint(2000, 2025)

    for zaznam in data["docs"]:
        year = zaznam.get("first_publish_year")
        if year:
            return year

    print("⚠️ Rok vydania nebol nájdený, vyberám náhodne.")
    return random.randint(2000, 2025)
