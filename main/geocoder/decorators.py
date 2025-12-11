import os
import redis
from dotenv import load_dotenv
load_dotenv()
r = redis.Redis(host='localhost', port=6379, db=2)
geocoder_api_count_key = os.getenv('GEOCODER_API_COUNT_KEY')

import logging

logger = logging.getLogger(__name__)

def geocoder_api_limit(func):
    def wrapper(*args, **kwargs):
        try:
            count = int(r.get(geocoder_api_count_key))
        except Exception as e:
            logger.error("Помилка при читанні лічильника Redis: %s", e)
            raise

        if count <= 25000:
            try:
                result = func(*args, **kwargs)
                r.incr(geocoder_api_count_key)
                logger.debug("Виконано запит до Geocoder API. Поточний лічильник: %d", count + 1)
                return result
            except Exception as e:
                logger.exception("Помилка під час виконання функції з декоратором geocoder_api_limit")
                raise
        else:
            logger.warning("Geocoder API limit перевищено: %d запитів", count)
            raise RuntimeError("Geocoder API limit exceeded")
    return wrapper
