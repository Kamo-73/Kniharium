from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from viewer.models import Book, Author, Publisher


def home(request):
    return render(request, 'home.html')



class BooksListView(ListView):
    template_name = 'books.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 10


class BookDetailView(DetailView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'book'


class AuthorsListView(ListView):
    template_name = 'authors.html'
    model = Author
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetailView(DetailView):
    template_name = 'author.html'
    model = Author
    context_object_name = 'author'


class PublishersListView(ListView):
    template_name = 'publishers.html'
    model = Publisher
    context_object_name = 'publishers'
    paginate_by = 10


class PublisherDetailView(DetailView):
    template_name = 'publisher.html'
    model = Publisher
    context_object_name = 'publisher'


def about(request):
    return render(request, 'about_us.html')





