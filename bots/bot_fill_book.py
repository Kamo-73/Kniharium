import os
import sys
import django
import random
from urllib.parse import quote
from math import ceil

# Nastavíme správny cestu k súboru settings.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

# Import modelov
from viewer.models import Book, Author, Publisher, Genre, Format
from django.db import transaction

# Zo zoznamov pre názvy kníh a popisy
book_titles = {
    "The Cat Who Filed Taxes": "Kočka, která podávala daňové přiznání",
    "How to Survive a Zombie Job Interview": "Jak přežít pohovor se zombie",
    "Fifty Shades of Beige: The IKEA Chronicles": "Padesát odstínů béžové: Kroniky IKEA",
    "My Toaster Hates Me (And Other Kitchen Nightmares)": "Můj toustovač mě nenávidí (a další kuchyňské noční můry)",
    "The Secret Life of Left Socks": "Tajný život levých ponožek",
    "How I Accidentally Became a Llama": "Jak jsem se omylem stal lamou",
    "Aliens Ate My Homework (Again)": "Mimozemšťani mi snědli domácí úkol (zase)",
    "Diary of a Mildly Confused Potato": "Deník mírně zmatené brambory",
    "Don’t Trust the Duck in the Suit": "Nevěř kachně v obleku",
    "Yoga for the Emotionally Unstable Penguin": "Jóga pro emočně nestabilního tučňáka",
    "The Cheeseburger That Knew Too Much": "Cheeseburger, který věděl příliš mnoho",
    "Time Travel for People with Anxiety": "Cestování časem pro úzkostlivé",
    "Cooking with Tears: A Breakup Recipe Book": "Vaření se slzami: Kuchařka po rozchodu",
    "Ghosted by My Ghost": "Duch mě ignoruje",
    "The Man Who Married a Wi-Fi Signal": "Muž, který si vzal Wi-Fi signál",
    "101 Ways to Lose an Argument (And Still Feel Right)": "101 způsobů, jak prohrát hádku (a přesto mít pocit, že máte pravdu)",
    "My Therapist Is a Goldfish": "Můj terapeut je zlatá rybka",
    "Sneeze Like Nobody’s Watching": "Kýchej, jako by se nikdo nedíval",
    "The Epic Quest for the Last Clean Spoon": "Epické tažení za poslední čistou lžičkou",
    "How to Tell If Your Dog Is Planning a Coup": "Jak poznat, že váš pes plánuje převrat"
}

book_descriptions = [
    """Tato kniha není určená k tomu, abyste ji zhltli za víkend. Je jako starý dům na kraji lesa, do kterého vstoupíte opatrně a s úctou. V každém koutě se skrývá příběh, který nespěchá, ale čeká, až si k němu najdete cestu. Věty jsou tu jako šepot mezi stromy, kapitoly jako kroky v mechu. Čtení, které nevzniklo pro efekt, ale pro chvíle, kdy potřebujete znovu uvěřit, že slova mají duši.""",

    """Je to příběh, který nezačíná velkým třeskem, ale tichým pohybem myšlenky. Vzpomínky tu nejsou napsané, ale zapsané v meziřádcích. Postavy neřvou, nehroutí se, ale dýchají a žijí tak, jak to umíme jen my – když si myslíme, že se nikdo nedívá. Tahle kniha se vám nezaryje do paměti jednou větou, ale zůstane ve vás jako tichý refrén, který si začnete broukat až o týden později, když pojedete tramvají.""",

    """Není snadné tuhle knihu popsat, protože se jí nedá přiřadit jednoznačný žánr. Je to jako pozorovat déšť skrze okno v odpoledni, které nikam nespěchá. Každá kapitola je jako kapka – samostatná a přesto součást celku. Slova tu nestavějí monumenty, ale choulostivé mosty mezi čtenářem a něčím zasutým, co si ani neuvědomil, že v sobě nosí.""",

    """Tato kniha není napsaná k tomu, aby vás přesvědčila, že svět je krásný. Ona vám to neříká – jen vám ukáže, jak se na něj můžete dívat, když se zastavíte. Příběh pomalu rozplétá lidské nitky, obyčejné a přece tak silné. Nepřináší odpovědi, ale klade otázky, které jsme si přestali pokládat, protože jsme se báli, že odpověď bude znít tiše.""",

    """Představte si, že si otevřete starou krabici plnou dopisů, které nikdy nikdo neodeslal. Tahle kniha je právě taková – plná nenapsaných přiznání, odložených bolestí a jemných radostí, které nikdo nevyslovil nahlas. Je to čtení, které neosloví všechny, ale koho osloví, toho obejme. A nepustí – alespoň ne hned.""",

    """Některé knihy se čtou očima, jiné srdcem. Tahle patří k těm druhým. Její příběh je jako klidná řeka, která se vine krajinou vaší mysli, aniž by cokoli bourala. Přesto, když ji dočtete, zjistíte, že jste někde úplně jinde, než kde jste začali. Ne proto, že by vás změnila. Ale protože vám umožnila slyšet věci, které v sobě nosíte už dávno – jen jste je zapomněli poslouchat.""",

    """Tato kniha není o hrdinech, kteří zachraňují svět. Je o lidech, kteří zachraňují sami sebe – občas neobratně, občas neochotně, ale vždycky skutečně. Její tempo je jako dech po pláči – pomalé, hluboké, očišťující. Nepředstírá víc, než je, a právě v tom je její síla. Je to vyprávění, které neburcuje, ale přesto vás probudí.""",

    """Každý list této knihy je jako malý obraz, malovaný vnitřním světlem. Nejsou v ní výbuchy ani přestřelky – jen slova, která hladí. A myšlenky, které bolí právě proto, že jsou pravdivé. Příběh, který se nepíše na billboardy, ale šeptá se u kuchyňského stolu při pozdní kávě. Kniha pro všechny, kdo někdy cítili, že nejsou slyšet – ale doufali, že někdo přece jen naslouchá.""",

    """Tato kniha je jako tenký šátek, který se vám omotá kolem duše, aniž byste si toho nejdřív všimli. Je jemná, ale ne slabá. Tichá, ale ne bez hlasu. Příběh v ní se rozvíjí jako starý film, kde není důležitý děj, ale pohledy, které si postavy vyměňují beze slov. A právě v tom tichu, které mezi nimi vzniká, najdete sami sebe.""",

    """Čtení této knihy je jako být pozván na cizí půdu a přesto cítit, že jste doma. Je to melancholické putování krajinou vnitřního světa, kde je každý detail důležitý – prasklina na hrnku, zatažená obloha, vůně pečeného chleba. Je napsaná s takovou něhou, že se jí nechcete dotknout prstem – jen ji držet na klíně a dýchat spolu s ní."""
]
# Funkcia pre výber náhodného počtu strán
def get_random_pages():
    return random.randint(100, 1100)

