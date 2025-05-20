import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kniharium.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from datetime import datetime

USERS = [
    {
        "username": "kvietok23",
        "email": "kvietok23@gmail.com",
        "first_name": "Jan",
        "last_name": "Novák",
        "date_of_birth": "1982-03-12",
        "biography": "Miluju přírodu a ticho lesa mi vždycky udělá dobře.",
    },
    {
        "username": "LibertyFox",
        "email": "libertyfox@seznam.cz",
        "first_name": "Tomáš",
        "last_name": "Svoboda",
        "date_of_birth": "1996-07-28",
        "biography": "Píšu, fotím a věřím, že v jednoduchosti je krása.",
    },
    {
        "username": "spoi",
        "email": "spoi@email.cz",
        "first_name": "Lukáš",
        "last_name": "Dvořák",
        "date_of_birth": "2002-11-09",
        "biography": "Zajímám se o technologie, ale nejvíc si vážím upřímnosti.",
    },
    {
        "username": "ShadowRider",
        "email": "shadowrider123@gmail.com",
        "first_name": "Petr",
        "last_name": "Marek",
        "date_of_birth": "1973-01-03",
        "biography": "Mám rád hudbu, dobré knihy a slušnost v každé době.",
    },
    {
        "username": "Tranzit7",
        "email": "tranzit7@centrum.cz",
        "first_name": "Martin",
        "last_name": "Procházka",
        "date_of_birth": "1989-06-19",
        "biography": "Rád přemýšlím o věcech do hloubky a vedu smysluplné rozhovory.",
    },
    {
        "username": "lilie.sky",
        "email": "lilie.sky@seznam.cz",
        "first_name": "Anna",
        "last_name": "Novotná",
        "date_of_birth": "1955-05-05",
        "biography": "Ráda rozdávám úsměv a věřím, že laskavost mění svět.",
    },
    {
        "username": "kat_blackcat",
        "email": "kat.blackcat@gmail.com",
        "first_name": "Kateřina",
        "last_name": "Černá",
        "date_of_birth": "1999-09-17",
        "biography": "Píšu, pozoruju a často hledám krásu v obyčejnosti.",
    },
    {
        "username": "LucidEcho",
        "email": "lucidecho@email.cz",
        "first_name": "Lucie",
        "last_name": "Horáková",
        "date_of_birth": "1985-12-30",
        "biography": "Miluju ticho, dobré knihy a ľudí, kteří umí naslouchat.",
    },
    {
        "username": "vera.nika",
        "email": "vera.nika@centrum.cz",
        "first_name": "Veronika",
        "last_name": "Králová",
        "date_of_birth": "2004-04-11",
        "biography": "Jsem snílek s hlavou v oblacích a srdcem na správném místě.",
    },
    {
        "username": "SilentStar9",
        "email": "silentstar9@gmail.com",
        "first_name": "Tereza",
        "last_name": "Pokorná",
        "date_of_birth": "1978-08-26",
        "biography": "Ráda tvořím, pomáhám a věřím na malé zázraky každého dne.",
    },
    {
        "username": "davezone",
        "email": "davezone@gmail.com",
        "first_name": "David",
        "last_name": "Malý",
        "date_of_birth": "1987-08-21",
        "biography": "Rád sleduju dění kolem sebe a dělám si vlastní názor.",
    },
    {
        "username": "jakubnet",
        "email": "jakubnet@seznam.cz",
        "first_name": "Jakub",
        "last_name": "Růžička",
        "date_of_birth": "1975-02-04",
        "biography": "Věci si rád ověřím a snažím se držet faktů.",
    },
    {
        "username": "mh_log",
        "email": "mh_log@email.cz",
        "first_name": "Milan",
        "last_name": "Havelka",
        "date_of_birth": "1990-06-16",
        "biography": "Zajímám se o technologie, zprávy a běžný život.",
    },
    {
        "username": "radekline",
        "email": "radekline@centrum.cz",
        "first_name": "Radek",
        "last_name": "Kříž",
        "date_of_birth": "1966-12-29",
        "biography": "Nejsem moc vidět, ale sleduju skoro všechno.",
    },
    {
        "username": "voxel.cz",
        "email": "voxel.cz@gmail.com",
        "first_name": "Vojtěch",
        "last_name": "Kolář",
        "date_of_birth": "1998-10-07",
        "biography": "Občas něco přidám, když mám co říct.",
    },
    {
        "username": "eva.box",
        "email": "eva.box@seznam.cz",
        "first_name": "Eva",
        "last_name": "Benešová",
        "date_of_birth": "1980-03-13",
        "biography": "Mám ráda pořádek, klid a věcné diskuze.",
    },
    {
        "username": "janette.cz",
        "email": "janette.cz@gmail.com",
        "first_name": "Jana",
        "last_name": "Urbanová",
        "date_of_birth": "1962-11-25",
        "biography": "Sleduju dění kolem, ale do ničeho se necpu.",
    },
    {
        "username": "nik.notes",
        "email": "nik.notes@email.cz",
        "first_name": "Nikola",
        "last_name": "Veselá",
        "date_of_birth": "1994-09-06",
        "biography": "Občas něco přečtu, občas něco okomentuju.",
    },
    {
        "username": "peta_input",
        "email": "peta_input@centrum.cz",
        "first_name": "Petra",
        "last_name": "Slavíková",
        "date_of_birth": "2000-05-18",
        "biography": "Dávám přednost jednoduchosti a jasnému vyjádření.",
    },
    {
        "username": "ak_skl",
        "email": "ak_skl@gmail.com",
        "first_name": "Alena",
        "last_name": "Krátká",
        "date_of_birth": "1988-01-02",
        "biography": "Nejsem expert, ale zajímají mě různé názory.",
    },
    {
        "username": "true.fil",
        "email": "true.fil@gmail.com",
        "first_name": "Filip",
        "last_name": "Hrdina",
        "date_of_birth": "1985-04-03",
        "biography": "Většina lidí jen plácá. Já mluvím k věci.",
    },
    {
        "username": "dom_critic",
        "email": "dom_critic@seznam.cz",
        "first_name": "Dominik",
        "last_name": "Král",
        "date_of_birth": "1992-01-15",
        "biography": "Nečekej, že budu souhlasit jen proto, že máš pocit.",
    },
    {
        "username": "alextight",
        "email": "alextight@email.cz",
        "first_name": "Aleš",
        "last_name": "Tomšík",
        "date_of_birth": "1976-07-23",
        "biography": "Názory mám tvrdé, protože svět je měkký.",
    },
    {
        "username": "kar.sv",
        "email": "kar.sv@centrum.cz",
        "first_name": "Karel",
        "last_name": "Švec",
        "date_of_birth": "1960-10-10",
        "biography": "Nepíšu často, ale když už, tak to má váhu.",
    },
    {
        "username": "obzero",
        "email": "obzero@gmail.com",
        "first_name": "Ondřej",
        "last_name": "Bláha",
        "date_of_birth": "1999-05-27",
        "biography": "Nesuď mě podle tónu, ale podle obsahu. Pokud to zvládneš.",
    },
    {
        "username": "sim_sharp",
        "email": "sim_sharp@seznam.cz",
        "first_name": "Simona",
        "last_name": "Richterová",
        "date_of_birth": "1983-06-06",
        "biography": "Nejsem tady, abych hladila ego.",
    },
    {
        "username": "ivy_note",
        "email": "ivy_note@gmail.com",
        "first_name": "Iveta",
        "last_name": "Mašková",
        "date_of_birth": "1971-09-30",
        "biography": "Řeknu, co si myslím. A často se to neslyší rádo.",
    },
    {
        "username": "sandrix",
        "email": "sandrix@email.cz",
        "first_name": "Sandra",
        "last_name": "Čechová",
        "date_of_birth": "2001-02-12",
        "biography": "Nemám trpělivost na hlouposti.",
    },
    {
        "username": "bkn_point",
        "email": "bkn_point@centrum.cz",
        "first_name": "Barbora",
        "last_name": "Konečná",
        "date_of_birth": "1995-08-04",
        "biography": "Neber si mě osobně. Já to tak myslím obecně.",
    },
    {
        "username": "luc.fix",
        "email": "luc.fix@gmail.com",
        "first_name": "Lucie",
        "last_name": "Holá",
        "date_of_birth": "1989-12-19",
        "biography": "Buď věcný, nebo mlč. To platí i pro mě.",
    },
]

for data in USERS:
    username = data["username"]

    if User.objects.filter(username=username).exists():
        print(f"⏭️ Užívateľ {username} už existuje. Preskakujem.")
        continue

    user = User.objects.create_user(
        username=username,
        email=data["email"],
        password="ahojahoj",
        first_name=data["first_name"],
        last_name=data["last_name"],
    )
    print(f"✅ Vytvorený User: {username}")

    # Create profile
    profile, created = Profile.objects.get_or_create(user=user)
    profile.date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
    profile.biography = data["biography"]
    profile.save()
    print(f"🧾 Profil pridaný: {username}")


# import bots.users_add