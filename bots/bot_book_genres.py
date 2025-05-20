import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import random

import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

from viewer.models import Genre
from django.db import transaction

# Mapping of English genres to Czech
GENRE_TRANSLATION = {
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

def get_subjects_from_openlibrary(book_title):
    query = quote(book_title)
    search_url = f"https://openlibrary.org/search?q={query}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print("❌ Nepodařilo se získat výsledky vyhledávání.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    first_link = soup.select_one("li.searchResultItem a")
    if not first_link:
        print("❌ Kniha nebyla nalezena.")
        return []

    detail_url = "https://openlibrary.org" + first_link['href']
    detail_response = requests.get(detail_url)
    if detail_response.status_code != 200:
        print("❌ Nepodařilo se načíst stránku knihy.")
        return []

    soup = BeautifulSoup(detail_response.text, "html.parser")
    subject_box = soup.select_one("div.link-box span.clamp")
    if not subject_box:
        print("⚠️ Žánry nebyly nalezeny.")
        return []

    tags = subject_box.select("a")
    subjects = [tag.get_text(strip=True) for tag in tags]
    return subjects

def get_genres(book_title):
    subjects = get_subjects_from_openlibrary(book_title)
    matches = []

    for subject in subjects:
        for en, cz in GENRE_TRANSLATION.items():
            if en.lower() in subject.lower():
                matches.append(cz)
                break

    return list(set(matches))

@transaction.atomic
def save_genres_to_database(book_title):
    matches = get_genres(book_title)

    if matches:
        for genre in matches:
            Genre.objects.get_or_create(name=genre)
        return matches

    # Fallback if nothing was found
    fallback_genres = random.sample(list(GENRE_TRANSLATION.values()), 3)
    print(f"⚠️ Nebyly nalezeny žádné žánry – použit fallback: {', '.join(fallback_genres)}")
    for genre in fallback_genres:
        Genre.objects.get_or_create(name=genre)
    return fallback_genres