import datetime

from django.test import TestCase

from viewer.forms import AuthorModelForm, BookModelForm
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
                    'publisher': ['1'],
                    'genre': ['1', '2'],
                    'rating_ours': '5',
                    'review': 'Recenze',
                    'year_of_publishing': '2021',
                    'time_of_reading': '650',
                    'format': ['1', '2', '3']
                }
            )
            self.assertTrue(form.is_valid())