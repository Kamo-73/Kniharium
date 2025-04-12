import requests
import random
from urllib.parse import quote

# 🔁 Fallback popisy – použijú sa, ak sa nenašiel alebo bol slabý originálny popis
FALLBACK_POPISY = [
    "Tato kniha je jako tiché posezení v zapadlém knihkupectví, kde voní starý papír a čas plyne pomaleji. Nabízí nenápadný, ale hluboký příběh, který se pomalu rozvíjí jako květina v prvním jarním slunci. Ideální pro chvíle, kdy potřebujete na chvíli vypnout a znovu se zamilovat do světa slov.",
    "Tahle kniha si na nic nehraje – prostě si vás získá. Možná nenápadně, ale o to vytrvaleji. Každá stránka dýchá atmosférou, která vás obejme jako starý známý.",
    "Tato kniha je jako tajný deník, který někdo zanechal ve staré zásuvce. Každé otočení stránky je jako objev nového zákoutí lidské duše. Čtení, které nenutí běžet, ale kráčet.",
    "Kniha, kterou právě držíte v ruce, nepatří mezi tituly, které křičí z regálů. Ale to je právě její kouzlo. Pomalu a s citem vás vezme na cestu, kde nečekané neznamená nutně hlasité.",
    "Je těžké tuhle knihu někam zařadit – a to je na ní to nejlepší. Není to jen příběh, je to nálada. Atmosféra, která vás obklopí a nepustí, dokud nedočtete poslední stránku.",
    "Některé knihy nepotřebují složitou zápletku, aby vám zůstaly v paměti – stačí jim atmosféra, lidskost a pár dobře mířených vět.",
    "Tato kniha je jako nečekaný rozhovor s cizincem ve vlaku. Je v ní něco zvláštně známého, co vás nutí číst dál a dál. Každý odstavec je jako tichý úsměv.",
    "V dnešní době, kdy všechno spěchá, působí tato kniha jako zpomalený záběr ve filmu. Pocta pomalosti, tichým myšlenkám a neokázalým příběhům.",
    "Existují knihy, které vás nezmění, ale přesto si je zamilujete. Nabízí jednoduchý příběh s emocemi, které mají váhu. Čtení, co připomíná rozhovor s někým, kdo vás chápe.",
    "Tato kniha není o velkých gestech ani dramatických zlomech. Je o každodennosti, která se stává výjimečnou, když ji někdo umí popsat správnými slovy."
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
        spojeny_text = " ".join(prelozene_casti)
        return spojeny_text.replace("\n", " ").strip()
    except:
        return text.replace("\n", " ").strip()

def ziskaj_work_key(nazov_knihy):
    query = quote(nazov_knihy)
    url = f"https://openlibrary.org/search.json?title={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if data["numFound"] == 0:
        return None
    return data["docs"][0].get("key")

def ziskaj_popis_z_openlibrary(work_key):
    url = f"https://openlibrary.org{work_key}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    desc = data.get("description")
    if isinstance(desc, dict):
        return desc.get("value")
    return desc

def ziskaj_a_preloz_popis(nazov_knihy):
    work_key = ziskaj_work_key(nazov_knihy)
    if not work_key:
        fallback = random.choice(FALLBACK_POPISY)
        print(f"⚠️ Neúspešné vyhľadanie – použitý fallback popis.")
        return fallback

    popis_en = ziskaj_popis_z_openlibrary(work_key)
    if not popis_en:
        fallback = random.choice(FALLBACK_POPISY)
        print(f"⚠️ Popis nenájdený – použitý fallback popis.")
        return fallback

    popis_cs = preloz_do_cestiny(popis_en)

    if len(popis_cs) < 50:
        fallback = random.choice(FALLBACK_POPISY)
        print(f"⚠️ Popis príliš krátky – použitý fallback popis.")
        return fallback

    print(f"📖 Preložený popis pre '{nazov_knihy}':\n{popis_cs}")
    return popis_cs
