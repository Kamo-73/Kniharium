import requests
from urllib.parse import quote
import random


def get_year_of_release(book_title):
    query = quote(book_title)
    url = f"https://openlibrary.org/search.json?title={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Chyba při načítání OpenLibrary.")
        return random.randint(2000, 2025)

    data = response.json()
    if not data.get("docs"):
        print("❌ Žádná shoda pro knihu.")
        return random.randint(2000, 2025)

    for record in data["docs"]:
        year = record.get("first_publish_year")
        if year:
            return year

    print("⚠️ Rok vydání nebyl nalezen, vybírám náhodně.")
    return random.randint(2000, 2025)


if __name__ == "__main__":
    book_title = input("Zadej název knihy: ")
    year = get_year_of_release(book_title)
    print(f"📅 Rok vydání: {year}")
