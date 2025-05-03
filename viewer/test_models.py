import datetime
from django.db import IntegrityError

from django.test import TestCase

from viewer.models import *


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        publisher = Publisher.objects.create(
            name="Albatros",
            information="Vydává knihy.",
            year_of_establishment=1955,
            year_of_dissolution=2010
            )

        book = Book.objects.create(
            title_orig="Originální název knihy",
            title_cz="Český název knihy",
            num_of_pages=128,
            description="Popis knihy.",
            publisher=publisher,
            rating_ours=4,
            review="Skvělá kniha.",
            year_of_publishing=2005,
            time_of_reading=10,
            )

        genre_fantasy = Genre.objects.create(name="fantasy")
        genre_horror = Genre.objects.create(name="horor")
        book.genre.add(genre_fantasy)
        book.genre.add(genre_horror)

        format_ebook = Format.objects.create(name="E-kniha")
        format_book = Format.objects.create(name="Vázaná kniha")
        book.format.add(format_ebook)
        book.format.add(format_book)

        nationality_czech = Nationality.objects.create(name="česká")
        nationality_british = Nationality.objects.create(name="britská")

        author = Author.objects.create(
            name="Petr",
            surname="Pan",
            date_of_birth=datetime.date(1965,1,1),
            date_of_death=datetime.date(2010,10,5),
            biography="Napsal několik knih.",
            nationality=nationality_british,
            )
        book.author.add(author)

    def setUp(self):
        print('-'*80)

    def test_title_orig(self):
        book = Book.objects.get(id=1)
        print(f"test_title_orig: {book.title_orig}")
        self.assertEqual(book.title_orig, "Originální název knihy")

    def test_title_cz(self):
        book = Book.objects.get(id=1)
        print(f"test_title_cz: {book.title_cz}")
        self.assertEqual(book.title_cz, "Český název knihy")

    def test_genres_count(self):
        book = Book.objects.get(id=1)
        number_of_genres = book.genre.count()
        print(f"test_genres_count: {number_of_genres}")
        self.assertEqual(number_of_genres, 2)

    def test_book_repr(self):
        book = Book.objects.get(id=1)
        print(f"test_book_repr: '{book.__repr__()}'")
        self.assertEqual(book.__repr__(), "Book(title_cz=Český název knihy, "
                                          "title_orig=Originální název knihy, authors=Petr Pan, "
                                          "year_of_publishing=2005)")

    def test_book_str(self):
        book = Book.objects.get(id=1)
        print(f"test_book_str: {book}")
        self.assertEqual(book.__str__(), "Český název knihy (Petr Pan)")

    def test_genre_unique(self):
        fantasy_count = Genre.objects.filter(name="fantasy").count()
        print(f"test_genre_unique: {fantasy_count}")
        self.assertEqual(fantasy_count, 1)

    def test_formats_count(self):
        book = Book.objects.get(id=1)
        number_of_formats = book.format.count()
        print(f"test_formats_count: {number_of_formats}")
        self.assertEqual(number_of_formats, 2)



