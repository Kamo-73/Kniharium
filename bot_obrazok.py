import requests
from urllib.parse import quote

def ziskaj_url_obrazka(nazov_knihy):
    query = quote(nazov_knihy)
    url = f"https://openlibrary.org/search.json?title={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Nepodarilo sa získať údaje z OpenLibrary.")
        return None

    data = response.json()
    if "docs" not in data or not data["docs"]:
        print("❌ Kniha nebola nájdená.")
        return None

    doc = data["docs"][0]
    if "cover_i" in doc:
        cover_id = doc["cover_i"]
        image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        print(f"🖼️ URL obálky: {image_url}")
        return image_url
    else:
        print("⚠️ Obálka nebola nájdená.")
        return None
