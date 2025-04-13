from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from viewer.models import Book, Author, Publisher
from django.core.paginator import Paginator
from django.db.models import Q

def home_view(request):
    recommended_titles = [
        "Chladnokrevně",
        "Mesiáš Duny",
        "Osvícení",
        "Pán prstenů",
        "Hobit",
        "To",
        "Řbitov zviřátek",
        "Hellstromův úl",
        "Cíl: Prázdnota",
        "Svědectví",
    ]

    query = Q()
    for title in recommended_titles:
        query |= Q(title_cz__iexact=title)

    recommended_books = Book.objects.filter(query).prefetch_related('author')

    return render(request, 'home.html', {
        'recommended_books': recommended_books,
    })


from django.views.generic import ListView
from viewer.models import Book, Author
from django.core.paginator import Paginator
from django.db.models import Q

from django.views.generic import ListView
from viewer.models import Book, Author
from django.core.paginator import Paginator
from django.db.models import Q

class BooksListView(ListView):
    template_name = 'books.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.sort = self.request.GET.get('sort', 'title')
        self.letter = self.request.GET.get('letter', 'A').upper()

        if self.sort == 'author':
            return Author.objects.filter(surname__istartswith=self.letter).order_by('surname', 'name')
        else:
            return Book.objects.filter(title_cz__istartswith=self.letter).order_by('title_cz')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alphabet = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
        page_number = int(self.request.GET.get('page', 1))

        if self.sort == 'author':
            all_authors = self.get_queryset()
            paginator = Paginator(all_authors, 40)
            page_obj = paginator.get_page(page_number)

            left_authors = page_obj.object_list[:20]
            right_authors = page_obj.object_list[20:]

            context.update({
                'sort': self.sort,
                'alphabet': alphabet,
                'current_letter': self.letter,
                'current_page': page_number,
                'page_obj': page_obj,
                'left_authors': left_authors,
                'right_authors': right_authors,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            })
        else:
            all_books = self.get_queryset()
            paginator = Paginator(all_books, 40)
            page_obj = paginator.get_page(page_number)

            context.update({
                'sort': self.sort,
                'alphabet': alphabet,
                'current_letter': self.letter,
                'current_page': page_number,
                'page_obj': page_obj,
                'left_books': page_obj.object_list[:20],
                'right_books': page_obj.object_list[20:],
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            })

        return context

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



