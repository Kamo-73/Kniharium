import datetime
import os
import django
from django.conf import settings

# Nastavíme správny cestu k súboru settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kniharium.settings')
django.setup()

import random
from viewer.models import Author, Nationality, Genre

# Zo zoznamov pre autorov a priezviská
names = [
    "Alex", "Taylor", "Jordan", "Casey", "Morgan", "Riley", "Avery", "Skyler", "Cameron", "Bailey",
    "Sydney", "Quinn", "Rowan", "Dakota", "Emerson", "Parker", "Harper", "Spencer", "Finley", "Rowan"
]

surnames = [
    "Taylor", "Morgan", "Jordan", "Parker", "Quinn", "Harper", "Riley", "Cameron", "Bailey",
    "Emerson", "Spencer", "Dawson", "Grey", "Ellis", "Brooks", "Lane", "Avery", "Foster",
    "Reid", "Sawyer"
]

author_descriptions_czech = [
    "Autor začal svou tvorbu v mladém věku, když si poprvé všiml, jak příroda kolem něj ovlivňuje jeho vnímání světa. Během dětství se jeho první verše věnovaly pozorování změn v ročních obdobích a jejich vlivu na duši. Tato tématika zůstala v jeho tvorbě přítomná, ale později přešel k psaní příběhů, v nichž se často odráží i hluboká symbolika přírody a její propojení s lidskými emocemi. V jeho dílech se objevují nejen literární obrazy, ale i postavy, které prožívají svou osobní melancholii, a hledání smyslu života ve světě, který je neustále v pohybu.",

    "Literární dráha autora začala v době, kdy objevil ticho a poklidnou atmosféru malého města, kde se knihy staly jeho jediným únikem. V období dospívání začal psát, nejprve deníky a později eseje, které zkoumaly identitu, existenci a místa, která se v jeho mysli neustále měnila. Postupně přešel k psychologickým románům, které se zaměřují na vnitřní svět postav a jejich pohledy na svět kolem sebe. Pro autora je charakteristická schopnost vykreslit rozpor mezi vnějšími očekáváními a vnitřním bojem jednotlivce.",

    "Během svého života se autor věnoval několika disciplínám, zejména divadlu a filmu, kde se jeho schopnosti psaní scénářů a dramaturgie odrazily i v jeho literární tvorbě. Jeho příběhy jsou dynamické, plné napětí a zvratů, přičemž každá scéna je jako malý film, který se čtenáři promítá před očima. Knihy autora balancují mezi realitou a imaginací, kde se hlavní hrdinové setkávají se svými vnitřními démony, čímž vytvářejí komplexní a zajímavou literární krajinu.",

    "Po letech strávených na cestách, autor našel inspiraci v zkušenostech, které si přinesl z různých zemí. Jeho příběhy jsou ovlivněny setkáními s různými kulturami, což se odráží v jeho psaní o cizině a pocitu, že člověk je vždy na cestě, hledajíc něco, co mu uniká. Každé město, každé místo, které navštívil, mu poskytlo nový pohled na svět, a tyto dojmy se přetavily do literárních děl, která nejsou pouze o geografii, ale i o vnímání odlišnosti a propojení mezi místy a lidmi.",

    "Autor, který předtím pracoval v akademické sféře, se dostal k psaní jako způsob vyjádření sebe samého mimo omezení vědy. Jeho knihy se vyznačují filozofickými otázkami o povaze reality a toho, co je skutečné. S využitím prvků science fiction autor zkoumá hranice mezi vědou a uměním a vytváří svět, kde psychologie postav a jejich reakce na existenciální problémy jsou stejně důležité jako samotný děj. Tento přístup umožňuje čtenáři ponořit se do hlubokých otázek o tom, co je pravda a jak ji vnímáme.",

    "Tvorba autora je ovlivněna jeho vnímáním noci a její schopností prohloubit myšlenky. Píše převážně v pozdních večerních hodinách, kdy se svět ztiší a pozornost se upírá na detaily, které přes den zůstávají skryté. Jeho díla jsou zaměřena na téma lidské křehkosti, ztráty, ale i na naději, která nikdy úplně nezmizí. Autor se často zabývá vnitřním světem jednotlivce, jeho myšlenkami, které odrážejí obavy a touhy člověka, který se snaží pochopit sám sebe a své místo v tomto světě.",

    "Autorovy začátky v literatuře jsou spojeny s jeho původním zájmem o matematiku a vědu, ale psaní se stalo jeho vášnivým únikem. V jeho dílech se často objevují složité filozofické a vědecké koncepty, které jsou zakomponovány do příběhů o lidských postavách a jejich osobních dilematech. Využívá prvky fantastiky a hororu, ale největší důraz klade na psychologickou hloubku postav, které se musí vyrovnávat se svými vlastními temnými stránkami. Tvorba autora je reflexí toho, co znamená být člověkem v neustále se měnící realitě.",

    "Tvorba autora se vyznačuje jeho schopností vytvořit atmosféru napětí a znepokojení. Knihy, které píše, balancují na hranici mezi hororem, psychologickými dramy a existenciálními otázkami. Fascinace temnými stránkami lidské povahy a otázkami o strachu, vině a ztrátě ho přivedla k psaní, které se vyznačuje intenzivním propojením mezi postavami a jejich vnitřním světem. Autor se nebojí využít i nepříjemné témata, protože věří, že pravá literatura musí být schopná znepokojovat a přinášet otázky, které zní i po přečtení poslední stránky.",

    "Autor pochází z malého města, kde si lidé často vyprávěli příběhy u kuchyňského stolu. Tuto tradici si udržel i ve své tvorbě, kde často píše o mezilidských vztazích, rodinných dramatech a malých tajemstvích, které jsou součástí každodenního života. V jeho knihách se často objevují postavy, které čelí svým problémům, rozhodnutím a ne vždy jednoduchým vztahům. Autor věří, že i v těch nejjednodušších příbězích se skrývá něco velmi hlubokého a pravdivého, co se nedá vyjádřit prázdnými slovy.",

    "V mládí autor snil o tom, že se stane hudebníkem, ale postupně zjistil, že jeho největší vášeň spočívá v psaní. Jeho tvorba je silně lyrická, s prvky hudebního rytmu a melodiky, které se přenášejí do jeho literárních děl. V jeho knihách se objevují motivy lásky, ztráty, snů a hledání smyslu života. Autor dokáže každou jednoduchou chvíli změnit na silný emocionální zážitek, který čtenář vnímá jako symfonii pocitů. Tento přístup ho činí jedinečným mezi spisovateli."
]

