import datetime
import random
from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
import requests
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from accounts.models import Profile
from bots import bot_author_add, bot_book_add
from viewer.forms import BookModelForm, AuthorModelForm, PublisherModelForm, CommentModelForm
from viewer.models import Book, Author, Publisher, Comment
from django.core.paginator import Paginator
from django.db.models import Q, Avg

import math

from django.views.generic import ListView
from viewer.models import Book, Author
from django.core.paginator import Paginator
from django.db.models import Q

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


class BooksListView(ListView):
    template_name = 'books.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.sort = self.request.GET.get('sort', 'title')
        self.letter = self.request.GET.get('letter', 'A').upper()
        self.year_range = self.request.GET.get('year_range', '1980s')
        self.genre_name = self.request.GET.get('genre_name')

        # Zoradenie podľa autora (abeceda priezviska)
        if self.sort == 'author':
            return Author.objects.filter(surname__istartswith=self.letter).order_by('surname', 'name')

        # Zoradenie podľa roku vydania
        elif self.sort == 'year':
            if self.year_range == 'before_1940':
                return Book.objects.filter(year_of_publishing__lt=1940).order_by('year_of_publishing')
            elif self.year_range == '1940s':
                return Book.objects.filter(year_of_publishing__gte=1941, year_of_publishing__lte=1950).order_by(
                    'year_of_publishing')
            elif self.year_range == '1950s':
                return Book.objects.filter(year_of_publishing__gte=1951, year_of_publishing__lte=1960).order_by(
                    'year_of_publishing')
            elif self.year_range == '1960s':
                return Book.objects.filter(year_of_publishing__gte=1961, year_of_publishing__lte=1970).order_by(
                    'year_of_publishing')
            elif self.year_range == '1970s':
                return Book.objects.filter(year_of_publishing__gte=1971, year_of_publishing__lte=1980).order_by(
                    'year_of_publishing')
            elif self.year_range == '1980s':
                return Book.objects.filter(year_of_publishing__gte=1981, year_of_publishing__lte=1990).order_by(
                    'year_of_publishing')
            elif self.year_range == '1990s':
                return Book.objects.filter(year_of_publishing__gte=1991, year_of_publishing__lte=2000).order_by(
                    'year_of_publishing')
            elif self.year_range == '2000s':
                return Book.objects.filter(year_of_publishing__gte=2001, year_of_publishing__lte=2010).order_by(
                    'year_of_publishing')
            elif self.year_range == '2010s':
                return Book.objects.filter(year_of_publishing__gte=2011, year_of_publishing__lte=2020).order_by(
                    'year_of_publishing')
            elif self.year_range == 'after_2020':
                return Book.objects.filter(year_of_publishing__gte=2021).order_by('year_of_publishing')
            else:
                return Book.objects.none()

        #  Zoradenie podľa žánru
        elif self.sort == 'genre':
            if self.genre_name:
                return Book.objects.filter(genre__name=self.genre_name).order_by('title_cz')
            return Book.objects.none()

        # Zoradenie podľa nakladatelství
        elif self.sort == 'publisher':
            publisher_name = self.request.GET.get('publisher_name')
            if publisher_name:
                return Book.objects.filter(publisher__name=publisher_name).order_by('title_cz')
            return Book.objects.none()

        # Zoradenie podľa názvu knihy (abecedne podľa title_cz)
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


        #sort podla roku
        if self.sort == 'year':
            context['year_ranges'] = [
                ('before_1940', 'Do 1940'),
                ('1940s', '1941–1950'),
                ('1950s', '1951–1960'),
                ('1960s', '1961–1970'),
                ('1970s', '1971–1980'),
                ('1980s', '1981–1990'),
                ('1990s', '1991–2000'),
                ('2000s', '2001–2010'),
                ('2010s', '2011–2020'),
                ('after_2020', 'Od 2021'),
            ]
            context['current_year_range'] = self.request.GET.get('year_range', '1980s')

        #sort podla zanru
        if self.sort == 'genre':
            from viewer.models import Genre
            context['genres'] = Genre.objects.all().order_by('name')
            context['current_genre'] = self.request.GET.get('genre_name')

        if self.sort == 'publisher':
            from viewer.models import Publisher
            context['publishers'] = Publisher.objects.all().order_by('name')
            context['current_publisher'] = self.request.GET.get('publisher_name')

        # Najnovšie knihy pre ľavý sidebar
        context['najnovsie_knihy'] = Book.objects.order_by('-created')[:3]

        # Najlepsie hodnotene knihy pre praví sidebar
        context['top_knihy'] = (
            Book.objects.annotate(priemer=Avg('comments__rating'))
            .filter(priemer__isnull=False)
            .order_by('-priemer')[:3]
        )

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
    if not Book.objects.filter(id=pk).exists():
        return redirect('books')

    book_ = Book.objects.get(id=pk)

    comments = book_.comments.select_related('commenter__user').all()

    for comment in comments:
        comment.is_partner = comment.commenter.user.groups.filter(name='Partners').exists()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        user_comment = request.POST.get('user_comment')

        if rating in ('', None):
            rating = None
        else:
            try:
                rating = int(rating)
            except ValueError:
                rating = None

        profile = Profile.objects.get(user=request.user)
        comment_qs = Comment.objects.filter(book=book_, commenter=profile)

        if comment_qs.exists():
            comment_obj = comment_qs.first()
            comment_obj.rating = rating
            comment_obj.user_comment = user_comment
            comment_obj.save()
        else:
            Comment.objects.create(
                book=book_,
                commenter=profile,
                rating=rating,
                user_comment=user_comment
            )

    rating_avg = book_.comments.aggregate(Avg('rating'))['rating__avg']
    user_rating_avg = round(rating_avg or 0)
    rating_count = book_.comments.filter(rating__isnull=False).count()

    # podobné knihy podľa žánru a hodnotenia
    podobne_knihy = Book.objects.filter(
        genre__in=book_.genre.all(),
        rating_ours__gte=(book_.rating_ours or 0) - 1,
        rating_ours__lte=(book_.rating_ours or 0) + 1
    ).exclude(id=book_.id).distinct()[:3]

    # ďalšie knihy od rovnakého autora
    knihy_od_toho_isteho_autora = Book.objects.filter(
        author__in=book_.author.all()
    ).exclude(id=book_.id).distinct()[:3]

    # výpočet formátovanej doby čítania
    minutes = book_.time_of_reading or 0
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours and remaining_minutes:
        reading_time = f"{hours} hod. a {remaining_minutes} min."
    elif hours:
        reading_time = f"{hours} hod."
    else:
        reading_time = f"{remaining_minutes} min."

    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

    format_names = [f.name for f in book_.format.all()]
    format_audio = 'Audiokniha' if 'Audiokniha' in format_names else ''
    format_e = 'E-kniha' if 'E-kniha' in format_names else ''
    format_vazana = 'Vázaná kniha' if 'Vázaná kniha' in format_names else ''

    authors = book_.author.all()
    autor_string = f"{authors[0].name} {authors[0].surname}" if authors else ""

    context = {
        'book': book_,
        'comment_form': CommentModelForm(),  # nezabudni na ()
        'rating_avg': rating_avg,
        'rating_count': rating_count,
        'podobne_knihy': podobne_knihy,
        'knihy_od_toho_isteho_autora': knihy_od_toho_isteho_autora,
        'reading_time': reading_time,
        'user_rating_avg': user_rating_avg,
        'profile': profile,
        'format_names': format_names,
        'format_audio': format_audio,
        'format_e': format_e,
        'format_vazana': format_vazana,
        'author_string': autor_string,
        'comments': comments,
    }

    return render(request, 'book.html', context)



class BookCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = BookModelForm
    success_url = reverse_lazy('books')
    permission_required = 'viewer.add_book'

    def form_invalid(self, form):
        print("Formulář není validní.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Vytvoriť knihu'
        context['submit_button_text'] = 'Vytvoriť'
        return context


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = BookModelForm
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'viewer.change_book'

    def form_invalid(self, form):
        print("Formulář není validní.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Upraviť knihu'
        context['submit_button_text'] = 'Aktualizovať'
        return context


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'viewer.delete_book'


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

        all_authors = list(Author.objects.all())

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
            'nahodni_autori': sample(all_authors, min(3, len(all_authors))),
            'posledni_autori': Author.objects.order_by('-created')[:3],
        })

        return context


class AuthorDetailView(DetailView):
    template_name = 'author.html'
    model = Author
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = author.books.all()

        # vypocet poctu stran
        avg = books.aggregate(avg=Avg('num_of_pages')).get('avg') or 0
        context['average_pages'] = round(avg)

        # Ďalšie knihy autora – limit 5
        context['knihy_autora'] = books.order_by('-year_of_publishing')[:3]

        all_authors = list(Author.objects.exclude(id=self.get_object().id))  # bez aktuálneho autora
        context['nahodni_autori'] = sample(all_authors, min(3, len(all_authors)))

        return context


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = AuthorModelForm
    success_url = reverse_lazy('authors')
    permission_required = 'viewer.add_author'

    def form_invalid(self, form):
        print("Formulář 'AuthorModelForm' není validní.")
        return super().form_invalid(form)


