import requests
from urllib.parse import quote


def get_picture_url(first_name, last_name, gender, language='en'):
    full_name = f"{first_name} {last_name}"
    query = quote(full_name)
    url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{query}"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Nepodařilo se získat údaje z Wikipedie pro {full_name}")
        return

    data = response.json()
    title = data.get("title", full_name)
    picture_url = data.get("thumbnail", {}).get("source")

    print(f"\n📚 Wikipedia stránka: {title}")
    if picture_url:
        print(f"🖼️ Obrázek z Wikipedie: {picture_url}")
    else:
        fallback = "author_fallback_woman.png" if gender == "žena" else "author_fallback_man.png"
        fallback_path = f"images/{fallback}"  # cesta relativní k MEDIA_ROOT
        print(f"🖼️ Obrázek nenalezen – použitý fallback: /media/{fallback_path}")


if __name__ == "__main__":
    first_name = input("Zadej jméno autora/autorky: ")
    last_name = input("Zadej příjmení autora/autorky: ")
    gender = input("Zadej pohlaví (muž/žena): ").strip().lower()

    if gender not in ["muž", "zena", "žena"]:
        print("⚠️ Neplatné pohlaví. Použij 'muž' nebo 'žena'.")
    else:
        gender = "žena" if gender in ["žena", "zena"] else "muž"
        get_picture_url(first_name, last_name, gender)
