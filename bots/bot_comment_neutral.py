import os
import django
import random
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

from django.contrib.auth.models import User
from viewer.models import Book, Comment
from accounts.models import Profile

neutral_males = [
    ("davezone", "David Malý"),
    ("jakubnet", "Jakub Růžička"),
    ("mh_log", "Milan Havelka"),
    ("radekline", "Radek Kříž"),
    ("voxel.cz", "Vojtěch Kolář"),
]

neutral_females = [
    ("eva.box", "Eva Benešová"),
    ("janette.cz", "Jana Urbanová"),
    ("nik.notes", "Nikola Veselá"),
    ("peta_input", "Petra Slavíková"),
    ("ak_skl", "Alena Krátká"),
]

neutral_male_comments = [
    "Kniha byla v pořádku, četl jsem ji bez problémů.",
    "Děj byl jednoduchý, ale dobře sledovatelný.",
    "Nebyla to špatná kniha, jen mě nechytla tak, jak jsem doufal.",
    "Něco mi tam chybělo, ale jinak to bylo celkem v pohodě.",
    "Dočetl jsem ji až do konce, což je u mě dobré znamení.",
    "Styl psaní mi celkem sedl.",
    "Některé pasáže byly zajímavé, jiné méně.",
    "Neurazí, ale ani nijak zvlášť nenadchne.",
    "Neměl jsem s ní větší problém.",
    "Příběh měl své silnější i slabší momenty.",
    "Nepatří mezi mé oblíbené, ale z četby jsem měl klidný dojem.",
    "Dalo se to číst, i když jsem čekal trochu víc.",
    "Celkem fajn kniha na odpočinek.",
    "Nezanechala ve mně silný dojem, ale byla v pohodě.",
    "Nebylo to špatné, ale podruhé bych si ji asi nepřečetl.",
    "V něčem mi sedla, v něčem méně – takový průměr.",
    "Určitě jsem četl i horší.",
    "Líbil se mi jazyk, ale děj mi byl trochu vzdálený.",
    "Není to úplně můj styl, ale kvalitu uznávám.",
    "Obsahově mě to neoslovilo, ale forma byla zpracovaná dobře.",
    "Kniha na mě působila klidně, ničím extra nevybočovala.",
    "Byla to zajímavá zkušenost, ale asi mi v paměti dlouho nezůstane.",
    "Nepřekáželo mi ji dočíst, ale ani jsem se netěšil na další kapitolu.",
    "Jednoduchý, ale konzistentní příběh.",
    "Vhodné na víkendové čtení bez velkých očekávání.",
    "Knihu jsem vnímal jako průměrnou, což nemusí být nutně špatně.",
    "Závěr byl celkem povedený, i když začátek mě nudil.",
    "Oceňuji snahu, i když to nebylo úplně pro mě.",
    "Kniha mi nic extra nedala, ale času s ní nelituji.",
    "Mohlo to být lepší, ale nebylo to špatné.",
]

neutral_female_comments = [
    "Kniha byla v pořádku, ale asi ve mně nezanechá hlubší stopu.",
    "Četla jsem ji bez větších emocí, ale dočetla jsem ji.",
    "Příběh měl potenciál, ale zůstal pro mě trochu vzdálený.",
    "Nemůžu říct, že by mě to nadchlo, ale neurazilo mě to.",
    "Děj plynul klidně, občas možná až moc.",
    "Postavy mi nebyly blízké, ale byla to zajímavá zkušenost.",
    "Styl psaní mi občas seděl, občas ne – tak půl na půl.",
    "Byla jsem zvědavá, jak to dopadne, ale žádné velké napětí jsem necítila.",
    "Obsahově to bylo nenáročné, vhodné na volný večer.",
    "Knihu jsem dočetla spíš ze zvyku než z nadšení.",
    "Některé části se mi líbily, jiné bych klidně přeskočila.",
    "Neměla jsem s knihou problém, ale ani jsem si ji extra neužila.",
    "Příběh se mi četl snadno, ale nedostal se mi pod kůži.",
    "Závěr mě nijak nepřekvapil, ale byl logický.",
    "Bylo to takové milé, ale nijak výjimečné čtení.",
    "Něco mi v tom chybělo, ale zároveň to nebylo špatné.",
    "Četla jsem horší, ale také mnohem lepší knihy.",
    "Kniha pro mě byla spíš kulisou než zážitkem.",
    "Styl byl jednoduchý, čitelný, ale trochu bez jiskry.",
    "Nezůstane mi v paměti, ale nelituji, že jsem ji četla.",
    "Místy mě bavila, místy jsem ztrácela pozornost.",
    "Knihu jsem vnímala jako průměrnou, což někdy úplně stačí.",
    "Četla se lehce, ale chyběla mi tam větší hloubka.",
    "Obsah ani forma mě příliš neoslovily, ale nebylo to špatné.",
    "Byla to klidná četba bez větších emocí.",
    "Nenadchla mě, ale chápu, že někoho jiného by mohla.",
    "Děj byl plynulý, ale bez momentu překvapení.",
    "Zajímavé téma, jen zpracování mě nechalo chladnou.",
    "Nebylo to úplně pro mě, ale chápu, co na tom může někoho zaujmout.",
    "Neurazilo, nenadchlo – prostě čtení na jedno odpoledne.",
]

ALL_USERS = neutral_males + neutral_females

try:
    num_users = int(input("Za koľkých používateľov sa mám prihlásiť? (max 10): "))
    num_comments_per_user = int(input("Koľko komentárov má každý z nich pridať?: "))
except ValueError:
    print("❌ Zadaj celé čísla.")
    exit()

if num_users < 1 or num_users > len(ALL_USERS):
    print("❌ Zlý počet používateľov.")
    exit()

selected_users = random.sample(ALL_USERS, num_users)

for username, full_name in selected_users:
    print(f"\n🧑‍💻 Prihlasujem sa za {username} ({full_name})")

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        print(f"❌ Užívateľ {username} neexistuje.")
        continue

    is_female = (username in dict(neutral_females))
    comments_pool = neutral_female_comments if is_female else neutral_male_comments

    available_books = list(Book.objects.all())
    if not available_books:
        print("❌ Žiadne knihy v databáze.")
        break

    books_to_comment = random.sample(available_books, min(num_comments_per_user, len(available_books)))

    for book in books_to_comment:
        comment_text = random.choice(comments_pool)
        rating = random.choice([2, 3])

        Comment.objects.create(
            book=book,
            commenter=profile,
            rating=rating,
            user_comment=comment_text
        )

        print(f"📘 {book.title_cz}: {rating}★ – {comment_text[:40]}...")