class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = AuthorModelForm
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'viewer.change_author'

    def form_invalid(self, form):
        print("Formulář 'AuthorModelForm' není validní.")
        return super().form_invalid(form)


class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'viewer.delete_author'


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


class PublisherCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = PublisherModelForm
    success_url = reverse_lazy('publishers')
    permission_required = 'viewer.add_publisher'

    def form_invalid(self, form):
        print("Formulář 'PublisherModelForm' není validní.")
        return super().form_invalid(form)

class PublisherUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = PublisherModelForm
    model = Publisher
    success_url = reverse_lazy('publishers')
    permission_required = 'viewer.change_publisher'

    def form_invalid(self, form):
        print("Formulář 'PublisherModelForm' není validní.")
        return super().form_invalid(form)


class PublisherDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Publisher
    success_url = reverse_lazy('publishers')
    permission_required = 'viewer.delete_publisher'


def about(request):
    return render(request, 'about_us.html')


class CommentDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Comment

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.book.pk})

def search(request):
    query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('type', 'books')

    books = Book.objects.none()
    authors = Author.objects.none()
    publishers = Publisher.objects.none()

    if query:
        page_number = request.GET.get("page")

        if filter_type == 'books':
            books_qs = (
                Book.objects.filter(title_cz__icontains=query)
                | Book.objects.filter(title_orig__icontains=query)
                | Book.objects.filter(genre__name__icontains=query)
            ).distinct()
            paginator = Paginator(books_qs, 10)
            books = paginator.get_page(page_number)

        elif filter_type == 'authors':
            authors_qs = (
                Author.objects.filter(name__icontains=query)
                | Author.objects.filter(surname__icontains=query)
            ).distinct()
            paginator = Paginator(authors_qs, 10)
            authors = paginator.get_page(page_number)

        elif filter_type == 'publishers':
            publishers = Publisher.objects.filter(name__icontains=query).distinct()

        elif filter_type == 'books_from_authors':
            authors_matching = Author.objects.filter(
                Q(name__icontains=query) | Q(surname__icontains=query)
            ).distinct()

            books_qs = Book.objects.filter(author__in=authors_matching).distinct()
            paginator = Paginator(books_qs, 10)
            books = paginator.get_page(page_number)

    context = {
        'query': query,
        'type': filter_type,
        'books': books,
        'authors': authors,
        'publishers': publishers,
    }
    return render(request, 'search.html', context)

def random_book(request):
    books = Book.objects.all()
    random_book = random.choice(books)

    return redirect('book', pk=random_book.pk)