nationalities = [
    "Americká", "Anglická", "Argentinská", "Australská", "Belgická", "Brazilská", "Britská", "Dánská", "Egyptská",
    "Finská", "Francouzská", "Indická", "Irská", "Italská", "Izraelská", "Japonská", "Kanadská", "Korejská", "Kubánská",
    "Maďarská", "Mexická", "Nizozemská", "Norská", "Německá", "Polská", "Portugalská", "Rakouská", "Rumunská", "Ruská",
    "Slovenská", "Turecká", "USA", "Ukrajinská", "Íránská", "Česká", "Čínská", "Řecká", "Španělská", "Švédská", "Švýcarská"
]

quotes = [
    "A reader lives a thousand lives before he dies.",
    "Books are a uniquely portable magic.",
    "Until I feared I would lose it, I never loved to read. One does not love breathing.",
    "So many books, so little time.",
    "A room without books is like a body without a soul.",
    "I have always imagined that Paradise will be a kind of library.",
    "Reading gives us someplace to go when we have to stay where we are.",
    "There is no friend as loyal as a book.",
    "That’s the thing about books. They let you travel without moving your feet.",
    "Books are the mirrors of the soul.",
    "We read to know we're not alone.",
    "You can never get a cup of tea large enough or a book long enough to suit me.",
    "The only thing that you absolutely have to know, is the location of the library.",
    "Books wash away from the soul the dust of everyday life.",
    "You don’t have to burn books to destroy a culture. Just get people to stop reading them.",
    "Reading is essential for those who seek to rise above the ordinary.",
    "Books are the quietest and most constant of friends.",
    "The man who does not read has no advantage over the man who cannot read.",
    "Once you learn to read, you will be forever free.",
    "I do believe something very magical can happen when you read a good book.",
    "Some books leave us free and some books make us free.",
    "Books are a form of political action. Books are knowledge. Books are reflection. Books change your mind.",
    "A book is a dream that you hold in your hands.",
    "There are worse crimes than burning books. One of them is not reading them.",
    "No two persons ever read the same book.",
    "If you only read the books that everyone else is reading, you can only think what everyone else is thinking.",
    "Books can be dangerous. The best ones should be labeled 'This could change your life.'",
    "Books are the treasured wealth of the world and the fit inheritance of generations and nations.",
    "A book is a device to ignite the imagination.",
    "You don’t read a book to pass the time. You read to discover yourself."
]



def fill_author_data():
    # Prejde všetkých autorov
    for author in Author.objects.all():
        print(f"🔄 Spracúvam autora: {author.name} {author.surname}")

        # Dopĺňa meno a priezvisko, ak chýbajú
        if not author.name:
            author.name = random.choice(names)
            print(f"👤 Meno pridané: {author.name}")
        if not author.surname:
            author.surname = random.choice(surnames)
            print(f"👤 Priezvisko pridané: {author.surname}")

        # Dopĺňa dátum narodenia, ak chýba
        if not author.date_of_birth:
            year = random.randint(1950, 2000)
            author.date_of_birth = datetime.date(year, 1, 1)
            print(f"🎂 Dátum narodenia pridaný: {author.date_of_birth}")

        # Dopĺňa biografiu, ak chýba
        if not author.biography:
            author.biography = random.choice(author_descriptions_czech)
            print(f"📖 Biografia pridaná.")

        # Dopĺňa národnosť, ak chýba
        if not author.nationality:
            nationality_name = random.choice(nationalities)
            nationality_obj, created = Nationality.objects.get_or_create(name=nationality_name)
            author.nationality = nationality_obj
            print(f"🌍 Národnosť pridaná: {nationality_name}")

        # Dopĺňa primarny zaner, ak chýba
        if not author.primary_genre:
            all_genres = Genre.objects.all()
            if all_genres.exists():
                author.primary_genre = random.choice(list(all_genres))
                print(f"Hlavny zaner pridany.")

        # Dopĺňa citat, ak chýba
        if not author.quote:
            author.quote = random.choice(quotes)
            print(f"Citat pridany.")

        # Nastaví obrázok, ak chýba
        if not author.image:
            author.image = "images/author_fallback_neutral.png"
            print(f"🖼️ Obrázok pridaný: author_fallback_neutral.png")

        # Uložíme aktualizovaného autora
        author.save()
        print(f"✅ Autor {author.name} {author.surname} bol úspešne aktualizovaný.")

def run():
    fill_author_data()


if __name__ == "__main__":
    fill_author_data()
