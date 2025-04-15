import os
import sys
import django
import random
import datetime
import requests
from urllib.parse import quote

# 🛠️ Inicializácia Django prostredia
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

# 📦 Import modelu a podbotov
from viewer.models import Author, Nationality
from bot_autor_bio import ziskaj_popis_z_wikipedie, preloz_do_cestiny, FALLBACK_BIO_MUZ, FALLBACK_BIO_ZENA
from bot_autor_narodnost import ziskaj_wikidata_id, ziskaj_narodnosti_z_wikidata, preloz_narodnost_do_cestiny, CESKE_NARODNOSTI
from bot_autor_roky import ziskaj_datum_narodenia
from bot_autor_obrazok import ziskaj_url_obrazka


def vytvor_autora(meno, priezvisko, pohlavie):
    # ✅ Kontrola, či autor už existuje
    if Author.objects.filter(name=meno.strip(), surname=priezvisko.strip()).exists():
        print(f"⚠️ Autor {meno} {priezvisko} už v databáze existuje.")
        return

    cele_meno = f"{meno} {priezvisko}"

    # ✅ BIOGRAFIA
    popis_en = ziskaj_popis_z_wikipedie(cele_meno)
    if not popis_en or len(popis_en.strip()) < 50:
        bio = random.choice(FALLBACK_BIO_MUZ if pohlavie == "muž" else FALLBACK_BIO_ZENA)
    else:
        bio = preloz_do_cestiny(popis_en)
        if len(bio.strip()) < 50 or "MYMEMORY WARNING" in bio.upper():
            bio = random.choice(FALLBACK_BIO_MUZ if pohlavie == "muž" else FALLBACK_BIO_ZENA)

    # ✅ NÁRODNOSŤ
    wikidata_id = ziskaj_wikidata_id(cele_meno)
    cz_narodnost = None
    if wikidata_id:
        narodnosti_en = ziskaj_narodnosti_z_wikidata(wikidata_id)
        for en in narodnosti_en:
            cz = preloz_narodnost_do_cestiny(en)
            if cz:
                cz_narodnost = cz
                break
    if not cz_narodnost:
        cz_narodnost = random.choice(CESKE_NARODNOSTI)

    # Pripojenie národnosti z DB (alebo vytvorenie)
    narodnost_obj, _ = Nationality.objects.get_or_create(name=cz_narodnost)

    # ✅ DÁTUM NARODENIA
    datum = ziskaj_datum_narodenia(wikidata_id) if wikidata_id else None
    if datum:
        rok, mesiac, den = map(int, datum.split("-"))
        if mesiac < 1 or mesiac > 12:
            mesiac = 1
        if den < 1 or den > 31:
            den = 1
        datum_obj = datetime.date(rok, mesiac, den)
    else:
        fallback_rok = random.randint(1969, 2000)
        datum_obj = datetime.date(fallback_rok, 1, 1)

    # ✅ OBRÁZOK
    query = quote(cele_meno)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        obrazok_url = data.get("thumbnail", {}).get("source")
    else:
        obrazok_url = None

    if not obrazok_url:
        fallback = "author_fallback_woman.png" if pohlavie == "žena" else "author_fallback_man.png"
        obrazok_url = f"viewer/static/images/{fallback}"

    # ✅ Uloženie autora
    autor = Author.objects.create(
        name=meno.strip(),
        surname=priezvisko.strip(),
        biography=bio.strip(),
        date_of_birth=datum_obj,
        image=obrazok_url,
        nationality=narodnost_obj
    )

    print(f"\n✅ Autor pridaný: {autor.name} {autor.surname}")
    print(f"📖 Bio: {bio[:100]}...")
    print(f"🌍 Národnosť: {cz_narodnost}")
    print(f"🎂 Dátum narodenia: {datum_obj}")
    print(f"🖼️ Obrázok: {obrazok_url}")


if __name__ == "__main__":
    meno = input("Zadaj meno autora/autorky: ")
    priezvisko = input("Zadaj priezvisko autora/autorky: ")
    pohlavie = input("Zadaj pohlavie (muž/žena): ").strip().lower()

    if pohlavie not in ["muž", "zena", "žena"]:
        print("⚠️ Neplatné pohlavie. Použi 'muž' alebo 'žena'.")
    else:
        pohlavie = "žena" if pohlavie in ["žena", "zena"] else "muž"
        vytvor_autora(meno, priezvisko, pohlavie)
