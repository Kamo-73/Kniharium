"""
📄 Tento súbor slúži na pridanie balíka kníh do databázy.

📌 Očakávané vstupy (dodané zoznamom dictionaries):
---------------------------------------------------
Pole           | Význam
-------------- | ----------------------------------------------------------
name           | Krstné meno autora (presne podľa DB)
surname        | Priezvisko autora (presne podľa DB)
title_orig     | Originálny názov knihy
title_cz       | Český preklad názvu knihy
num_of_pages   | Počet strán
publisher      | Názov českého vydavateľstva (musí existovať v DB)
rating_ours    | Hodnotenie (1–5) podľa subjektívneho hodnotenia
format         | Zoznam formátov (napr. ["Audio kniha", "E-kniha", "Vázaná kniha"])

📌 Útaje ako popis, rok vydania, obálka, žánre doplnia ďalší boti:
- bot_popis.py
- bot_rok.py
- bot_obrazok.py
- bot_zanre.py

Stačí meniť obsah premennej `ZOZNAM_KNIH` a spustiť skript.
"""

from viewer.models import Book, Author, Publisher, Genre, Format
from bot_popis import ziskaj_a_preloz_popis
from bot_rok import ziskaj_rok_vydania
from bot_zanre import ziskaj_subjects_openlibrary, PREKLAD_ZANROV
from bot_obrazok import ziskaj_url_obrazka
from django.db import transaction
from math import ceil

ZOZNAM_KNIH = [
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "The Shining",
        "title_cz": "Osvícení",
        "num_of_pages": 456,
        "publisher": "Beta Dobrovský",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha", "Audio kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "It",
        "title_cz": "To",
        "num_of_pages": 1168,
        "publisher": "BETA",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "Audio kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "Carrie",
        "title_cz": "Carrie",
        "num_of_pages": 264,
        "publisher": "BETA",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "Misery",
        "title_cz": "Misery",
        "num_of_pages": 384,
        "publisher": "BETA",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "Audio kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "Pet Sematary",
        "title_cz": "Řbitov zvířátek",
        "num_of_pages": 368,
        "publisher": "BETA",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "Doctor Sleep",
        "title_cz": "Doktor Spánek",
        "num_of_pages": 544,
        "publisher": "BETA",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "Audio kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "11/22/63",
        "title_cz": "Dallas 63",
        "num_of_pages": 752,
        "publisher": "BETA",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha", "Audio kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "The Green Mile",
        "title_cz": "Zelená míle",
        "num_of_pages": 448,
        "publisher": "BETA",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "Audio kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "Gerald's Game",
        "title_cz": "Geraldova hra",
        "num_of_pages": 352,
        "publisher": "BETA",
        "rating_ours": 4,
        "format": ["E-kniha"]
    },
    {
        "name": "Stephen",
        "surname": "King",
        "title_orig": "Salem's Lot",
        "title_cz": "Prokletí Salemu",
        "num_of_pages": 480,
        "publisher": "BETA",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha"]
    }
]

def vypocitaj_dobu_citania(pocet_stran):
    words_per_page = 275
    reading_speed = 225
    total_words = pocet_stran * words_per_page
    return ceil(total_words / reading_speed)

@transaction.atomic
def pridaj_knihy():
    for kniha in ZOZNAM_KNIH:
        print(f"\n🔄 Spracúvam knihu: {kniha['title_orig']}")

        autor_obj = Author.objects.filter(name=kniha["name"], surname=kniha["surname"]).first()
        if not autor_obj:
            print(f"❌ Autor {kniha['name']} {kniha['surname']} neexistuje v databáze.")
            continue

        # 🔎 Kontrola duplicity
        print("🔍 Kontrolujem, či kniha už existuje...")
        existujuca_kniha = Book.objects.filter(title_orig=kniha["title_orig"], author=autor_obj).first()
        if existujuca_kniha:
            print(f"⚠️ Kniha '{kniha['title_orig']}' od autora už existuje. Preskakujem.")
            continue

        publisher_obj, _ = Publisher.objects.get_or_create(name=kniha["publisher"])

        format_objs = []
        for nazov_formatu in kniha["format"]:
            form_obj, _ = Format.objects.get_or_create(name=nazov_formatu)
            format_objs.append(form_obj)

        rok = ziskaj_rok_vydania(kniha["title_orig"])
        popis = ziskaj_a_preloz_popis(kniha["title_orig"])
        image_url = ziskaj_url_obrazka(kniha["title_orig"])
        time_of_reading = vypocitaj_dobu_citania(kniha["num_of_pages"])

        subjects = ziskaj_subjects_openlibrary(kniha["title_orig"])
        zhody = []
        for s in subjects:
            for en, cz in PREKLAD_ZANROV.items():
                if en.lower() in s.lower():
                    zhody.append(cz)
                    break
        zhody = list(set(zhody))

        book = Book.objects.create(
            title_orig=kniha["title_orig"],
            title_cz=kniha["title_cz"],
            num_of_pages=kniha["num_of_pages"],
            publisher=publisher_obj,
            year_of_publishing=rok,
            time_of_reading=time_of_reading,
            description=popis,
            image=image_url,
            rating_ours=kniha["rating_ours"]
        )

        book.author.add(autor_obj)
        for f in format_objs:
            book.format.add(f)

        if not zhody:
            genre_obj, _ = Genre.objects.get_or_create(name="Neurčený")
            book.genre.add(genre_obj)
        else:
            for nazov_zanru in zhody:
                genre_obj, _ = Genre.objects.get_or_create(name=nazov_zanru)
                book.genre.add(genre_obj)

        print(f"✅ Kniha '{book.title_orig}' bola pridaná do databázy.")


# from bot_pridaj_knihy import pridaj_knihy
# pridaj_knihy()
