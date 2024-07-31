import requests
from bs4 import BeautifulSoup
import json

data = []

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
        apartment_link = apartment.find("a", class_="_93444fe79c--link--eoxce")

        if name_span and address_div and price_div and price_span:
            name = name_span.text
            price = price_span.text
            address = address_div.text

            data.append({
                "name": name,
                "price": price,
                "address": address,
                "link": apartment_link["href"]
            })

with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
