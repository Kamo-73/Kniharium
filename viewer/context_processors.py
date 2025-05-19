import datetime
import requests


def nameday(request):
    today = datetime.date.today()
    day = f"{today.day:02}"
    month = f"{today.month:02}"
    formatted_date = f"{today.day}.{today.month}.{today.year}"

    try:
        url = f"https://svatky.adresa.info/json?date={day}{month}"
        response = requests.get(url, timeout=2)
        data = response.json()
        name = data[0]['name']
    except Exception:
        name = "neznámé"

    return {
        'name_day': name,
        'today': formatted_date
    }


def month(request):
    today = datetime.date.today().month

    if today == 1:
        mesic = "leden"
    elif today == 2:
        mesic = "únor"
    elif today == 3:
        mesic = "březen"
    elif today == 4:
        mesic = "duben"
    elif today == 5:
        mesic = "květen"
    elif today == 6:
        mesic = "červen"
    elif today == 7:
        mesic = "červenec"
    elif today == 8:
        mesic = "srpen"
    elif today == 9:
        mesic = "září"
    elif today == 10:
        mesic = "říjen"
    elif today == 11:
        mesic = "listopad"
    elif today == 12:
        mesic = "prosinec"
    return {'current_month_name': mesic}
