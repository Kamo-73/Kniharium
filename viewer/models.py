from django.db import models
from django.db.models import Model, CharField, DateField, TextField, ForeignKey, SET_NULL, DateTimeField, ImageField


class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"Genre(name={self.name})"

    def __str__(self):
        return self.name


class Nationality(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Nationalities"

    def __repr__(self):
        return f"Nationality(name={self.name})"

    def __str__(self):
        return self.name


class Author(Model):
    name = CharField(max_length=32, null=True, blank=True)
    surname = CharField(max_length=50, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)
    nationality = ForeignKey(Nationality, null=True, blank=True, on_delete=SET_NULL, related_name='authors')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    image = ImageField(upload_to='images/', default=None, null=True, blank=True)

    class Meta:
        ordering = ['surname', 'name', 'date_of_birth']

    def __repr__(self):
        return f"Author(name={self.name}, surname={self.surname}, date_of_birth={self.date_of_birth})"

    def __str__(self):
        if self.date_of_birth:
            return f"{self.name} {self.surname} ({self.date_of_birth.year})"
        return f"{self.name} {self.surname}"
