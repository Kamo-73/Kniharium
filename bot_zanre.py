import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from viewer.models import Genre
from django.db import transaction

# Mapa anglických žánrov na české
PREKLAD_ZANROV = {
    "Fiction": "Beletria",
    "Nonfiction": "Literatura faktu",
    "Romance": "Romantika",
    "Science Fiction": "Sci-fi",
    "Fantasy": "Fantasy",
    "Dark Fantasy": "Temná fantasy",
    "Urban Fantasy": "Městská fantasy",
    "High Fantasy": "Vysoká fantasy",
    "Epic Fantasy": "Epická fantasy",
    "Horror": "Horor",
    "Thriller": "Thriller",
    "Psychological Thriller": "Psychologický thriller",
    "Mystery": "Detektívka",
    "Crime": "Zločin",
    "Historical Fiction": "Historická beletria",
    "Historical Romance": "Historická romantika",
    "Biography": "Biografie",
    "Autobiography": "Autobiografie",
    "Memoir": "Paměti",
    "Self-Help": "Osobní rozvoj",
    "Health": "Zdraví",
    "Psychology": "Psychologie",
    "Philosophy": "Filozofie",
    "Religion": "Náboženství",
    "Spirituality": "Spiritualita",
    "Poetry": "Poezie",
    "Drama": "Drama",
    "Classics": "Klasika",
    "Young Adult": "Pro mládež",
    "Children": "Dětské knihy",
    "Middle Grade": "Pro starší děti",
    "New Adult": "Pro mladé dospělé",
    "Adventure": "Dobrodružství",
    "Action": "Akce",
    "Comics": "Komiksy",
    "Graphic Novels": "Grafické romány",
    "Art": "Umění",
    "Cookbooks": "Kuchařky",
    "Travel": "Cestování",
    "Science": "Věda",
    "Technology": "Technologie",
    "Engineering": "Inženýrství",
    "Mathematics": "Matematika",
    "Education": "Vzdělávání",
    "Business": "Podnikání",
    "Economics": "Ekonomie",
    "Politics": "Politika",
    "Law": "Právo",
    "War": "Válka",
    "Military": "Armáda",
    "Music": "Hudba",
    "Animals": "Zvířata",
    "Nature": "Příroda",
    "Environment": "Životní prostředí",
    "Parenting": "Rodičovství",
    "Sports": "Sport",
    "True Crime": "Skutečné zločiny",
    "LGBT": "LGBT+",
    "Gender Studies": "Genderová studia",
    "Cyberpunk": "Kyberpunk",
    "Steampunk": "Steampunk",
    "Dystopia": "Dystopie",
    "Utopia": "Utopie",
    "Aliens": "Mimozemšťané",
    "Vampires": "Upíři",
    "Werewolves": "Vlkodlaci",
    "Zombies": "Zombíci",
    "Witches": "Čarodějnice",
    "Magic": "Magie",
    "Witchcraft": "Čarodějnictví",
    "Mythology": "Mytologie",
    "Fairy Tales": "Pohádky",
    "Folklore": "Folklor",
    "Supernatural": "Nadpřirozeno",
    "Paranormal": "Paranormální",
    "Time Travel": "Cestování časem",
    "Coming of Age": "Dospívání",
    "Survival": "Přežití",
    "Military Fiction": "Válečná beletria",
    "Satire": "Satira",
    "Humor": "Humor",
    "Western": "Western",
    "Political Fiction": "Politická beletria",
    "Epistolary Novel": "Román v dopisech",
    "Psychological Fiction": "Psychologická beletria",
    "Gothic Fiction": "Gotická beletria",
    "Literary Criticism": "Literární kritika"
}

def ziskaj_subjects_openlibrary(nazov_knihy):
    query = quote(nazov_knihy)
    search_url = f"https://openlibrary.org/search?q={query}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print("❌ Nepodarilo sa získať výsledky vyhľadávania.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    prvy_odkaz = soup.select_one("li.searchResultItem a")
    if not prvy_odkaz:
        print("❌ Kniha nebola nájdená.")
        return []

    detail_url = "https://openlibrary.org" + prvy_odkaz['href']
    detail_response = requests.get(detail_url)
    if detail_response.status_code != 200:
        print("❌ Nepodarilo sa načítať stránku knihy.")
        return []

    soup = BeautifulSoup(detail_response.text, "html.parser")
    subject_box = soup.select_one("div.link-box span.clamp")
    if not subject_box:
        print("⚠️ Subjekty neboli nájdené.")
        return []

    tags = subject_box.select("a")
    subjects = [tag.get_text(strip=True) for tag in tags]
    return subjects

def ziskaj_zanre(nazov_knihy):
    subjects = ziskaj_subjects_openlibrary(nazov_knihy)
    zhody = []

    for s in subjects:
        for en, cz in PREKLAD_ZANROV.items():
            if en.lower() in s.lower():
                zhody.append(cz)
                break

    zhody = list(set(zhody))
    return zhody

@transaction.atomic
def uloz_zanre_do_databazy(nazov_knihy):
    zhody = ziskaj_zanre(nazov_knihy)
    if not zhody:
        print("❌ Nenašli sa žiadne známe žánre.")
        return []

    print(f"\n✅ Pridávam žánre do DB pre knihu '{nazov_knihy}':")
    for zaner in zhody:
        obj, created = Genre.objects.get_or_create(name=zaner)
        if created:
            print(f"  ➕ Pridaný žáner: {zaner}")
        else:
            print(f"  ✔️ Už existuje: {zaner}")
    return zhody
