import os
import django
import random
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

from django.contrib.auth.models import User
from viewer.models import Book, Comment
from accounts.models import Profile

bad_males = [
    ("true.fil", "Filip Hrdina"),
    ("dom_critic", "Dominik Král"),
    ("alextight", "Aleš Tomšík"),
    ("kar.sv", "Karel Švec"),
    ("obzero", "Ondřej Bláha"),
]

bad_females = [
    ("sim_sharp", "Simona Richterová"),
    ("ivy_note", "Iveta Mašková"),
    ("sandrix", "Sandra Čechová"),
    ("bkn_point", "Barbora Konečná"),
    ("luc.fix", "Lucie Holá"),
]

bad_male_comments = [
    "Tohle mě vůbec nebavilo, četl jsem to jen se sebezapřením.",
    "Příběh mi přišel zmatený a nedotažený.",
    "Autor očividně nevěděl, kam tím chce jít.",
    "Měl jsem co dělat, abych to vůbec dočetl.",
    "Nesedl mi styl psaní, působilo to na mě uměle.",
    "Postavy byly ploché a vůbec jsem si k nim nenašel cestu.",
    "Nevyvolalo to ve mně žádné emoce, jen nudu.",
    "Po prvních kapitolách jsem ztratil zájem.",
    "Závěr byl zklamáním – čekal jsem něco víc.",
    "Děj se vlekl a nevedl nikam zajímavého.",
    "Slabá zápletka, která se zbytečně natahovala.",
    "Čekal jsem kvalitu, ale dostal jsem průměr zabalený do klišé.",
    "Mám pocit, že to psal někdo bez zkušeností.",
    "Hodně slov, málo obsahu.",
    "Všechno bylo předvídatelné a bez nápadu.",
    "Téma bylo zaujímavé, ale provedení mě zklamalo.",
    "Zbytečně komplikované a přitom bez hloubky.",
    "Nedokázal jsem se do toho vůbec začíst.",
    "Nechápu, proč má tahle kniha tolik dobrých recenzí.",
    "Místo zážitku jsem měl pocit ztraceného času.",
    "Jedna z těch knih, které si přečtu a hned zapomenu.",
    "Dialogy byly nepřirozené a kostrbaté.",
    "Kniha mě ničím nepřekvapila, spíš otrávila.",
    "Styl mi přišel přehnaný a samoúčelný.",
    "Pořád jsem čekal, že se to zlepší, ale nestalo se.",
    "Četl jsem to jen proto, že jsem to už začal – jinak bych přestal.",
    "Nic nového, nic hlubokého, jen prázdné řádky.",
    "Byla to pro mě spíš povinnost než radost.",
    "Slibný začátek, ale rychle to sklouzlo do průměru.",
    "Kdybych věděl, jak to dopadne, ani bych se do toho nepouštěl.",
]

bad_female_comments = [
    "Tahle kniha mě bohužel vůbec neoslovila.",
    "Četla jsem to jen proto, že nerada něco nedočítám.",
    "Postavy mi přišly ploché a nezajímavé.",
    "Měla jsem pocit, že to nikam nevede.",
    "Od začátku jsem se nudila, a nic se nezměnilo ani v průběhu.",
    "Děj byl pro mě zmatený a těžko sledovatelný.",
    "Styl psaní mi nesedl – zbytečně komplikovaný a těžkopádný.",
    "Byla jsem zklamaná, čekala jsem úplně něco jiného.",
    "Nepřišlo mi to autentické, všechno působilo uměle.",
    "Nevyvolalo to ve mně vůbec žádné emoce.",
    "Čekala jsem hlubší pointu, ale zůstalo to na povrchu.",
    "Příběh mi připadal neoriginální a předvídatelný.",
    "Kniha byla dlouhá, ale bohužel bez obsahu.",
    "Nic nového jsem si z toho neodnesla.",
    "Místy jsem měla chuť to zavřít a už se k tomu nevracet.",
    "Dialogy mi přišly nepřirozené a nucené.",
    "Byla to pro mě ztráta času, a to říkám nerada.",
    "Nevěřila jsem postavám ani jejich motivům.",
    "Kniha mě ničím nezaujala, jen jsem se trápila od stránky ke stránce.",
    "Celý děj působil rozvláčně a zbytečně nataženě.",
    "Zklamalo mě, jak plytký ten příběh vlastně byl.",
    "Dočetla jsem ji spíš z povinnosti než ze zájmu.",
    "Nedokázala jsem se do toho ponořit, pořád mě něco rušilo.",
    "Téma bylo zajímavé, ale zpracování nezvládnuté.",
    "Nenašla jsem tam nic, co by mi stálo za to doporučit dál.",
    "Za mě jedna z nejslabších knih, které jsem letos četla.",
    "Byla to taková slátanina bez hlavy a paty.",
    "Měla jsem od toho velká očekávání, a o to větší bylo zklamání.",
    "Celou dobu jsem čekala, že to konečně začne dávat smysl – nedočkala jsem se.",
    "Po dočtení jsem si spíš oddechla, že už je konec.",
]

ALL_USERS = bad_males + bad_females

def create_bad_comments(num_users, num_comments_per_user):
    selected_users = random.sample(ALL_USERS, min(num_users, len(ALL_USERS)))
    available_books = list(Book.objects.all())
    if not available_books:
        return

    for username, _ in selected_users:
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
        except User.DoesNotExist:
            continue

        is_female = username in dict(bad_females)
        comment_pool = bad_female_comments if is_female else bad_male_comments

        books_to_comment = random.sample(available_books, min(num_comments_per_user, len(available_books)))

        for book in books_to_comment:
            comment_text = random.choice(comment_pool)
            rating = random.choice([1, 2])

            Comment.objects.create(
                book=book,
                commenter=profile,
                rating=rating,
                user_comment=comment_text
            )

            print(f"👤 {username} komentoval 📖 „{book.title_cz}“ ({rating}★): {comment_text[:50]}...")


def run(num_users, num_comments_per_user):
    create_bad_comments(num_users, num_comments_per_user)

if __name__ == "__main__":
    run(2, 3)