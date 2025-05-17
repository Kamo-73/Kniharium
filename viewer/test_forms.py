import datetime

from django.test import TestCase

from viewer.forms import AuthorModelForm, BookModelForm, PublisherModelForm, CommentModelForm
from viewer.models import Nationality, Genre, Author, Publisher, Format


class AuthorFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Nationality.objects.create(name="česká")
        Nationality.objects.create(name="americká")

    def test_author_form_is_valid(self):
        form = AuthorModelForm(
            data={
                'name': 'Petr',
                'surname': 'Pan',
                'date_of_birth': '1956-01-02',
                'date_of_death': '2010-02-02',
                'biography': 'Něco.',
                'nationality': '1',
            }
        )
        self.assertTrue(form.is_valid())

    def test_author_form_name_is_invalid(self):
        form = AuthorModelForm(
            data={
                'name': '',
                'surname': '',
                'date_of_birth': '1956-01-02',
                'date_of_death': '2010-02-02',
                'biography': 'Něco.',
                'nationality': '1',
            }
        )
        self.assertFalse(form.is_valid())

    def test_author_form_date_of_birth_is_invalid(self):
        form = AuthorModelForm(
            data={
                'name': 'Petr',
                'surname': 'Pan',
                'date_of_birth': '2032-01-02',
                'date_of_death': '',
                'biography': 'Něco.',
                'nationality': '1',
            }
        )
        self.assertFalse(form.is_valid())

    def test_author_form_date_of_death_is_invalid(self):
        form = AuthorModelForm(
            data={
                'name': 'Petr',
                'surname': 'Pan',
                'date_of_birth': '1990-01-02',
                'date_of_death': '2034-01-02',
                'biography': 'Něco.',
                'nationality': '1',
            }
        )
        self.assertFalse(form.is_valid())

    def test_author_form_dates_is_invalid(self):
        form = AuthorModelForm(
            data={
                'name': 'Petr',
                'surname': 'Pan',
                'date_of_birth': '1990-01-02',
                'date_of_death': '1980-01-02',
                'biography': 'Něco.',
                'nationality': '1',
            }
        )
        self.assertFalse(form.is_valid())

class BookFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="drama")
        Genre.objects.create(name="fantasy")

        Nationality.objects.create(name="česká")
        Nationality.objects.create(name="americká")


        Author.objects.create(
            name="Petr",
            surname="Pan",
            date_of_birth=datetime.date(1956, 1, 2),
            biography="Super."
        )

        Author.objects.create(
            name="Pavel",
            surname='Malý',
            date_of_birth=datetime.date(1969, 1, 2),
            biography="Fajn."
        )

        Publisher.objects.create(
            name='Albatros',
            information='něco',
            year_of_establishment=1963,
        )

        Publisher.objects.create(
            name='aaa',
            information='něco',
            year_of_establishment=1963,
        )

        Format.objects.create(
            name='vázaná kniha'
        )

        Format.objects.create(
            name='E-kniha'
        )

        Format.objects.create(
            name='Audio kniha'
        )

    def test_book_form_is_valid(self):
            form = BookModelForm(
                data={
                    'author': ['1'],
                    'title_orig': 'Originální název',
                    'title_cz': 'Český název',
                    'num_of_pages': '310',
                    'description': 'Popis.',
                    'publisher': '2',
                    'genre': ['1', '2'],
                    'rating_ours': '5',
                    'review': 'Recenze',
                    'year_of_publishing': '2021',
                    'time_of_reading': '650',
                    'format': ['1', '2', '3']
                }
            )
            self.assertTrue(form.is_valid())

    def test_book_title_orig_is_invalid(self):
            form = BookModelForm(
                data={
                    'author': ['1'],
                    'title_orig': '',
                    'title_cz': 'Český název',
                    'num_of_pages': '310',
                    'description': 'Popis.',
                    'publisher': '2',
                    'genre': ['1', '2'],
                    'rating_ours': '5',
                    'review': 'Recenze',
                    'year_of_publishing': '2021',
                    'time_of_reading': '650',
                    'format': ['1', '2', '3']
                }
            )
            self.assertFalse(form.is_valid())

    def test_book_title_cz_is_invalid(self):
            form = BookModelForm(
                data={
                    'author': ['1'],
                    'title_orig': 'Originální název',
                    'title_cz': '',
                    'num_of_pages': '310',
                    'description': 'Popis.',
                    'publisher': '2',
                    'genre': ['1', '2'],
                    'rating_ours': '5',
                    'review': 'Recenze',
                    'year_of_publishing': '2021',
                    'time_of_reading': '650',
                    'format': ['1', '2', '3']
                }
            )
            self.assertFalse(form.is_valid())

    def test_book_num_of_pages_is_invalid(self):
            form = BookModelForm(
                data={
                    'author': ['1'],
                    'title_orig': 'Originální název',
                    'title_cz': 'Český název',
                    'num_of_pages': '-310',
                    'description': 'Popis.',
                    'publisher': '2',
                    'genre': ['1', '2'],
                    'rating_ours': '5',
                    'review': 'Recenze',
                    'year_of_publishing': '2021',
                    'time_of_reading': '650',
                    'format': ['1', '2', '3']
                }
            )
            self.assertFalse(form.is_valid())

            form = BookModelForm(
                data={
                    'author': ['1'],
                    'title_orig': 'Originální název',
                    'title_cz': 'Český název',
                    'num_of_pages': '0',
                    'description': 'Popis.',
                    'publisher': '2',
                    'genre': ['1', '2'],
                    'rating_ours': '5',
                    'review': 'Recenze',
                    'year_of_publishing': '2021',
                    'time_of_reading': '650',
                    'format': ['1', '2', '3']
                }
            )
            self.assertFalse(form.is_valid())

    def test_book_rating_ours_is_invalid(self):
        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '0',
                'review': 'Recenze',
                'year_of_publishing': '2021',
                'time_of_reading': '650',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '-2',
                'review': 'Recenze',
                'year_of_publishing': '2021',
                'time_of_reading': '650',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '7',
                'review': 'Recenze',
                'year_of_publishing': '2021',
                'time_of_reading': '650',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

    def test_book_year_of_publishing_is_invalid(self):
        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '3',
                'review': 'Recenze',
                'year_of_publishing': '2030',
                'time_of_reading': '650',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '3',
                'review': 'Recenze',
                'year_of_publishing': '0',
                'time_of_reading': '650',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '3',
                'review': 'Recenze',
                'year_of_publishing': '-10',
                'time_of_reading': '650',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

    def test_book_time_of_reading_is_invalid(self):
        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '3',
                'review': 'Recenze',
                'year_of_publishing': '2020',
                'time_of_reading': '0',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())

        form = BookModelForm(
            data={
                'author': ['1'],
                'title_orig': 'Originální název',
                'title_cz': 'Český název',
                'num_of_pages': '310',
                'description': 'Popis.',
                'publisher': '2',
                'genre': ['1', '2'],
                'rating_ours': '3',
                'review': 'Recenze',
                'year_of_publishing': '2020',
                'time_of_reading': '-10',
                'format': ['1', '2', '3']
            }
        )
        self.assertFalse(form.is_valid())


class PublisherFormTest(TestCase):
    def test_publisher_form_is_valid(self):
        form = PublisherModelForm(
            data={
                'name': 'Název',
                'information': 'Informace',
                'year_of_establishment': '1990',
                'year_of_dissolution': '2024',
            }
        )
        self.assertTrue(form.is_valid())

    def test_publisher_year_of_establishment_is_invalid(self):
        form = PublisherModelForm(
            data={
                'name': 'Název',
                'information': 'Informace',
                'year_of_establishment': '1439',
                'year_of_dissolution': '2024',
            }
        )
        self.assertFalse(form.is_valid())

        form = PublisherModelForm(
            data={
                'name': 'Název',
                'information': 'Informace',
                'year_of_establishment': '2035',
                'year_of_dissolution': '',
            }
        )
        self.assertFalse(form.is_valid())

    def test_publisher_year_of_dissolution_is_invalid(self):
        form = PublisherModelForm(
            data={
                'name': 'Název',
                'information': 'Informace',
                'year_of_establishment': '1990',
                'year_of_dissolution': '1989',
            }
        )
        self.assertFalse(form.is_valid())

        form = PublisherModelForm(
            data={
                'name': 'Název',
                'information': 'Informace',
                'year_of_establishment': '1990',
                'year_of_dissolution': '2035',
            }
        )
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    def test_comment_form_is_valid(self):
        form = CommentModelForm(
            data={
                'rating': 4,
                'user_comment': 'Skvělé.'
            }
        )
        self.assertTrue(form.is_valid())

    def test_comment_form_rating_high_is_invalid(self):
        form = CommentModelForm(
            data={
                'rating': 6,
                'user_comment': 'Přehnané hodnocení.'
            }
        )
        self.assertFalse(form.is_valid())

    def test_comment_form_rating_low_is_invalid(self):
        form = CommentModelForm(
            data={
                'rating': 0,
                'user_comment': 'Nízké hodnocení.'
            }
        )
        self.assertFalse(form.is_valid())





