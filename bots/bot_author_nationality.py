import requests
import random
from urllib.parse import quote

# ✅ Česká národnosť – zoznam
CZECH_NATIONALITIES = [
    "Americká", "Anglická", "Argentinská", "Australská", "Belgická", "Brazilská", "Britská",
    "Dánská", "Egyptská", "Finská", "Francouzská", "Indická", "Irská", "Italská", "Izraelská",
    "Japonská", "Kanadská", "Korejská", "Kubánská", "Maďarská", "Mexická", "Nizozemská",
    "Norská", "Německá", "Polská", "Portugalská", "Rumunská", "Ruská", "Slovenská", "Turecká",
    "USA", "Ukrajinská", "Íránská", "Česká", "Čínská", "Řecká", "Španělská", "Švédská", "Švýcarská",
    "Rakouská"
]

# 🔤 Preklad anglických národností na české
NATIONALITY_MAP = {
    "United States of America": "Americká", "United States": "Americká", "USA": "Americká", "US": "Americká", "American": "Americká",
    "England": "Anglická", "English": "Anglická", "United Kingdom": "Britská", "Great Britain": "Britská", "British": "Britská",
    "Argentina": "Argentinská", "Argentine": "Argentinská", "Australia": "Australská", "Australian": "Australská",
    "Belgium": "Belgická", "Belgian": "Belgická", "Brazil": "Brazilská", "Brazilian": "Brazilská",
    "Denmark": "Dánská", "Danish": "Dánská", "Egypt": "Egyptská", "Egyptian": "Egyptská",
    "Finland": "Finská", "Finnish": "Finská", "France": "Francouzská", "French": "Francouzská",
    "India": "Indická", "Indian": "Indická", "Ireland": "Irská", "Irish": "Irská",
    "Italy": "Italská", "Italian": "Italská", "Israel": "Izraelská", "Israeli": "Izraelská",
    "Japan": "Japonská", "Japanese": "Japonská", "Canada": "Kanadská", "Canadian": "Kanadská",
    "South Korea": "Korejská", "Republic of Korea": "Korejská", "Korean": "Korejská",
    "Cuba": "Kubánská", "Cuban": "Kubánská", "Hungary": "Maďarská", "Hungarian": "Maďarská",
    "Mexico": "Mexická", "Mexican": "Mexická", "Netherlands": "Nizozemská", "Dutch": "Nizozemská",
    "Norway": "Norská", "Norwegian": "Norská", "Germany": "Německá", "German": "Německá",
    "Poland": "Polská", "Polish": "Polská", "Portugal": "Portugalská", "Portuguese": "Portugalská",
    "Romania": "Rumunská", "Romanian": "Rumunská", "Russia": "Ruská", "Russian": "Ruská",
    "Slovakia": "Slovenská", "Slovak": "Slovenská", "Turkey": "Turecká", "Turkish": "Turecká",
    "Ukraine": "Ukrajinská", "Ukrainian": "Ukrajinská", "Iran": "Íránská", "Iranian": "Íránská",
    "Czech Republic": "Česká", "Czechia": "Česká", "Czech": "Česká", "China": "Čínská", "Chinese": "Čínská",
    "Greece": "Řecká", "Greek": "Řecká", "Spain": "Španělská", "Spanish": "Španělská",
    "Sweden": "Švédská", "Swedish": "Švédská", "Switzerland": "Švýcarská", "Swiss": "Švýcarská",
    "Czechoslovakia": "Česká", "Cisleithania": "Rakouská"
}

def translate_nationality_to_czech(english):
    return NATIONALITY_MAP.get(english.strip(), None)

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

def get_nationalities_from_wikidata(wikidata_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    claims = data['entities'][wikidata_id].get('claims', {})
    nationalities = []
    if 'P27' in claims:
        for item in claims['P27']:
            qid = item['mainsnak']['datavalue']['value']['id']
            detail_url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
            detail_resp = requests.get(detail_url)
            if detail_resp.status_code == 200:
                label_data = detail_resp.json()
                en_name = label_data['entities'][qid]['labels'].get('en', {}).get('value')
                if en_name:
                    nationalities.append(en_name)
    return nationalities

def detect_author_nationality(first_name, last_name):
    full_name = f"{first_name} {last_name}"
    wikidata_id = get_wikidata_id(full_name)
    if not wikidata_id:
        print("❌ Wikidata ID se nepodařilo získat.")
        return

    nationalities_en = get_nationalities_from_wikidata(wikidata_id)

    for en_nationality in nationalities_en:
        cz_nationality = translate_nationality_to_czech(en_nationality)
        if cz_nationality:
            print(f"🌍 Národnost: {cz_nationality}")
            return

    fallback = random.choice(CZECH_NATIONALITIES)
    print(f"🌍 Národnost (náhodná): {fallback}")

if __name__ == "__main__":
    first_name = input("Zadej jméno autora: ")
    last_name = input("Zadej příjmení autora: ")
    detect_author_nationality(first_name, last_name)
