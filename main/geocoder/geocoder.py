import requests, sys, os, django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) ###Шлях до кореневої папки для парсера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_lviv.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config')) ###Шлях до API геокодера
import config ###Імпорт файлу з API геокодера
from .decorators import geocoder_api_limit
import logging
logger = logging.getLogger(__name__)
@geocoder_api_limit
def geocode_address(address_text):
    url = 'https://geocode.search.hereapi.com/v1/geocode'

    params = {
        'q': address_text,
        'apiKey' : config.API_KEY,
        'limit': 1
    }

    response = requests.get(url, params=params)
    try:
        1 / 0  # штучна помилка
    except Exception:
        logger.exception("Тест логування")
    try:
        data = response.json()
        logger.debug("HERE API response for '%s': %s", address_text, data)
        position = data['items'][0]['position']
        return position['lat'], position['lng']
    except KeyError:
        logger.error("HERE API не повернув 'items' для '%s'. Повна відповідь: %s", address_text, response.text)
        raise
    # position = response.json()['items'][0]['position']
    # return position['lat'], position['lng']