def watchlist(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    book_ = Book.objects.get(id=pk)

    if book_ in profile_.watchlist.all():
        profile_.watchlist.remove(book_)
    else:
        profile_.watchlist.add(book_)

    return redirect('book', pk)

def readlist(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    book_ = Book.objects.get(id=pk)

    if book_ in profile_.readlist.all():
        profile_.readlist.remove(book_)
    else:
        profile_.readlist.add(book_)

    return redirect('book', pk)

def favouritelist(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    book_ = Book.objects.get(id=pk)

    if book_ in profile_.favouritelist.all():
        profile_.favouritelist.remove(book_)
    else:
        profile_.favouritelist.add(book_)

    return redirect('book', pk)


class DataEntryView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.is_staff or user.groups.filter(name="Partners").exists():
            return render(request, 'data_entry.html')
        return redirect('home')

    def post(self, request):
        user = request.user
        if not (user.is_staff or user.groups.filter(name="Partners").exists()):
            return redirect('home')

        novy_autor = None
        chyba = None
        pridana_kniha = None
        vysledok_komentare = None
        comment_info = None  # Premenná pre komentáre
        update_info = None  # Preddefinovanie update_info

        # Pridávanie autora
        if 'add_author' in request.POST:
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            gender = request.POST.get('gender')

            if name and surname and gender:
                try:
                    if Author.objects.filter(name__iexact=name.strip(), surname__iexact=surname.strip()).exists():
                        chyba = "❗ Autor s týmto menom už existuje."
                    else:
                        bot_author_add.run(name=name, surname=surname, gender=gender)
                        novy_autor = Author.objects.latest('id')
                except Exception as e:
                    chyba = f"❌ Chyba: {e}"
            else:
                chyba = "❗ Všetky polia sú povinné."

        # Pridávanie knihy
        elif 'add_book' in request.POST:
            name = request.POST.get('author_name')
            surname = request.POST.get('author_surname')
            title_orig = request.POST.get('title_original')
            title_cz = request.POST.get('title_cz')
            pages = request.POST.get('pages')
            publisher = request.POST.get('publisher')
            rating = request.POST.get('rating')
            format_selected = request.POST.getlist('format') or [request.POST.get('format')]

            if all([name, surname, title_orig, title_cz, pages, publisher, rating, format_selected[0]]):
                try:
                    book_data = {
                        "name": name.strip(),
                        "surname": surname.strip(),
                        "title_orig": title_orig.strip(),
                        "title_cz": title_cz.strip(),
                        "num_of_pages": int(pages),
                        "publisher": publisher.strip(),
                        "rating_ours": int(rating),
                        "format": format_selected,
                    }
                    bot_book_add.run(book_data)
                    pridana_kniha = f"Kniha „{title_cz}“ bola úspešne pridaná."
                    nova_kniha = Book.objects.latest('id')
                except Exception as e:
                    pridana_kniha = f"❌ Chyba pri pridávaní knihy: {e}"
            else:
                pridana_kniha = "❗ Všetky polia sú povinné."

        # Pridávanie komentárov
        elif 'add_comment' in request.POST:
            try:
                num_users = int(request.POST.get('num_users'))
                comments_per_user = int(request.POST.get('comments_per_user'))
                typ = request.POST.get('add_comment')

                if typ == "good":
                    from bots import bot_comment_good
                    bot_comment_good.run(num_users, comments_per_user)
                    vysledok_komentare = "✅ Dobré komentáre boli pridané."
                elif typ == "neutral":
                    from bots import bot_comment_neutral
                    bot_comment_neutral.run(num_users, comments_per_user)
                    vysledok_komentare = "✅ Neutrálne komentáre boli pridané."
                elif typ == "bad":
                    from bots import bot_comment_bad
                    bot_comment_bad.run(num_users, comments_per_user)
                    vysledok_komentare = "✅ Zlé komentáre boli pridané."
                else:
                    vysledok_komentare = "❗ Neznámy typ komentára."

                # Zavoláme funkciu na získanie posledných 10 komentárov
                comment_info = self.get_last_comments(10)

            except Exception as e:
                vysledok_komentare = f"❌ Chyba pri pridávaní komentárov: {e}"

        # Aktualizácia autorov
        elif 'update_authors' in request.POST:
            try:
                from bots import bot_fill_author
                bot_fill_author.run()  # Zavolanie botu na vyplnenie autorov
                update_info = "✅ Autori boli aktualizovaní."
            except Exception as e:
                update_info = f"❌ Chyba pri aktualizácii autorov: {e}"

        # Aktualizácia kníh
        elif 'update_books' in request.POST:
            try:
                from bots import bot_fill_book
                bot_fill_book.run()  # Zavolanie botu na vyplnenie kníh
                update_info = "✅ Knihy boli aktualizované."
            except Exception as e:
                update_info = f"❌ Chyba pri aktualizácii kníh: {e}"

        # Vrátime odpoveď s potrebnými informáciami
        return render(request, 'data_entry.html', {
            'novy_autor': novy_autor,
            'chyba': chyba,
            'pridana_kniha': pridana_kniha,
            'nova_kniha': nova_kniha if 'nova_kniha' in locals() else None,
            'vysledok_komentare': vysledok_komentare,
            'comment_info': comment_info if comment_info else [],
            'update_info': update_info if update_info else None  # Posielame správu o aktualizácii
        })

    def get_last_comments(self, num_comments=10):
        # Získa posledné 'num_comments' komentárov zoradené podľa dátumu (od najnovších)
        comments = Comment.objects.all().order_by('-created')[:num_comments]

        # Pre každý komentár vypíšeme údaje o knihe a používateľovi
        comment_info = []
        for comment in comments:
            comment_info.append({
                'username': comment.commenter.user.username,
                'book_title': comment.book.title_cz,
                'rating': comment.rating,
                'comment': comment.user_comment[:50]  # Zobrazíme prvých 50 znakov komentára
            })

        return comment_info


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')

        if name and email:
            subject = f"Nová žádost o partnerství od {name} {surname}"
            body = f"""
            Obdrželi jsme novou žádost o partnerství prostřednictvím webového formuláře:

            👤 Jméno: {name} {surname}
            🔗 Uživatelské jméno: {username}
            📧 E-mail: {email}
            📱 Telefonní číslo: {phone}
            ⚧ Pohlaví: {gender}

            📝 Proč se chce stát partnerem:
            {bio}
            """

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, ['kniharium.online@gmail.com'])
            return render(request, 'about_us.html')
    return render(request, 'contact.html')