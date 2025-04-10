from django.db import models

from django.db.models import Model, CharField, DateField, TextField, ForeignKey, SET_NULL, DateTimeField, ImageField, \
    URLField, ManyToManyField, IntegerField


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




class Format(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"Format(name={self.name})"

    def __str__(self):
        return self.name


class Publisher(Model):
    name = CharField(max_length=150, null=False, blank=False, unique=True)
    information = TextField(null=True, blank=True)
    link = URLField(max_length=200, null=True, blank=True, unique=True)
    date_of_establishment = DateField(null=True, blank=True)
    date_of_dissolution = DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"Publisher(name={self.name})"

    def __str__(self):
        return self.name


class Book(Model):
    author = ManyToManyField(Author, blank=False, related_name='books')
    title_orig = CharField(max_length=150, null=False, blank=False)
    title_cz = CharField(max_length=150, null=False, blank=False)
    num_of_pages = IntegerField(null=False, blank=False)
    description = TextField(null=True, blank=True)
    publisher = ForeignKey(Publisher, null=True, blank=True, on_delete=SET_NULL, related_name='books')
    genre = ManyToManyField(Genre, blank=False, related_name='books')
    rating_ours = IntegerField(null=True, blank=True)
    review = TextField(null=True, blank=True)
    publishing_date = DateField(null=True, blank=True)
    time_of_reading = IntegerField(null=True, blank=True)
    format = ManyToManyField(Format, blank=False, related_name='books')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    image = ImageField(upload_to='images/', default=None, null=True, blank=True)

    class Meta:
        ordering = ['title_cz', 'title_orig', 'publishing_date']

    def __repr__(self):
        return f"Book(title_cz={self.title_cz}, title_orig={self.title_orig}, author={self.author}, publishing_date={self.publishing_date})"

    def __str__(self):
        authors = ", ".join([f"{author.name} {author.surname}" for author in self.author.all()])
        return f"{self.title_cz} ({authors})"


class Award(Model):
    name = CharField(max_length=150, null=False, blank=False, unique=True)
    author = ManyToManyField(Author, blank=True, related_name='awards')
    book = ManyToManyField(Book, blank=True, related_name='awards')
    year = IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name', 'year']

    def __repr__(self):
        return f"Book(name={self.name}, year={self.year})"

    def __str__(self):
        return f"{self.name}"






