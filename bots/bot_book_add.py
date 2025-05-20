import os
import sys
import django
from math import ceil
from django.db import transaction

# Django initialization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

# Import of models and bots
from viewer.models import Book, Author, Publisher, Genre, Format
from bots.bot_book_description import get_and_translate_description
from bots.bot_book_year import get_year_of_release
from bots.bot_book_picture import get_cover_url
from bots.bot_book_genres import save_genres_to_database

# List of books to add
BOOK_LIST = [
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "Sarum",
        "title_cz": "Sarum: Sága Anglie",
        "num_of_pages": 912,
        "publisher": "BB/art",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "London",
        "title_cz": "Londýn",
        "num_of_pages": 1152,
        "publisher": "BB/art",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha", "Audiokniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "New York",
        "title_cz": "New York",
        "num_of_pages": 1040,
        "publisher": "BB/art",
        "rating_ours": 5,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "Paris",
        "title_cz": "Paříž",
        "num_of_pages": 944,
        "publisher": "BB/art",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "Russka",
        "title_cz": "Russka: Příběh Ruska",
        "num_of_pages": 992,
        "publisher": "BB/art",
        "rating_ours": 4,
        "format": ["Vázaná kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "The Forest",
        "title_cz": "Les",
        "num_of_pages": 816,
        "publisher": "BB/art",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "China",
        "title_cz": "Čína",
        "num_of_pages": 1072,
        "publisher": "BB/art",
        "rating_ours": 5,
        "format": ["Vázaná kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "The Rebels of Ireland",
        "title_cz": "Rebelové Irska",
        "num_of_pages": 768,
        "publisher": "BB/art",
        "rating_ours": 4,
        "format": ["Vázaná kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "The Princes of Ireland",
        "title_cz": "Princové Irska",
        "num_of_pages": 768,
        "publisher": "BB/art",
        "rating_ours": 4,
        "format": ["Vázaná kniha", "E-kniha"]
    },
    {
        "name": "Edward",
        "surname": "Rutherfurd",
        "title_orig": "Dublin: Foundation",
        "title_cz": "Dublin: Zrození",
        "num_of_pages": 720,
        "publisher": "BB/art",
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


def run(book_data):
    print("▶️ Pridávam knihu:", book_data["title_cz"])

    from viewer.models import Author, Book, Publisher, Format, Genre
    from bots.bot_book_description import get_and_translate_description
    from bots.bot_book_year import get_year_of_release
    from bots.bot_book_picture import get_cover_url
    from bots.bot_book_genres import save_genres_to_database
    from math import ceil

    def calculate_reading_time(pages):
        words_per_page = 275
        reading_speed = 225
        return ceil((pages * words_per_page) / reading_speed)

    author_obj = Author.objects.filter(name=book_data["name"], surname=book_data["surname"]).first()
    if not author_obj:
        raise Exception(f"❌ Autor {book_data['name']} {book_data['surname']} neexistuje v databáze.")

    books_with_same_title = Book.objects.filter(title_orig=book_data["title_orig"])
    already_exists = any(author_obj in b.author.all() for b in books_with_same_title)
    if already_exists:
        raise Exception(f"⚠️ Kniha s názvom {book_data['title_orig']} od daného autora už existuje.")
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

    print(f"✅ Kniha '{book.title_cz}' bola pridaná.")


if __name__ == "__main__":
    add_books()
