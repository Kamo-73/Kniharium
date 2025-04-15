import re
from datetime import date

from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput, DateField, NumberInput

from viewer.models import Book, Author


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        #fields = '__all__'
        #fields = ['title_orig', 'title_cz']
        #exclude = ['title_cz']
        exclude = ['in_watchlist']

        labels = {
            'author': 'Autor',
            'title_orig': 'Originální název',
            'title_cz': 'Český název',
            'num_of_pages': 'Počet stran',
            'description': 'Popis',
            'publisher': 'Nakladatelství',
            'genre': 'Žánr',
            'rating_ours': 'Naše hodnocení',
            'review': 'Recenze',
            'year_of_publishing': 'Rok vydání',
            'time_of_reading': 'Čas čtení',
            'format': 'Format',
        }

        help_texts = {
            'time_of_reading': 'Délka čtení v minutách.',
            'description': 'Popis knihy, stručný obsah nebo jiné detaily.'
        }

        error_messages = {
            'author': {
                'required': 'Tento údaj je povinný.'
            }
        }

    title_orig = CharField(max_length=150,
                           required=True,
                           widget=TextInput(attrs={'class': 'bg-info'}),
                           label="Originální název")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_title_orig(self):
        initial = self.cleaned_data['title_orig']
        return initial.capitalize()

    def clean_title_cz(self):
        initial = self.cleaned_data['title_cz']
        if initial:
            return initial.capitalize()
        return initial


class AuthorModelForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

        labels = {
            'name': 'Jméno',
            'surname': 'Příjmení',
            'date_of_birth': 'Datum narození',
            'date_of_death': 'Datum úmrtí',
            'biography': 'Biografie',
            'nationality': 'Národnost',
            'image': 'Foto autora'
        }

    date_of_birth = DateField(required=False,
                              widget=NumberInput(attrs={'type': 'date'}),
                              label='Datum narození')
    date_of_death = DateField(required=False,
                              widget=NumberInput(attrs={'type': 'date'}),
                              label='Datum úmrtí')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        if initial:
            return initial.capitalize()
        return initial

    def clean_surname(self):
        initial = self.cleaned_data['surname']
        if initial:
            return initial.capitalize()
        return initial

    def clean_date_of_birth(self):
        initial = self.cleaned_data['date_of_birth']
        if initial and initial > date.today():
            raise ValidationError("Datum narození nesmí být v budoucnosti.")
        return initial

    def clean_date_of_death(self):
        initial = self.cleaned_data['date_of_death']
        if initial and initial > date.today():
            raise ValidationError("Datum úmrtí nesmí být v budoucnosti.")
        return initial

    def clean_biography(self):
        initial = self.cleaned_data['biography']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')  # TODO: Věta může končit i ! ?
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        cleaned_data = super().clean()
        initial_name = cleaned_data['name']
        initial_surname = cleaned_data['surname']
        error_message = ''
        if not initial_name and not initial_surname:
            error_message += "Je nutné zadat jméno nebo příjmení (nebo oboje)."
            #raise ValidationError("Je nutné zadat jméno nebo příjmení (nebo oboje).")

        initial_date_of_birth = cleaned_data.get('date_of_birth')
        initial_date_of_death = cleaned_data.get('date_of_death')
        if initial_date_of_birth and initial_date_of_death and initial_date_of_death <= initial_date_of_birth:
            error_message += " Datum úmrtí nesmí být dřív, než datum narození."
            #raise ValidationError("Datum úmrtí nesmí být dřív, než datum narození.")

        if error_message:
            raise ValidationError(error_message)

        return cleaned_data

