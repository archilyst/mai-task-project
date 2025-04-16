import requests
from bs4 import BeautifulSoup
from datetime import datetime


def parse_yandex_afisha(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []
        event_cards = soup.find_all('div', class_='Root-fq4hbj-4 fifmVY')
        for card in event_cards:
            # Название исполнителя/мероприятия
            title = card.find('h2', class_='Title-fq4hbj-3 kkgEyg').text.strip()
            # Дата проведения
            date = card.find('li', class_='DetailsItem-fq4hbj-1 DqObr').text.strip()
            # Место проведения
            place_tag = card.find('a', class_='PlaceLink-fq4hbj-2 TIeg').text.strip()
            place = place_tag.text.strip() if place_tag else "Место не указано"
            # Минимальная цена
            price_tag = card.find('span', class_='PriceBlock-njdnt8-11 cdLpTT')
            price = price_tag.text.strip() if price_tag else "Цена не указана"
            events.append({
                'title': title,
                'date': date,
                'place': place,
                'price': price
            })
        return events
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        return []


url = "https://afisha.yandex.ru/moscow/concert?date=2025-04-18&period=1"
concerts = parse_yandex_afisha(url)
for i, concert in enumerate(concerts, 1):
    print(f"{i}. {concert['title']}")
    print(f"   Дата: {concert['date']}")
    print(f"   Место: {concert['place']}")
    print(f"   Цена от: {concert['price']}")
