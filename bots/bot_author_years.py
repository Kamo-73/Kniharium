import requests
from urllib.parse import quote
import random

def get_wikidata_id(author_name):
    query = quote(author_name)
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={query}&prop=pageprops"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        return page.get("pageprops", {}).get("wikibase_item")
    return None

def get_birth_date(wikidata_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    claims = data['entities'][wikidata_id].get('claims', {})

    if 'P569' in claims:
        time_str = claims['P569'][0]['mainsnak']['datavalue']['value']['time']
        return time_str.lstrip('+').split('T')[0]
    return None

def display_author_birth_year(first_name, last_name):
    full_name = f"{first_name} {last_name}"
    wikidata_id = get_wikidata_id(full_name)
    if not wikidata_id:
        print("❌ Wikidata ID se nepodařilo získat.")
        return

    birth_date = get_birth_date(wikidata_id)

    if birth_date:
        print(f"🎂 Datum narození: {birth_date}")
    else:
        fallback_year = random.randint(1969, 2000)
        print(f"🎂 Datum narození neznámý – vygenerovaný: {fallback_year}-01-01")

if __name__ == "__main__":
    first_name = input("Zadej jméno autora: ")
    last_name = input("Zadej příjmení autora: ")
    display_author_birth_year(first_name, last_name)
