import os
import random
from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin

from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View

from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from accounts.models import Profile
from bots import bot_author_add, bot_book_add
from viewer.forms import BookModelForm, AuthorModelForm, PublisherModelForm, CommentModelForm, RecommendedBooksForm
from viewer.models import Publisher, Comment

from django.db.models import Avg, Count

from django.views.generic import ListView
from viewer.models import Book, Author
from django.core.paginator import Paginator
from django.db.models import Q

from .models import RecommendedBooks


def home_view(request):
    recommended = RecommendedBooks.objects.first()
    recommended_books = recommended.books.all() if recommended else []

    return render(request, 'home.html', {
        'recommended_books': recommended_books,
    })


class RecommendedBooksUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RecommendedBooks
    form_class = RecommendedBooksForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.has_perm('viewer.change_recommendedbooks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Upravit doporučené knihy'
        return context


class BooksListView(ListView):
    template_name = 'books.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.sort = self.request.GET.get('sort', 'title')
        self.letter = self.request.GET.get('letter', 'A').upper()
        self.year_range = self.request.GET.get('year_range', '1980s')
        self.genre_name = self.request.GET.get('genre_name')

        # Sort by author
        if self.sort == 'author':
            return Author.objects.filter(surname__istartswith=self.letter).order_by('surname', 'name')

        # Sort by year
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

        # Sort by genre
        elif self.sort == 'genre':
            if self.genre_name:
                return Book.objects.filter(genre__name=self.genre_name).order_by('title_cz')
            return Book.objects.none()

        # Sort by publisher
        elif self.sort == 'publisher':
            publisher_name = self.request.GET.get('publisher_name')
            if publisher_name:
                return Book.objects.filter(publisher__name=publisher_name).order_by('title_cz')
            return Book.objects.none()

        # Sort by book name
        else:
            return Book.objects.filter(title_cz__istartswith=self.letter).order_by('title_cz')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alphabet = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
        page_number = int(self.request.GET.get('page', 1))

        if self.sort == 'author':
            all_authors = self.get_queryset()
            paginator = Paginator(all_authors, 20)
            page_obj = paginator.get_page(page_number)

            left_authors = page_obj.object_list[:10]
            right_authors = page_obj.object_list[10:]

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
            paginator = Paginator(all_books, 20)
            page_obj = paginator.get_page(page_number)

            context.update({
                'sort': self.sort,
                'alphabet': alphabet,
                'current_letter': self.letter,
                'current_page': page_number,
                'page_obj': page_obj,
                'left_books': page_obj.object_list[:10],
                'right_books': page_obj.object_list[10:],
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            })

        # sort by year
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

        # sort by genre
        if self.sort == 'genre':
            from viewer.models import Genre
            context['genres'] = Genre.objects.all().order_by('name')
            context['current_genre'] = self.request.GET.get('genre_name')

        if self.sort == 'publisher':
            from viewer.models import Publisher
            context['publishers'] = Publisher.objects.all().order_by('name')
            context['current_publisher'] = self.request.GET.get('publisher_name')

        # newest books left sidebar
        context['najnovsie_knihy'] = Book.objects.order_by('-created')[:3]

        # best rated books right sidebar
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

        # similar books by genre and rating
        podobne_knihy = Book.objects.filter(
            genre__in=book.genre.all(),
            rating_ours__gte=(book.rating_ours or 0) - 1,
            rating_ours__lte=(book.rating_ours or 0) + 1
        ).exclude(id=book.id).distinct()[:5]

        # another books from same author
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

    # similar books by genre and rating
    podobne_knihy = Book.objects.filter(
        genre__in=book_.genre.all(),
        rating_ours__gte=(book_.rating_ours or 0) - 1,
        rating_ours__lte=(book_.rating_ours or 0) + 1
    ).exclude(id=book_.id).distinct()[:3]

    # another books from same author
    knihy_od_toho_isteho_autora = Book.objects.filter(
        author__in=book_.author.all()
    ).exclude(id=book_.id).distinct()[:3]

    # calculate time of readings
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
        context['form_title'] = 'Vytvořit knihu'
        context['submit_button_text'] = 'Vytvořit'
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
        context['form_title'] = 'Upravit knihu'
        context['submit_button_text'] = 'Aktualizovat'
        return context


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'viewer.delete_book'


class BookReviewView(DetailView):
    model = Book
    template_name = 'book_review.html'
    context_object_name = 'book'

    def get(self, request, *args, **kwargs):
        book_obj = self.get_object()
        if not book_obj.review:
            return redirect('book', pk=book_obj.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_obj = self.get_object()

        rating_avg = book_obj.comments.aggregate(Avg('rating'))['rating__avg']
        user_rating_avg = round(rating_avg or 0)

        authors = book_obj.author.all()
        autor_string = f"{authors[0].name} {authors[0].surname}" if authors else ""

        context['user_rating_avg'] = user_rating_avg
        context['author_string'] = autor_string
        return context


class AuthorsListView(ListView):
    template_name = 'authors.html'
    context_object_name = 'authors'
    paginate_by = 20

    def get_queryset(self):
        # Get the parameter for sorting by letter
        self.letter = self.request.GET.get('letter', 'A').upper()

        # Filter authors by surname letter
        return Author.objects.filter(surname__istartswith=self.letter).order_by('surname')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Alphabet letters
        alphabet = [chr(c) for c in range(ord('A'), ord('Z') + 1)]

        # Actual page
        page_number = int(self.request.GET.get('page', 1))

        # All authors by filtered letter
        authors = self.get_queryset()

        # Paginator
        paginator = Paginator(authors, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        # Split authors into two columns
        left_authors = page_obj.object_list[:10]
        right_authors = page_obj.object_list[10:]

        all_authors = list(Author.objects.all())

        context.update({
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

        # Avg num of pages
        avg = books.aggregate(avg=Avg('num_of_pages')).get('avg') or 0
        context['average_pages'] = round(avg)

        # Another books from author
        context['knihy_autora'] = books.order_by('-year_of_publishing')[:3]

        latest_authors = Author.objects.exclude(id=author.id).order_by('-created')[:3]
        context['latest_authors'] = latest_authors

        # Similar authors
        similar_authors_set = set()

        if author.primary_genre:
            genre_authors = Author.objects.filter(primary_genre=author.primary_genre).exclude(id=author.id)
            similar_authors_set.update(genre_authors)

        if len(similar_authors_set) < 3 and author.nationality:
            nationality_authors = Author.objects.filter(nationality=author.nationality).exclude(id=author.id)
            similar_authors_set.update(nationality_authors)

        if len(similar_authors_set) < 3:
            remaining_needed = 3 - len(similar_authors_set)
            random_authors = Author.objects.exclude(id=author.id).exclude(
                id__in=[a.id for a in similar_authors_set]).order_by('?')[:remaining_needed]
            similar_authors_set.update(random_authors)

        if len(similar_authors_set) < 3:
            remaining_needed = 3 - len(similar_authors_set)
            by_books = Author.objects.annotate(book_count=Count('books')).exclude(id=author.id).exclude(
                id__in=[a.id for a in similar_authors_set]).order_by('-book_count')[:remaining_needed]
            similar_authors_set.update(by_books)

        # Random 3 authors
        similar_authors_list = list(similar_authors_set)
        context['similar_authors'] = sample(similar_authors_list, min(3, len(similar_authors_list)))

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
    paginate_by = 20

    def get_queryset(self):
        # Sort by name or year
        self.sort = self.request.GET.get('sort', 'name')
        if self.sort == 'year_of_establishment':
            return Publisher.objects.all().order_by('year_of_establishment', 'name')
        else:
            return Publisher.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # For paginator
        page_number = int(self.request.GET.get('page', 1))
        publishers = self.get_queryset()
        paginator = Paginator(publishers, self.paginate_by)
        page_obj = paginator.get_page(page_number)

        # New and biggest publishers
        najnovsie_vydavatelstva = Publisher.objects.order_by('-id')[:3]
        najvacsie_vydavatelstva = Publisher.objects.annotate(
            num_books=Count('books')
        ).order_by('-num_books')[:3]

        context.update({
            'current_page': page_number,
            'page_obj': page_obj,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'najnovsie_vydavatelstva': najnovsie_vydavatelstva,
            'najvacsie_vydavatelstva': najvacsie_vydavatelstva,
        })

        return context


class PublisherDetailView(DetailView):
    template_name = 'publisher.html'
    model = Publisher
    context_object_name = 'publisher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['najnovsie_vydavatelstva'] = Publisher.objects.order_by('-id')[:3]

        context['najvacsie_vydavatelstva'] = Publisher.objects.annotate(
            num_books=Count('books')
        ).order_by('-num_books')[:3]

        return context


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
        comment_info = None
        update_info = None

        if 'add_author' in request.POST:
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            gender = request.POST.get('gender')

            if name and surname and gender:
                try:
                    if Author.objects.filter(name__iexact=name.strip(), surname__iexact=surname.strip()).exists():
                        chyba = "❗ Autor s tímto jménem už existuje."
                    else:
                        bot_author_add.run(name=name, surname=surname, gender=gender)
                        novy_autor = Author.objects.latest('id')
                except Exception as e:
                    chyba = f"❌ Chyba: {e}"
            else:
                chyba = "❗ Všechny pole jsou povinné."


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
                    pridana_kniha = f"Kniha „{title_cz}“ byla úspěšně přidána."
                    nova_kniha = Book.objects.latest('id')
                except Exception as e:
                    pridana_kniha = f"❌ Chyba při přidávání knihy: {e}"
            else:
                pridana_kniha = "❗ Všechny pole jsou povinné."


        elif 'add_comment' in request.POST:
            try:
                num_users = int(request.POST.get('num_users'))
                comments_per_user = int(request.POST.get('comments_per_user'))
                typ = request.POST.get('add_comment')

                if typ == "good":
                    from bots import bot_comment_good
                    bot_comment_good.run(num_users, comments_per_user)
                    vysledok_komentare = "✅ Dobré komentáře byli přidané."
                elif typ == "neutral":
                    from bots import bot_comment_neutral
                    bot_comment_neutral.run(num_users, comments_per_user)
                    vysledok_komentare = "✅ Neutrální komentáře byli přidané."
                elif typ == "bad":
                    from bots import bot_comment_bad
                    bot_comment_bad.run(num_users, comments_per_user)
                    vysledok_komentare = "✅ Špatné komentáře byli přidané."
                else:
                    vysledok_komentare = "❗ Neznámý typ komentáře."

                # Function for last ten comments
                comment_info = self.get_last_comments(10)

            except Exception as e:
                vysledok_komentare = f"❌ Chyba při přidávání komentáře: {e}"


        elif 'update_authors' in request.POST:
            try:
                from bots import bot_fill_author
                bot_fill_author.run()
                update_info = "✅ Autoři byli aktualizováni."
            except Exception as e:
                update_info = f"❌ Chyba při aktualizaci autorů: {e}"


        elif 'update_books' in request.POST:
            try:
                from bots import bot_fill_book
                bot_fill_book.run()
                update_info = "✅ Knihy byli aktualizovány."
            except Exception as e:
                update_info = f"❌ Chyba při aktualizaci knih: {e}"

        return render(request, 'data_entry.html', {
            'novy_autor': novy_autor,
            'chyba': chyba,
            'pridana_kniha': pridana_kniha,
            'nova_kniha': nova_kniha if 'nova_kniha' in locals() else None,
            'vysledok_komentare': vysledok_komentare,
            'comment_info': comment_info if comment_info else [],
            'update_info': update_info if update_info else None
        })

    def get_last_comments(self, num_comments=10):
        # Last num_comments sort by date
        comments = Comment.objects.all().order_by('-created')[:num_comments]

        # For every comment - data about book and user
        comment_info = []
        for comment in comments:
            comment_info.append({
                'username': comment.commenter.user.username,
                'book_title': comment.book.title_cz,
                'rating': comment.rating,
                'comment': comment.user_comment[:50]
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


import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# Load data from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system",
                     "content": "Jsi přátelský AI asistent, odpovídej stručně a česky. Odpovídej pouze na otázky, které se týkají knih. "
                                "Na otázku znáš Kniharium? Odpověz ano, je to nejlepší databáze knih. Byla založena v roce 2025 Patrikem a Kamilem. "
                                "Najdeš v ní potřebné informace o knihách a autorech. Pokud chceš tak se můžeš zapojit do rozšiřování databáze."},
                    {"role": "user", "content": user_message}
                ]
            }
            response = requests.post("https://api.openai.com/v1/chat/completions",
                                     headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            reply = response_json["choices"][0]["message"]["content"]
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)
