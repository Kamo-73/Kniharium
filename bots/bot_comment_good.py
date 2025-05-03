import os
import django
import random
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

from django.contrib.auth.models import User
from viewer.models import Book, Comment
from accounts.models import Profile

# Používateľské skupiny
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
    "Vynikající jazyk, žádné zbytečné řeči – přesně to mám rád.",
    "Byl jsem nadšený, jak autor zvládl náročné téma.",
    "Už dlouho jsem nečetl něco tak upřímného a silného.",
    "Knihu jsem přečetl za dva večery – nemohl jsem přestat.",
    "Doporučuji každému, kdo má rád inteligentní příběhy.",
    "Jsem rád, že jsem na tuhle knihu narazil.",
    "Děj mě držel v napětí až do poslední stránky.",
    "Líbilo se mi, jak se všechno nakonec spojilo.",
    "Velmi silný závěr – zanechalo to ve mně stopu.",
    "Mám rád knihy, které mě nutí se zamyslet – a tahle to zvládla skvěle.",
    "Příběh měl hloubku i emoci, přesně to jsem hledal.",
    "Musím uznat, že tohle bylo výjimečné čtení.",
    "Postavy byly realistické a jednaly uvěřitelně – ocenil jsem to.",
    "Už dlouho mě nic takhle nevtáhlo.",
    "Zhltnul jsem to za jeden den.",
    "Krásně napsané – klobouk dolů.",
    "Celé to působilo přirozeně a uvěřitelně.",
    "Kniha mě obohatila a zanechala ve mně silný dojem.",
    "Pro mě osobně to bylo velmi inspirativní.",
    "Skvělé zpracování, výborný jazyk a silný příběh – jsem spokojený.",
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
    "Tohle bylo víc než kniha – spíš tichý rozhovor, co hladí duši.",
    "Četla jsem to pomalu, abych si každou vetu vychutnala.",
    "Kniha plná jemnosti, ale aj sily – krásné spojení.",
    "Konečně příběh, kde se cítím pochopená.",
    "Jazyk byl nádherný, občas jsem si musela některé pasáže přečíst dvakrát – jen pro tu krásu.",
    "Emoční rovina téhle knihy byla přesně to, co jsem v tu chvíli potřebovala.",
    "Dlouho mě nic tak nezasáhlo, a přitom to bylo tak nenápadné.",
    "Kniha se mnou zůstala – pořád se k ní myšlenkami vracím.",
    "Postavy mi byly neuvěřitelně blízké, skoro jako by to byli moji známí.",
    "Silný příběh, ale bez zbytečného patosu – to umí málokdo.",
    "Našla jsem se v těch pocitech, v tom tichu mezi řádky.",
    "Každá kapitola ve mně vyvolala jiný obraz, krásně vizuální zážitek.",
    "Tahle kniha se mnou mluvila tichým, ale pevným hlasem.",
    "Byla jsem mile překvapená, jak jednoduše a přirozeně příběh plyne.",
    "Děkuju autorce za tenhle zážitek – takové knihy bych chtěla víc.",
    "Oceňuji, že příběh nesoudil, jen vyprávěl – a to mi stačilo.",
    "Kniha, která mě objala, i když jsem to vůbec nečekala.",
    "Každá stránka měla svůj význam, nebylo tam nic navíc.",
    "Skvělá rovnováha mezi emocemi a myšlenkou – jsem nadšená.",
    "Četla jsem ji pomalu, s respektem, protože si to zasloužila.",
]

# Zbierka všetkých používateľov
ALL_GOOD_USERS = good_males + good_females

# Dotaz na užívateľa
try:
    num_users = int(input("Za koľkých používateľov sa mám prihlásiť? (max 10): "))
    num_comments_per_user = int(input("Koľko komentárov má každý z nich pridať?: "))
except ValueError:
    print("❌ Zadaj celé čísla.")
    exit()

if num_users < 1 or num_users > len(ALL_GOOD_USERS):
    print("❌ Zlý počet používateľov.")
    exit()

# Výber náhodných používateľov
selected_users = random.sample(ALL_GOOD_USERS, num_users)

for username, full_name in selected_users:
    print(f"\n🧑‍💻 Prihlasujem sa za {username} ({full_name})")

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        print(f"❌ Užívateľ {username} neexistuje.")
        continue

    is_female = (username in dict(good_females))

    comments_pool = good_female_comments if is_female else good_male_comments
    available_books = list(Book.objects.all())
    if not available_books:
        print("❌ Žiadne knihy v databáze.")
        break

    # Vyber náhodné unikátne knihy
    books_to_comment = random.sample(available_books, min(num_comments_per_user, len(available_books)))

    for book in books_to_comment:
        comment_text = random.choice(comments_pool)
        rating = random.choice([4, 5])

        Comment.objects.create(
            book=book,
            commenter=profile,
            rating=rating,
            user_comment=comment_text
        )

        print(f"📘 {book.title_cz}: {rating}★ – {comment_text[:40]}...")