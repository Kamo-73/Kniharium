import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import CharField, PasswordInput, DateField, NumberInput, \
    Textarea, ModelForm, DateInput

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2']

        labels = {
            'username': 'Uživatelské jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'E-mail',
        }

    password1 = CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo'}),
        label='Heslo'
    )

    password2 = CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo znovu'}),
        label='Heslo znovu'
    )

    date_of_birth = DateField(
        widget=NumberInput(attrs={'type': 'date'}),
        label='Datum narození',
        required=False
    )

    biography = CharField(
        widget=Textarea,
        label='Biografie',
        required=False
    )

    phone = CharField(
        label='Telefonní číslo',
        required=False
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)

        date_of_birth = self.cleaned_data.get('date_of_birth')
        biography = self.cleaned_data.get('biography')
        phone = self.cleaned_data.get('phone')
        profile = Profile(
            user=user,
            date_of_birth=date_of_birth,
            biography=biography,
            phone=phone
        )
        if commit:
            profile.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        date_of_birth = cleaned_data.get('date_of_birth')

        if password1 and password1 != password2:
            raise ValidationError("Hesla se neshodují.")
        if date_of_birth and date_of_birth > datetime.date.today():
            raise ValidationError("Datum narození nesmí být v budoucnosti.")
        return cleaned_data


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Uživatelské jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'E-mail',
        }


class ProfileModelForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'biography', 'phone']
        labels = {
            'date_of_birth': 'Datum narození',
            'biography': 'Biografie',
            'phone': 'Telefonní číslo',
        }
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'biography': Textarea(attrs={'rows': 4}),
        }
