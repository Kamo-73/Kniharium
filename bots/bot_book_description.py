import requests
import random
from urllib.parse import quote

#  Fallback descriptions – used if the original description was missing or weak
FALLBACK_DESCRIPTIONS = [
    "Tato kniha je jako tiché posezení v zapadlém knihkupectví, kde voní starý papír a čas plyne pomaleji. Nabízí nenápadný, ale hluboký příběh, který se pomalu rozvíjí jako květina v prvním jarním slunci. Ideální pro chvíle, kdy potřebujete na chvíli vypnout a znovu se zamilovat do světa slov.",
    "Tahle kniha si na nic nehraje – prostě si vás získá. Možná nenápadně, ale o to vytrvaleji. Každá stránka dýchá atmosférou, která vás obejme jako starý známý.",
    "Tato kniha je jako tajný deník, který někdo zanechal ve staré zásuvce. Každé otočení stránky je jako objev nového zákoutí lidské duše. Čtení, které nenutí běžet, ale kráčet.",
    "Kniha, kterou právě držíte v ruce, nepatří mezi tituly, které křičí z regálů. Ale to je právě její kouzlo. Pomalu a s citem vás vezme na cestu, kde nečekané neznamená nutně hlasité.",
    "Je těžké tuhle knihu někam zařadit – a to je na ní to nejlepší. Není to jen příběh, je to nálada. Atmosféra, která vás obklopí a nepustí, dokud nedočtete poslední stránku.",
    "Některé knihy nepotřebují složitou zápletku, aby vám zůstaly v paměti – stačí jim atmosféra, lidskost a pár dobře mířených vět.",
    "Tato kniha je jako nečekaný rozhovor s cizincem ve vlaku. Je v ní něco zvláštně známého, co vás nutí číst dál a dál. Každý odstavec je jako tichý úsměv.",
    "V dnešní době, kdy všechno spěchá, působí tato kniha jako zpomalený záběr ve filmu. Pocta pomalosti, tichým myšlenkám a neokázalým příběhům.",
    "Existují knihy, které vás nezmění, ale přesto si je zamilujete. Nabízí jednoduchý příběh s emocemi, které mají váhu. Čtení, co připomíná rozhovor s někým, kdo vás chápe.",
    "Tato kniha není o velkých gestech ani dramatických zlomech. Je o každodennosti, která se stává výjimečnou, když ji někdo umí popsat správnými slovy.",
    "Tato kniha je jako pomalá procházka v podvečerním světle, kdy se město ukládá ke spánku a člověk si konečně může dovolit zpomalit. Nečekejte velké dějové zvraty, ale spíš tiché momenty, které vám zůstanou v hlavě ještě dlouho po dočtení. Je to příběh pro ty, kteří vnímají meziřádky víc než samotná slova.",
    "Čtení této knihy připomíná dlouhý dopis od někoho, koho jste kdysi znali a trochu zapomněli. Je v ní melancholie, ale i naděje, klid i vnitřní bouře. Není to titul, který by se hnal kupředu – spíš vás nenápadně přitáhne a zůstane s vámi jako vzpomínka, která se nevytrácí.",
    "Jsou knihy, které vám přinesou odpovědi, a pak ty, které ve vás vyvolají nové otázky. Tahle patří k těm druhým. Je to tichý dialog mezi autorem a čtenářem, založený na důvěře, že i ticho má co říct. Pro čtenáře, kteří hledají něco hlubšího, i když nevědí přesně co.",
    "Tato kniha nevypráví příběh – ona ho šeptá. Pomalu, bez spěchu, občas s pauzami na přemýšlení. Nabízí svět, do kterého se nechcete vrhnout po hlavě, ale spíš do něj opatrně vkročit, usednout, nadechnout se a chvíli jen být. Je to čtení, které má duši.",
    "Kdyby tahle kniha byla hudbou, byla by jemnou melodií hranou na starý klavír v tiché místnosti. Nic v ní nekřičí, ale o to víc říká. Je plná malých gest, které mají váhu, a příběhů, co se odehrávají spíš uvnitř než venku. Skvělá volba pro chvíle, kdy potřebujete ztišit svět kolem sebe.",
    "Je to kniha, která nepřichází s velkými sliby – a přesto splní víc, než čekáte. Je o věcech, které jsou mezi řádky. O tom, co se stane, když se nic neděje. Pokud máte rádi příběhy, které se odvíjejí jako vzpomínky, a postavy, které nejsou hrdiny, ale lidmi, pak je to kniha pro vás.",
    "Tato kniha je jako snění s otevřenýma očima. Nejasná, jemná, ale přitom intenzivní. Každá kapitola je jako obraz malovaný akvarelem – barvy nejsou ostré, ale přesto zanechávají dojem. Pro čtenáře, kteří milují atmosféru víc než akci, a emoce víc než fakta.",
    "Není to čtení pro ty, kdo chtějí všechno hned. Ale kdo se nechá vést jejím tempem, najde v ní víc, než by čekal. Příběh, který vás nezavalí, ale obklopí. Kniha, která vás možná nezmění – ale možná vám připomene, kdo jste byli, než se svět zrychlil.",
    "Tahle kniha je jako cesta vlakem za deště. Není kam spěchat, nic není naléhavé, a právě v tom je její krása. Slova v ní jsou jako kapky na skle – každá má tvar, směr a smysl. Pro čtenáře, kteří hledají ticho, v němž se rodí myšlenky.",
    "Je to kniha, která nemluví nahlas – ale kdo naslouchá, uslyší v ní všechno. Místo dramat nabízí střípky života. Místo velkých point jemné poznání. A místo akce klidnou sílu. Čtení pro duši, ne pro seznam bestsellerů.",
    "Tato kniha je jako šálek čaje na okně během deštivého dne – klidná, zahřívající a plná jemných nuancí, které odhalíte jen tehdy, když zpomalíte. Nečeká na vás akce, ale něha. Nehoní se za efekty, ale důvěřuje síle obyčejných slov. Čtení, které uzdravuje.",
    "V každé větě této knihy je cítit lidskost – neokázalá, tichá, ale upřímná. Je to jako pohled do cizího života, který je překvapivě blízký tomu vašemu. Nejsou tu hrdinové ani padouši, jen lidé. A právě proto má tenhle příběh sílu zůstat s vámi.",
    "Tahle kniha je jako vzpomínka, o které jste nevěděli, že ji máte. Nevnucuje se, nevyčnívá, ale jakmile se jí dotknete, něco ve vás se rozpomene. Možná na dětské léto, na starý hlas v rádiu, nebo na ticho, které mělo význam. Je to příběh o věcech, které neumíme pojmenovat – ale cítíme je.",
    "Tato kniha je jako paprsek slunce na zaprášeném stole. Nenápadná, ale když si k ní sednete, osvítí i to, co jste nečekali. Čtení, které vás nezvedne ze židle – ale změní způsob, jak se na svět díváte, když z ní vstanete.",
    "Někdy člověk nepotřebuje odpovědi, jen dobré otázky – a tahle kniha je jich plná. Není návodem, ale společníkem. Místo děje nabízí prostor. Místo akce klade důraz na to, co cítíte mezi stránkami. Kniha, která vás naučí poslouchat i vlastní ticho.",
    "Je to čtení pro chvíle, kdy venku prší, uvnitř voní dřevo a vy máte čas. Ne proto, že ho máte hodně – ale protože ho chcete věnovat něčemu, co si to zaslouží. Tahle kniha není rychlý zážitek, ale pomalé pohlazení po duši.",
    "Tato kniha připomíná zpětné zrcátko – nevede vás vpřed, ale dovolí vám rozumět cestě, kterou jste už prošli. Možná neodpoví na vše, ale přiměje vás zastavit se a uvidět to, co jste přehlíželi. Tiché čtení, které zní ještě dlouho poté.",
    "Je to příběh, který nespěchá. Otevírá se jako stará krabice se vzpomínkami – trochu zaprášená, ale plná malých pokladů. Věci, které se nedají koupit, jen najít. A tahle kniha je jedním z nich.",
    "Některé knihy jsou jako polozapomenuté dopisy, které vám někdo kdysi napsal, ale nikdy neodeslal. Tato je jedním z nich. Oslovuje vás napřímo, osobně, i když možná ani neznáte jméno autora. Čtení, které nevysvětluje, ale rozumí.",
    "Tato kniha není odpovědí. Je otázkou, kterou jste si dávno přestali klást – ale která čekala, až ji znovu uslyšíte. Pomalu, tiše, ale s o to větší silou vás vede zpět k sobě. Možná v ní nenajdete děj, ale najdete se v ní sami.",
    "Tato kniha není výkřikem do tmy, ale spíš slabým světélkem na konci dlouhé chodby – nevede vás ven, ale dovnitř. Věnuje pozornost tomu, co většina příběhů přehlíží: drobným tichům mezi větami, úsměvům, které si postavy ani neuvědomí, že dávají. Je to vyprávění, které nelze dočíst bez toho, aniž byste si v sobě něco malého přestavěli.",
    "Některé příběhy nespěchají, protože vědí, že ty nejdůležitější věci potřebují čas. Tato kniha je jako rozhovor, který se nevede kvůli odpovědím, ale kvůli přítomnosti. Každá kapitola je jako pokoj, do kterého vstoupíte, posadíte se, a chvíli jen posloucháte, co v něm zůstalo viset ve vzduchu. Čtení pro ty, kteří si všímají víc pocitů než činů.",
    "Příběhy jako tento nejsou o tom, co se stane, ale co se změní – ne venku, ale ve vás. Je to kniha, která vás neohromí prvními stránkami, ale nenápadně vás vtáhne, jako když vám někdo při večerní procházce podá ruku. Není v ní nic přehnaného, a přece má každá věta sílu zůstat.",
    "Tato kniha není jen příběhem, je prostorem. Místem, kam můžete utéct, když se svět zdá být příliš hlučný. Je napsaná jazykem, který nic netlačí, ale všechno cítí. Připomíná dávno ztracený sen, který se vám vrátí ve chvíli, kdy ho nejmíň čekáte – a vy si uvědomíte, že vám chyběl.",
    "Není to kniha, kterou byste přečetli za večer. Ne proto, že by byla náročná – ale protože vás nutí zastavovat se. Přemýšlet. Vrátit se k předchozí větě. A možná i k sobě samým. Je to čtení, které se nevejde do anotace, protože to nejdůležitější se odehrává mezi slovy.",
    "V některých knihách nenajdete ani dobrodružství, ani napětí – ale najdete klid. Tahle kniha je jako návrat na místo, kde jste kdysi byli šťastní, i když už si přesně nevzpomínáte proč. Přináší jemnost, kterou dnešní svět často ztrácí, a připomíná, že i ticho může být plné hlasů.",
    "Tato kniha je jako když se podíváte na starou fotografii, kterou jste nikdy předtím neviděli – a přesto v ní poznáváte něco důvěrně známého. Není důležité, o čem přesně je. Důležité je, jak se při jejím čtení cítíte. A pokud jí dovolíte vstoupit pod kůži, možná vám tiše změní pohled na svět.",
    "Někdy člověk potřebuje knihu, která ho neodvede jinam, ale přivede zpět. K sobě, ke vzpomínkám, ke slovům, která už dlouho nikdo nevyslovil. Tahle kniha není hlasitá – ale právě tím má sílu. Je jako stisk ruky v nečekaném okamžiku. Jako dech mezi větami. Jako domov tam, kde jste ho nehledali.",
    "Tahle kniha si vás nezíská efektem, ale tichem. Nabízí příběh, který nevysvětluje, jen existuje – a vy ho začnete vnímat spíš srdcem než hlavou. Je to čtení pro lidi, kteří neztrácejí čas hledáním velkých slov, ale ocení, když někdo beze slov řekne všechno důležité.",
    "Je to kniha, kterou si nepamatujete po kapitolách, ale po pocitech. Po náladách, které ve vás vyvolala. Po momentech, kdy jste se přistihli, že na chvíli zapomněli, kde jste. Nečeká na váš obdiv – jen na vaši pozornost. A kdo ji dá, dostane víc, než by čekal."
]

