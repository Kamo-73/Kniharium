import re
from datetime import date

from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput, DateField, NumberInput, IntegerField, Form

from viewer.models import Book, Author, Publisher, Comment


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

    def clean_num_of_pages(self):
        initial = self.cleaned_data['num_of_pages']
        if initial is not None and initial <= 0:
            raise ValidationError("Počet stran musí být větší než nula.")
        return initial

    def clean_rating_ours(self):
        initial = self.cleaned_data.get('rating_ours')
        if initial is not None and initial not in [1, 2, 3, 4, 5]:
            raise ValidationError("Hodnocení musí být v rozmezí 1–5.")
        return initial

    def clean_year_of_publishing(self):
        initial = self.cleaned_data.get('year_of_publishing')
        if initial is not None and initial <= 0 or initial > date.today().year:
            raise ValidationError("Rok vydání musí být větší než nula a nesmí být v budoucnosti.")
        return initial

    def clean_time_of_reading(self):
        initial = self.cleaned_data.get('time_of_reading')
        if initial is not None and initial <= 0:
            raise ValidationError("Čas čtení musí být větší než nula.")
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
        if initial is not None and initial > date.today():
            raise ValidationError("Datum narození nesmí být v budoucnosti.")
        return initial

    def clean_date_of_death(self):
        initial = self.cleaned_data['date_of_death']
        if initial is not None and initial > date.today():
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


class PublisherModelForm(ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'

        labels = {
            'name': 'Název',
            'information': 'Informace',
            'link': 'Link',
            'year_of_establishment': 'Rok založení',
            'year_of_dissolution': 'Rok ukončení činnosti',
            }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        if initial:
            return initial.capitalize()
        return initial

    def clean_year_of_establishment(self):
        initial = self.cleaned_data.get('year_of_establishment')
        if initial is not None and initial < 1440:
            raise ValidationError("Rok založení nesmí být dřívější než 1440.")
        if initial is not None and initial > date.today().year:
            raise ValidationError("Rok založení nesmí být v budoucnosti.")
        return initial

    def clean_year_of_dissolution(self):
        initial = self.cleaned_data.get('year_of_dissolution')
        if initial is not None and initial > date.today().year:
            raise ValidationError("Datum ukončení činnosti nesmí být v budoucnosti.")
        return initial

    def clean_information(self):
        initial = self.cleaned_data['information']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')  # TODO: Věta může končit i ! ?
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        cleaned_data = super().clean()
        initial_name = cleaned_data['name']
        error_message = ''
        if not initial_name:
            error_message += "Je nutné zadat název nakladatelství."

        initial_year_of_establishment = cleaned_data.get('year_of_establishment')
        initial_year_of_dissolution = cleaned_data.get('year_of_dissolution')
        if initial_year_of_establishment and initial_year_of_dissolution and initial_year_of_dissolution < initial_year_of_establishment:
            error_message += " Rok ukončení činnosti nesmí být dřív, než rok založení."

        if error_message:
            raise ValidationError(error_message)

        return cleaned_data


class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['rating', 'user_comment']
        labels = {
            'rating': 'Hodnocení',
            'user_comment': 'Komentář'
        }
    rating = IntegerField(min_value=1, max_value=5, required=False)

    def clean_rating(self):
        initial = self.cleaned_data['rating']
        if initial is not None and initial not in [1, 2, 3, 4, 5]:
            raise ValidationError("Hodnocení musí být v rozmezí 1–5.")
        return initial

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'width: 100%;'
            })







