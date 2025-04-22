from django.test import TestCase

from viewer.forms import AuthorModelForm
from viewer.models import Nationality


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

    def test_author_form_is_invalid(self):
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