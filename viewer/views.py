from django.shortcuts import render
from django.views.generic import ListView, DetailView

from viewer.models import Book


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




