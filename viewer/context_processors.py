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