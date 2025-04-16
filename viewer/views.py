from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from accounts.models import Profile
from viewer.forms import BookModelForm, AuthorModelForm, PublisherModelForm, CommentModelForm
from viewer.models import Book, Author, Publisher, Comment
from django.core.paginator import Paginator
from django.db.models import Q, Avg


def home_view(request):
    recommended_titles = [
        "Andělé a démoni",
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        # podobné knihy podľa žánru a hodnotenia
        podobne_knihy = Book.objects.filter(
            genre__in=book.genre.all(),
            rating_ours__gte=(book.rating_ours or 0) - 1,
            rating_ours__lte=(book.rating_ours or 0) + 1
        ).exclude(id=book.id).distinct()[:5]

        # ďalšie knihy od rovnakého autora
        knihy_od_toho_isteho_autora = Book.objects.filter(
            author__in=book.author.all()
        ).exclude(id=book.id).distinct()[:5]

        context['podobne_knihy'] = podobne_knihy
        context['knihy_od_toho_isteho_autora'] = knihy_od_toho_isteho_autora
        return context

def book(request, pk):
    if Book.objects.filter(id=pk).exists():
        book_ = Book.objects.get(id=pk)
        if request.method == 'POST':
            # zpracování formuláře
            rating = request.POST.get('rating')
            user_comment = request.POST.get('user_comment')
            # pokud již uživatel tento film hodnotil, tak upravíme původní review
            if Comment.objects.filter(book=book_, commenter=Profile.objects.get(user=request.user)).exists():
                user_comment_ = Comment.objects.get(book=book_, commenter=Profile.objects.get(user=request.user))
                user_comment_.rating = rating
                user_comment_.user_comment = user_comment
                user_comment_.save()
            else:
                Comment.objects.create(
                    book=book_,
                    commenter=Profile.objects.get(user=request.user),
                    rating=rating,
                    user_comment=user_comment
                )
        rating_avg = book_.comments.aggregate(Avg('rating'))['rating__avg']
        rating_count = book_.comments.filter(rating__isnull=False).count()
        context = {'book': book_,
                   'comment_form': CommentModelForm,
                   'rating_avg': rating_avg,
                   'rating_count': rating_count}
        return render(request, 'book.html', context)
    return redirect('books')














class BookCreateView(CreateView):
    template_name = 'form.html'
    form_class = BookModelForm
    success_url = reverse_lazy('books')
    #permission_required = 'viewer.add_book'

    def form_invalid(self, form):
        print("Formulář není validní.")
        return super().form_invalid(form)


class BookUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = BookModelForm
    model = Book
    success_url = reverse_lazy('books')
    #permission_required = 'viewer.change_book'

    def form_invalid(self, form):
        print("Formulář není validní.")
        return super().form_invalid(form)


class BookDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Book
    success_url = reverse_lazy('books')
    #permission_required = 'viewer.delete_book'


class AuthorsListView(ListView):
    template_name = 'authors.html'
    context_object_name = 'authors'
    paginate_by = 40  # Počet autorov na stránku

    def get_queryset(self):
        # Získame parameter pre triedenie podľa písmena
        self.letter = self.request.GET.get('letter', 'A').upper()

        # Filtrovanie autorov podľa písmena priezviska
        return Author.objects.filter(surname__istartswith=self.letter).order_by('surname')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Zoznam písmen abecedy
        alphabet = [chr(c) for c in range(ord('A'), ord('Z') + 1)]

        # Získanie aktuálnej stránky
        page_number = int(self.request.GET.get('page', 1))

        # Získanie všetkých autorov podľa filtrovaného písmena
        authors = self.get_queryset()

        # Paginator pre stránkovanie
        paginator = Paginator(authors, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        # Rozdelenie autorov do dvoch stĺpcov
        left_authors = page_obj.object_list[:20]
        right_authors = page_obj.object_list[20:]

        context.update({
            'alphabet': alphabet,  # Pre abecedu
            'current_letter': self.letter,  # Aktuálne zvolené písmeno
            'current_page': page_number,  # Aktuálna stránka
            'page_obj': page_obj,  # Aktuálny objekt stránkovania
            'left_authors': left_authors,  # Autori pre ľavý stĺpec
            'right_authors': right_authors,  # Autori pre pravý stĺpec
            'has_previous': page_obj.has_previous(),  # Predchádzajúca stránka
            'has_next': page_obj.has_next(),  # Ďalšia stránka
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            # Predchádzajúce číslo stránky
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,  # Ďalšie číslo stránky
        })

        return context


class AuthorDetailView(DetailView):
    template_name = 'author.html'
    model = Author
    context_object_name = 'author'


class AuthorCreateView(CreateView):
    template_name = 'form.html'
    form_class = AuthorModelForm
    success_url = reverse_lazy('authors')
    #permission_required = 'viewer.add_author'

    def form_invalid(self, form):
        print("Formulář 'AuthorModelForm' není validní.")
        return super().form_invalid(form)


class AuthorUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = AuthorModelForm
    model = Author
    success_url = reverse_lazy('authors')
    #permission_required = 'viewer.change_author'

    def form_invalid(self, form):
        print("Formulář 'AuthorModelForm' není validní.")
        return super().form_invalid(form)


class AuthorDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Author
    success_url = reverse_lazy('authors')
    #permission_required = 'viewer.delete_author'


class PublishersListView(ListView):
    template_name = 'publishers.html'
    context_object_name = 'publishers'
    paginate_by = 20  # 20 vydavateľstiev na stránku

    def get_queryset(self):
        # Filtrovanie podľa názvu alebo roku založenia
        self.sort = self.request.GET.get('sort', 'name')
        if self.sort == 'year_of_establishment':
            return Publisher.objects.all().order_by('year_of_establishment', 'name')
        else:
            return Publisher.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pre stránkovanie
        page_number = int(self.request.GET.get('page', 1))
        publishers = self.get_queryset()
        paginator = Paginator(publishers, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        context.update({
            'current_page': page_number,
            'page_obj': page_obj,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        })

        return context

class PublisherDetailView(DetailView):
    template_name = 'publisher.html'
    model = Publisher
    context_object_name = 'publisher'


class PublisherCreateView(CreateView):
    template_name = 'form.html'
    form_class = PublisherModelForm
    success_url = reverse_lazy('publishers')
    #permission_required = 'viewer.add_author'

    def form_invalid(self, form):
        print("Formulář 'PublisherModelForm' není validní.")
        return super().form_invalid(form)

class PublisherUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = PublisherModelForm
    model = Publisher
    success_url = reverse_lazy('publishers')
    #permission_required = 'viewer.change_author'

    def form_invalid(self, form):
        print("Formulář 'PublisherModelForm' není validní.")
        return super().form_invalid(form)


class PublisherDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Publisher
    success_url = reverse_lazy('publishers')
    #permission_required = 'viewer.delete_author'


def about(request):
    return render(request, 'about_us.html')



