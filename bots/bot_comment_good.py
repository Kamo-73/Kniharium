import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

from django.contrib.auth.models import User
from viewer.models import Book, Comment
from accounts.models import Profile

good_males = [
    ("kvietok23", "Jan Novák"),
    ("LibertyFox", "Tomáš Svoboda"),
    ("spoi", "Lukáš Dvořák"),
    ("ShadowRider", "Petr Marek"),
    ("Tranzit7", "Martin Procházka"),
]

good_females = [
    ("lilie.sky", "Anna Novotná"),
    ("kat_blackcat", "Kateřina Černá"),
    ("LucidEcho", "Lucie Horáková"),
    ("vera.nika", "Veronika Králová"),
    ("SilentStar9", "Tereza Pokorná"),
]

good_male_comments = [
    "Skvělá kniha, četl jsem ji jedním dechem.",
    "Byl jsem příjemně překvapený, jak mě děj vtáhl.",
    "Autor mě vtáhl do příběhu hned na začátku.",
    "Ocenil jsem propracované postavy a promyšlený vývoj děje.",
    "Dlouho mě nic takhle nezaujalo – výborné čtení.",
    "Měl jsem pocit, že jsem tam s nimi – silně napsané.",
    "Hodně jsem si užil atmosféru a styl psaní.",
    "Po dočtení jsem o příběhu ještě dlouho přemýšlel.",
    "Přiznávám, místy mě to dojalo.",
    "Nečekal jsem, že mě tahle kniha tak zasáhne.",
]

good_female_comments = [
    "Tahle kniha mě naprosto pohltila, ani jsem si nevšimla, že je půlnoc.",
    "Četla jsem to s radostí – lehké, ale zároveň hluboké.",
    "Byla to krásná kombinace emocí a přemýšlení, přesně moje tempo.",
    "Zamilovala jsem si hlavní postavu, takhle silné ženy v literatuře miluju.",
    "Příběh mi zněl v hlavě ještě několik dní po dočtení.",
    "Dlouho jsem neprožívala každou stránku tak intenzivně jako tady.",
    "Styl psaní byl jemný a pritom úderný – moc mi sedl.",
    "Nečekala jsem tolik emocí, ale padly mi přesně na srdce.",
    "Díky téhle knize jsem se na chvíli úplně zastavila a vnímala svět jinak.",
    "Velmi oceňuji, jak autorka pracuje s vnitřním světem postav.",
]

ALL_GOOD_USERS = good_males + good_females


def create_good_comments(num_users, num_comments_per_user):
    selected_users = random.sample(ALL_GOOD_USERS, min(num_users, len(ALL_GOOD_USERS)))
    available_books = list(Book.objects.all())
    if not available_books:
        return

    for username, _ in selected_users:
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
        except User.DoesNotExist:
            continue

        is_female = username in dict(good_females)
        comment_pool = good_female_comments if is_female else good_male_comments

        books_to_comment = random.sample(available_books, min(num_comments_per_user, len(available_books)))

        for book in books_to_comment:
            comment_text = random.choice(comment_pool)
            rating = random.choice([4, 5])

            Comment.objects.create(
                book=book,
                commenter=profile,
                rating=rating,
                user_comment=comment_text
            )

            print(f"✅ {profile.user.username} komentoval knihu '{book.title_cz}' – {rating}★")


def run(num_users, num_comments_per_user):
    create_good_comments(num_users, num_comments_per_user)


if __name__ == "__main__":
    run(2, 3)
