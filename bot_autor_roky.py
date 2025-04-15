import requests
from urllib.parse import quote
import random


def ziskaj_wikidata_id(meno_autora):
    query = quote(meno_autora)
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={query}&prop=pageprops"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        return page.get("pageprops", {}).get("wikibase_item")
    return None


def ziskaj_datum_narodenia(wikidata_id):
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


def zobraz_rok_narodenia_autora(meno, priezvisko):
    cele_meno = f"{meno} {priezvisko}"
    wikidata_id = ziskaj_wikidata_id(cele_meno)
    if not wikidata_id:
        print("❌ Wikidata ID sa nepodarilo získať.")
        return

    narodenie = ziskaj_datum_narodenia(wikidata_id)

    if narodenie:
        print(f"🎂 Dátum narodenia: {narodenie}")
    else:
        fallback_rok = random.randint(1969, 2000)
        print(f"🎂 Dátum narodenia neznámy – vygenerovaný: {fallback_rok}-01-01")


if __name__ == "__main__":
    meno = input("Zadaj meno autora: ")
    priezvisko = input("Zadaj priezvisko autora: ")
    zobraz_rok_narodenia_autora(meno, priezvisko)
