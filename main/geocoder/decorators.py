import os
import redis
from dotenv import load_dotenv
load_dotenv()
r = redis.Redis(host='localhost', port=6379, db=2)
geocoder_api_count_key = os.getenv('GEOCODER_API_COUNT_KEY')

def geocoder_api_limit(func):
    def wrapper(*args, **kwargs):
        count = int(r.get(geocoder_api_count_key))
        if count <= 25000:
            result = func(*args, **kwargs)
            r.incr(geocoder_api_count_key)
            return result
        else:
            raise RuntimeError("Geocoder API limit exceeded")
    return wrapper