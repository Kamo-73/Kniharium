import requests
import random
from urllib.parse import quote

# 🔁 Fallback biografie – muži
FALLBACK_BIO_MUZ = [
    "Autor začal písať už v desiatich rokoch, keď vznikli prvé básne inšpirované prírodou a rodinným prostredím...",
    "Literárna cesta autora sa začala počas dlhých letných prázdnin na dedine, kde prístup k technológiám bol minimálny...",
    "Autor sa dlhé roky venoval divadlu a filmovej tvorbe, pričom pôsobil ako dramaturg aj scenárista...",
    "Po rokoch strávených cestovaním po rôznych krajinách a kontinentoch sa autor rozhodol usadiť a spracovať všetky zážitky...",
    "Autor pôvodne študoval fyziku a niekoľko rokov pracoval v akademickom prostredí ako výskumník...",
    "Autor sa venuje písaniu najmä v neskorých večerných hodinách, keď sa svet stíši a myšlienky získavajú hĺbku...",
    "Prvú poviedku autor napísal počas vyučovania matematiky na strednej škole – bola to krátka hororová scéna...",
    "Autor pochádza z malého mesta, kde sa silné príbehy odovzdávali medzi generáciami pri kuchynskom stole...",
    "V mladosti autor túžil byť hudobníkom – skladal piesne, hral na klavíri a vystupoval na školských podujatiach...",
    "Autor sa dlho hľadal – začínal s rozprávkami pre deti, prešiel cez poviedky pre mládež, neskôr vyskúšal publicistiku..."
]

# 🔁 Fallback biografie – ženy
FALLBACK_BIO_ZENA = [
    "Autorka začala písať už ako dieťa, keď si vymýšľala príbehy pre svoje bábiky a zapisovala ich do školských zošitov...",
    "Autorka vyrastala obklopená knihami, ktoré jej matka nosila z knižnice. Už ako tínedžerka si viedla čitateľský denník...",
    "Autorka pôsobila dlhé roky v oblasti filmu a divadla, kde sa venovala réžii a scenáristike...",
    "Po rokoch strávených v zahraničí sa autorka rozhodla usadiť a zachytiť svoje cestovateľské zážitky vo forme príbehov...",
    "Autorka študovala matematiku a informatiku, no počas dlhých večerov si písala vlastné príbehy len pre seba...",
    "Písanie sa pre autorku stalo útočiskom počas náročného životného obdobia...",
    "Autorka písala odjakživa, no prvý skutočný príbeh vznikol v lavici počas hodiny fyziky...",
    "Autorka vyrástla v dedinskom prostredí, kde sa príbehy šírili ústnym podaním...",
    "V detstve sa autorka venovala hudbe – hrala na klavíri a písala texty piesní...",
    "Autorka si prešla rôznymi fázami – najprv písala pre deti, potom pre mládež, neskôr skúšala žurnalistiku..."
]

def preloz_do_cestiny(text):
    try:
        casti = [text[i:i+500] for i in range(0, len(text), 500)]
        prelozene_casti = []
        for cast in casti:
            resp = requests.get(f"https://api.mymemory.translated.net/get?q={quote(cast)}&langpair=en|cs")
            data = resp.json()
            preklad = data['responseData']['translatedText']
            prelozene_casti.append(preklad)
        return " ".join(prelozene_casti).strip()
    except:
        return text.strip()

def ziskaj_popis_z_wikipedie(cele_meno):
    query = quote(cele_meno)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get("extract", "")

def zobraz_biografiu(meno, priezvisko, pohlavie):
    cele_meno = f"{meno} {priezvisko}"
    popis_en = ziskaj_popis_z_wikipedie(cele_meno)

    if not popis_en or len(popis_en.strip()) < 50:
        fallback = random.choice(FALLBACK_BIO_MUZ if pohlavie == "muž" else FALLBACK_BIO_ZENA)
        print(f"⚠️ Popis chýba alebo je príliš krátky – použitý fallback:")
        print(f"📖 Biografia:\n{fallback}")
        return

    popis_cs = preloz_do_cestiny(popis_en)
    if len(popis_cs.strip()) < 50 or "MYMEMORY WARNING" in popis_cs.upper():
        fallback = random.choice(FALLBACK_BIO_MUZ if pohlavie == "muž" else FALLBACK_BIO_ZENA)
        print(f"⚠️ Preklad zlyhal alebo je príliš krátky – použitý fallback:")
        print(f"📖 Biografia:\n{fallback}")
        return

    print(f"📖 Biografia (preložená):\n{popis_cs}")

if __name__ == "__main__":
    meno = input("Zadaj meno autora/autorky: ")
    priezvisko = input("Zadaj priezvisko autora/autorky: ")
    pohlavie = input("Zadaj pohlavie (muž/žena): ").strip().lower()
    if pohlavie not in ["muž", "zena", "žena"]:
        print("⚠️ Neplatné pohlavie. Použi 'muž' alebo 'žena'.")
    else:
        pohlavie = "žena" if pohlavie in ["žena", "zena"] else "muž"
        zobraz_biografiu(meno, priezvisko, pohlavie)
