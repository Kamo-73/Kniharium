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
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "101x Česko",
        "title_cz": "101x Česko",
        "num_of_pages": 250,
        "publisher": "Motto",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Cesta na konec světa",
        "title_cz": "Cesta na konec světa",
        "num_of_pages": 310,
        "publisher": "Motto",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Na východ vlakem",
        "title_cz": "Na východ vlakem",
        "num_of_pages": 290,
        "publisher": "Motto",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Cesty na východ",
        "title_cz": "Cesty na východ",
        "num_of_pages": 350,
        "publisher": "Motto",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha", "Audio kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Pěšky do Indie",
        "title_cz": "Pěšky do Indie",
        "num_of_pages": 320,
        "publisher": "Motto",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Konec světa",
        "title_cz": "Konec světa",
        "num_of_pages": 330,
        "publisher": "Motto",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Cesty na východ – druhá část",
        "title_cz": "Cesty na východ – druhá část",
        "num_of_pages": 310,
        "publisher": "Motto",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Cesta do Indie",
        "title_cz": "Cesta do Indie",
        "num_of_pages": 300,
        "publisher": "Motto",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Cesta kolem světa",
        "title_cz": "Cesta kolem světa",
        "num_of_pages": 350,
        "publisher": "Motto",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Ladislav",
        "surname": "Zibura",
        "title_orig": "Pěšky na konec světa",
        "title_cz": "Pěšky na konec světa",
        "num_of_pages": 290,
        "publisher": "Motto",
        "rating_ours": 4,
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