# Funkcia pre výber náhodného popisu
def get_random_description():
    return random.choice(book_descriptions)

# Funkcia pre výber náhodného vydavateľa z databázy
def get_random_publisher():
    return Publisher.objects.order_by('?').first()

# Funkcia pre výber náhodne 3 žánre z databázy
def get_random_genres():
    genres = Genre.objects.order_by('?')[:3]
    return [genre.name for genre in genres]

# Funkcia pre výber náhodného obrázka
def get_random_image():
    image_files = ["book_fallback_1.png", "book_fallback_2.png", "book_fallback_3.png", "book_fallback_4.png", "book_fallback_5.png"]
    return f"images/{random.choice(image_files)}"

# Funkcia pre výber náhodného autora z databázy
def get_random_author():
    return Author.objects.order_by('?').first()

# Funkcia pre výber náhodného hodnotenia
def get_random_rating():
    return random.randint(1, 5)

# Funkcia pre výber náhodného roku vydania
def get_random_year():
    return random.randint(1969, 2025)

# Funkcia pre výber formátu (vždy "Vázaná kniha")
def get_format():
    return ["Vázaná kniha"]

# Funkcia pre výpočet času čítania na základe počtu strán
def calculate_reading_time(pages):
    words_per_page = 275
    reading_speed = 225  # words per minute
    return ceil((pages * words_per_page) / reading_speed)

@transaction.atomic
def check_and_fill_books():
    for book in Book.objects.all():
        print(f"\n🔄 Zpracovávám knihu: {book.title_orig}")

        # Ak kniha nemá title_orig, priradí náhodný názov z book_titles
        if not book.title_orig:
            random_title = random.choice(list(book_titles.keys()))
            book.title_orig = random_title
            book.title_cz = book_titles[random_title]
            print(f"📚 Názov knihy doplněn: '{book.title_orig}' a český překlad: '{book.title_cz}'")

        # Ak kniha nemá title_cz, vyberieme český preklad z book_titles podľa title_orig
        if not book.title_cz:
            if book.title_orig in book_titles:
                book.title_cz = book_titles[book.title_orig]
                print(f"📚 Český překlad doplněn: '{book.title_cz}'")

        # Ak kniha nemá description, vyberieme náhodný popis
        if not book.description:
            book.description = get_random_description()
            print(f"📖 Popis knihy doplněn.")

        # Ak kniha nemá num_of_pages, vyberieme náhodný počet strán
        if not book.num_of_pages:
            book.num_of_pages = get_random_pages()
            print(f"📄 Počet stran doplněn: {book.num_of_pages}")

        # Ak kniha nemá publisher, vyberieme náhodného vydavateľa
        if not book.publisher:
            book.publisher = get_random_publisher()
            print(f"🏢 Vydavatel doplněn: {book.publisher.name}")

        # Ak kniha nemá genre, vyberieme náhodné 3 žánre z databázy
        if not book.genre.exists():
            genres = get_random_genres()
            for genre_name in genres:
                genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                book.genre.add(genre_obj)
            print(f"🎬 Žánry doplněny: {', '.join(genres)}")

        # Ak kniha nemá rating_ours, vyberieme náhodné číslo medzi 1 a 5
        if not book.rating_ours:
            book.rating_ours = get_random_rating()
            print(f"⭐ Hodnocení doplněno: {book.rating_ours}")

        # Ak kniha nemá year_of_publishing, vyberieme náhodný rok
        if not book.year_of_publishing:
            book.year_of_publishing = get_random_year()
            print(f"📅 Rok vydání doplněn: {book.year_of_publishing}")

        # Ak kniha nemá time_of_reading, vypočítame ho
        if not book.time_of_reading:
            book.time_of_reading = calculate_reading_time(book.num_of_pages)
            print(f"⏳ Čas čtení doplněn: {book.time_of_reading} minut")

        # Ak kniha nemá format, vložíme "Vázaná kniha"
        if not book.format.exists():
            for format_name in get_format():
                format_obj, _ = Format.objects.get_or_create(name=format_name)
                book.format.add(format_obj)
            print(f"📚 Formát doplněn: {', '.join(get_format())}")

        # Ak kniha nemá obrázok, vyberieme náhodný obrázok
        if not book.image:
            book.image = get_random_image()
            print(f"🖼️ Obrázek doplněn: {book.image}")

        book.save()
        print(f"✅ Kniha '{book.title_orig}' bola úspešne aktualizována.")

if __name__ == "__main__":
    check_and_fill_books()

