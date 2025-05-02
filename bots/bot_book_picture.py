import requests
from urllib.parse import quote

def get_cover_url(book_title):
    query = quote(book_title)
    url = f"https://openlibrary.org/search.json?title={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Nepodařilo se získat údaje z OpenLibrary.")
        return None

    data = response.json()
    if "docs" not in data or not data["docs"]:
        print("❌ Kniha nebyla nalezena.")
        return None

    doc = data["docs"][0]
    if "cover_i" in doc:
        cover_id = doc["cover_i"]
        image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        print(f"🖼️ URL obálky: {image_url}")
        return image_url
    else:
        print("⚠️ Obálka nebyla nalezena.")
        return None

if __name__ == "__main__":
    book_title = input("Zadej název knihy: ")
    get_cover_url(book_title)
