import os
import sys
import django
import random
import datetime
import requests
from urllib.parse import quote

# Django environment initialization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

# Import of the model and sub-bots
from viewer.models import Author, Nationality
from bots.bot_author_bio import get_description_from_wikipedia, translate_to_czech, FALLBACK_BIO_MALE, \
    FALLBACK_BIO_FEMALE
from bots.bot_author_nationality import get_wikidata_id, get_nationalities_from_wikidata, \
    translate_nationality_to_czech, CZECH_NATIONALITIES
from bots.bot_author_years import get_birth_date


def create_author(first_name, last_name, gender):
    # Check if the author already exists
    if Author.objects.filter(name=first_name.strip(), surname=last_name.strip()).exists():
        print(f"⚠️ Autor {first_name} {last_name} už v databázi existuje.")
        return

    full_name = f"{first_name} {last_name}"

    # Bio
    description_en = get_description_from_wikipedia(full_name)
    if not description_en or len(description_en.strip()) < 50:
        bio = random.choice(FALLBACK_BIO_MALE if gender == "muž" else FALLBACK_BIO_FEMALE)
    else:
        bio = translate_to_czech(description_en)
        if len(bio.strip()) < 50 or "MYMEMORY WARNING" in bio.upper():
            bio = random.choice(FALLBACK_BIO_MALE if gender == "muž" else FALLBACK_BIO_FEMALE)

    # Nationality
    wikidata_id = get_wikidata_id(full_name)
    cz_nationality = None
    if wikidata_id:
        nationalities_en = get_nationalities_from_wikidata(wikidata_id)
        for en in nationalities_en:
            cz = translate_nationality_to_czech(en)
            if cz:
                cz_nationality = cz
                break
    if not cz_nationality:
        cz_nationality = random.choice(CZECH_NATIONALITIES)

    nationality_obj, _ = Nationality.objects.get_or_create(name=cz_nationality)

    # Birth date
    birth_date = get_birth_date(wikidata_id) if wikidata_id else None
    if birth_date:
        year, month, day = map(int, birth_date.split("-"))
        if month < 1 or month > 12:
            month = 1
        if day < 1 or day > 31:
            day = 1
        birth_date_obj = datetime.date(year, month, day)
    else:
        fallback_year = random.randint(1969, 2000)
        birth_date_obj = datetime.date(fallback_year, 1, 1)

    # ✅ Picture
    query = quote(full_name)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        picture_url = data.get("thumbnail", {}).get("source")
    else:
        picture_url = None

    if not picture_url:
        fallback = "author_fallback_woman.png" if gender == "žena" else "author_fallback_man.png"
        picture_url = f"images/{fallback}"

    # Saving the author
    author = Author.objects.create(
        name=first_name.strip(),
        surname=last_name.strip(),
        biography=bio.strip(),
        date_of_birth=birth_date_obj,
        image=picture_url,
        nationality=nationality_obj
    )

    print(f"\n✅ Autor pridaný: {author.name} {author.surname}")
    print(f"📖 Bio: {bio[:100]}...")
    print(f"🌍 Národnost: {cz_nationality}")
    print(f"🎂 Datum narození: {birth_date_obj}")
    print(f"🖼️ Obrázek: {picture_url}")


def run(name, surname, gender):
    create_author(name, surname, gender)


if __name__ == "__main__":
    first_name = input("Zadej jméno autora/autorky: ")
    last_name = input("Zadej příjmení autora/autorky: ")
    gender = input("Zadej pohlaví (muž/žena): ").strip().lower()

    if gender not in ["muž", "zena", "žena"]:
        print("⚠️ Neplatné pohlaví. Použij 'muž' nebo 'žena'.")
    else:
        gender = "žena" if gender in ["žena", "zena"] else "muž"
        create_author(first_name, last_name, gender)
