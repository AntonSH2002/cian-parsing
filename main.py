import re
import requests
from bs4 import BeautifulSoup
import json
from geopy.geocoders import Nominatim

# https://habr.com/ru/articles/664888/

data = []

geolocator = Nominatim(user_agent="GetLoc")

for i in range(1, 16):
    url = f"https://barnaul.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={i}&region=4668"
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    apartments = bs.findAll("div", class_="_93444fe79c--card--ibP42")

    for apartment in apartments:
        name_span = apartment.find("a", class_="_93444fe79c--link--VtWj6")
        address_div = apartment.find("div", class_="_93444fe79c--labels--L8WyJ")
        price_div = apartment.find("div", class_="_93444fe79c--container--aWzpE")
        price_span = price_div.find("span", class_="_93444fe79c--color_black_100--Ephi7")
        price_square_meter_p = apartment.find("p", class_="_93444fe79c--color_gray60_100--mYFjS")
        apartment_link = apartment.find("a", class_="_93444fe79c--link--eoxce")

        if name_span and address_div and price_div and price_span and price_square_meter_p:
            name = name_span.text
            price = int(price_span.text.replace(" ", "").replace(" ", "").replace("₽", ""))
            price_square_meter = int(price_square_meter_p.text.replace(" ", "").replace(" ", "").replace("₽", "")
                                     .replace("/м²", ""))
            address = address_div.text
            address_for_location = address.replace("р-н", "")
            address_for_location = re.sub(r'\sмкр\.\s[^,]+,\s*', '', address_for_location)
            location = geolocator.geocode(address_for_location)

            if location:
                data.append({
                    "Объявление": name,
                    "Цена": price,
                    "Цена за квадратный метр": price_square_meter,
                    "Адрес": address,
                    "Ссылка": apartment_link["href"],
                    "Долгота": location.latitude,
                    "Широта": location.longitude
                })
            else:
                data.append({
                    "Объявление": name,
                    "Цена": price,
                    "Цена за квадратный метр": price_square_meter,
                    "Адрес": address,
                    "Ссылка": apartment_link["href"],
                    "Долгота": None,
                    "Широта": None
                })

data.sort(key=lambda x: x["Цена"])

with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