def translate_to_czech(text):
    try:
        parts = [text[i:i+500] for i in range(0, len(text), 500)]
        translated_parts = []
        for part in parts:
            resp = requests.get(f"https://api.mymemory.translated.net/get?q={quote(part)}&langpair=en|cs")
            data = resp.json()
            translation = data['responseData']['translatedText']
            translated_parts.append(translation)
        joined = " ".join(translated_parts)
        return joined.replace("\n", " ").strip()
    except:
        return text.replace("\n", " ").strip()

def get_work_key(book_title):
    query = quote(book_title)
    url = f"https://openlibrary.org/search.json?title={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if data["numFound"] == 0:
        return None
    return data["docs"][0].get("key")

def get_description_from_openlibrary(work_key):
    url = f"https://openlibrary.org{work_key}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    desc = data.get("description")
    if isinstance(desc, dict):
        return desc.get("value")
    return desc

def get_and_translate_description(book_title):
    work_key = get_work_key(book_title)
    if not work_key:
        fallback = random.choice(FALLBACK_DESCRIPTIONS)
        print("⚠️ Neúspěšné vyhledání – použitý fallback popis.")
        return fallback

    description_en = get_description_from_openlibrary(work_key)
    if not description_en:
        fallback = random.choice(FALLBACK_DESCRIPTIONS)
        print("⚠️ Popis nenalezen – použitý fallback popis.")
        return fallback

    description_cz = translate_to_czech(description_en)

    if len(description_cz) < 50 or "MYMEMORY WARNING" in description_cz.upper():
        fallback = random.choice(FALLBACK_DESCRIPTIONS)
        print("⚠️ Popis je chybný nebo příliš krátký – použitý fallback popis.")
        return fallback

    print(f"📖 Přeložený popis pro '{book_title}':\n{description_cz}")
    return description_cz

if __name__ == "__main__":
    book_title = input("Zadej název knihy: ")
    get_and_translate_description(book_title)
