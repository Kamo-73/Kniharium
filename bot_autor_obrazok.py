import requests
from urllib.parse import quote

def ziskaj_url_obrazka(meno, priezvisko, pohlavie, jazyk='en'):
    cele_meno = f"{meno} {priezvisko}"
    query = quote(cele_meno)
    url = f"https://{jazyk}.wikipedia.org/api/rest_v1/page/summary/{query}"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Nepodarilo sa získať údaje z Wikipédie pre {cele_meno}")
        return

    data = response.json()
    title = data.get("title", cele_meno)
    obrazok_url = data.get("thumbnail", {}).get("source")

    print(f"\n📚 Wikipedia stránka: {title}")
    if obrazok_url:
        print(f"🖼️ Obrázok z Wikipédie: {obrazok_url}")
    else:
        fallback = "author_fallback_woman.png" if pohlavie == "žena" else "author_fallback_man.png"
        fallback_path = f"images/{fallback}"  # cesta relatívna k MEDIA_ROOT
        print(f"🖼️ Obrázok nenájdený – použitý fallback: /media/{fallback_path}")

if __name__ == "__main__":
    meno = input("Zadaj meno autora/autorky: ")
    priezvisko = input("Zadaj priezvisko autora/autorky: ")
    pohlavie = input("Zadaj pohlavie (muž/žena): ").strip().lower()

    if pohlavie not in ["muž", "zena", "žena"]:
        print("⚠️ Neplatné pohlavie. Použi 'muž' alebo 'žena'.")
    else:
        pohlavie = "žena" if pohlavie in ["žena", "zena"] else "muž"
        ziskaj_url_obrazka(meno, priezvisko, pohlavie)
