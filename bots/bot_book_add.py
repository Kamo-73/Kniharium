import os
import sys
import django
from math import ceil
from django.db import transaction

# Inicializácia Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

# Import modelov a botov
from viewer.models import Book, Author, Publisher, Genre, Format
from bots.bot_book_description import get_and_translate_description
from bots.bot_book_year import get_year_of_release
from bots.bot_book_picture import get_cover_url
from bots.bot_book_genres import save_genres_to_database

# Zoznam kníh na pridanie
BOOK_LIST = [
    {
        "name": "Lucy",
        "surname": "Foley",
        "title_orig": "The Hunting Party",
        "title_cz": "Lovecká společnost",
        "num_of_pages": 384,
        "publisher": "Argo",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Lucy",
        "surname": "Foley",
        "title_orig": "The Guest List",
        "title_cz": "Zoznam hostí",
        "num_of_pages": 320,
        "publisher": "Tatran",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Lucy",
        "surname": "Foley",
        "title_orig": "The Paris Apartment",
        "title_cz": "Byt v Paříži",
        "num_of_pages": 400,
        "publisher": "Argo",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Lucy",
        "surname": "Foley",
        "title_orig": "The Book of Lost and Found",
        "title_cz": "Kniha strát a nálezov",
        "num_of_pages": 400,
        "publisher": "Fortuna Libri",
        "rating_ours": 3,
        "format": ["Vázaná kniha"]
    }
]

def calculate_reading_time(pages):
    words_per_page = 275
    reading_speed = 225  # words per minute
    return ceil((pages * words_per_page) / reading_speed)

@transaction.atomic
def add_books():
    for book_data in BOOK_LIST:
        print(f"\n🔄 Zpracovávám knihu: {book_data['title_orig']}")

        author_obj = Author.objects.filter(name=book_data["name"], surname=book_data["surname"]).first()
        if not author_obj:
            print(f"❌ Autor {book_data['name']} {book_data['surname']} neexistuje v databázi.")
            continue

        if Book.objects.filter(title_orig=book_data["title_orig"], author=author_obj).exists():
            print(f"⚠️ Kniha '{book_data['title_orig']}' od autora již existuje. Přeskakuji.")
            continue

        publisher_obj, _ = Publisher.objects.get_or_create(name=book_data["publisher"])

        format_objects = []
        for format_name in book_data["format"]:
            format_obj, _ = Format.objects.get_or_create(name=format_name)
            format_objects.append(format_obj)

        year = get_year_of_release(book_data["title_orig"])
        description = get_and_translate_description(book_data["title_orig"])
        cover_url = get_cover_url(book_data["title_orig"])
        reading_time = calculate_reading_time(book_data["num_of_pages"])

        book = Book.objects.create(
            title_orig=book_data["title_orig"],
            title_cz=book_data["title_cz"],
            num_of_pages=book_data["num_of_pages"],
            publisher=publisher_obj,
            year_of_publishing=year,
            time_of_reading=reading_time,
            description=description,
            image=cover_url,
            rating_ours=book_data["rating_ours"]
        )

        book.author.add(author_obj)
        for f in format_objects:
            book.format.add(f)

        genres = save_genres_to_database(book_data["title_orig"])
        for genre in genres:
            genre_obj, _ = Genre.objects.get_or_create(name=genre)
            book.genre.add(genre_obj)

        print(f"✅ Kniha '{book.title_orig}' byla přidána do databáze.")

if __name__ == "__main__":
    add_books()
