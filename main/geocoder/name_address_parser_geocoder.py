import requests, sys, os, django, re
from bs4 import BeautifulSoup
from companies_config import companies, headers
from urllib.parse import urljoin
from unidecode import unidecode


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) ###Шлях до кореневої папки для парсера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_lviv.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config')) ###Шлях до API геокодера

from main.models import Company
import config ###Імпорт файлу з API геокодера
import boto3
import io

s3 = boto3.client('s3')



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

        try:
            with requests.get(urljoin(company['url'],(soup.find('link', rel='icon')['href'])), stream=True, headers=headers) as response:
                logo_name = f"{re.sub(r'[^a-z0-9]+', '-', unidecode(company_name).lower()).strip('-')}.{response.headers.get('Content-Type', '').split('/')[-1]}"
                bucket_name = os.getenv('S3_BUCKET_NAME')
                region = os.getenv('S3_REGION')
                s3.upload_fileobj(io.BytesIO(response.content), bucket_name, logo_name, ExtraArgs={'ContentType': response.headers.get('Content-Type')})
                company_logo_url = f'https://{bucket_name}.s3.{region}.amazonaws.com/{logo_name}'
                
        except AttributeError:
            print(f"Не вдалося отримати логотип для {company['url']}")
   
    # #     ##Оновлення запису в БД
        company, created = Company.objects.update_or_create(
            company_url = company['url'],
            defaults={
                'name': company_name,
                'latitude': company_latitude,
                'longititude': company_longititude,
                'logo_url': company_logo_url
            }
                
            )
    
    else:
        print(f"Помилка: не вдалося отримати дані, код статусу: {response.status_code}")






