import requests, sys, os, django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) ###Шлях до кореневої папки для парсера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_lviv.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config')) ###Шлях до API геокодера
import config ###Імпорт файлу з API геокодера
from .decorators import geocoder_api_limit
import logging
logger = logging.getLogger(__name__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
@geocoder_api_limit
def geocode_address(address_text):
    url = 'https://geocode.search.hereapi.com/v1/geocode'

    params = {
        'q': address_text,
        'apiKey' : config.API_KEY,
        'limit': 1
    }

    response = requests.get(url, params=params, headers=headers)
    position = response.json()['items'][0]['position']
    return position['lat'], position['lng']