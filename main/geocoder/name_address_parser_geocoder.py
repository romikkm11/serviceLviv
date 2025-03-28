import requests, sys, os, django
from bs4 import BeautifulSoup
from companies_config import companies, headers


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) ###Шлях до кореневої папки для парсера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_lviv.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config')) ###Шлях до API геокодера

from main.models import Company
import config ###Імпорт файлу з API геокодера


for company in companies:
    response = requests.get(company['url'], headers=headers)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        company_name = soup.find('title').text.strip()
        try:
            # Виклик методу безпосередньо з параметрів компанії
            address_text = company['get_address'](soup, company)
        except AttributeError:
            print(f"Не вдалося отримати адресу для {company['url']}")

        ##Геокодер

        url = 'https://geocode.search.hereapi.com/v1/geocode'

        params = {
            'q': address_text,
            'apiKey' : config.API_KEY,
            'limit': 1
        }


        response = requests.get(url, params=params)

        company_pos = response.json()['items'][0]['position']

        company_latitude = company_pos['lat']
        company_longititude = company_pos['lng'] 
   
    #     ##Оновлення запису в БД
        company, created = Company.objects.update_or_create(
                name=company_name,
                latitude = company_latitude,
                longititude = company_longititude
            )
    else:
        print(f"Помилка: не вдалося отримати дані, код статусу: {response.status_code}")
    # print(company_name, company_latitude, company_longititude)
    # # print(company_name, address_text)






