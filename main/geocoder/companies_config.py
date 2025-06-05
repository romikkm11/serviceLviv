import os, sys, django
# 
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_lviv.settings')

django.setup()
load_dotenv()
import methods
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

companies = [
    {
        'url' : os.getenv('URL_1'),
        'address_selector' : {'data-id': 'ef86798'},
        'get_address': methods.get_address_method_1,
        'price_url' : os.getenv('URL_1_price'),
        'price_selector' : {'class' : 'elementor-tabs'},
        'get_price' : methods.get_price_method_1,
        'min_prices_recording_sequence' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
        'max_prices_recording_sequence' : [14, 20, 21, 22, 33, 46, 47, 48, 49, 53],
        'db_id' : 1,
        'service_type_id' : 1

    },
# # #     {
# # #         'url' : os.getenv('URL_2'),
# # #         'address_selector' : {'class': 'footer-info'},
# # #         'get_address': get_address_method_2 
# # #     },
    {
        'url' : os.getenv('URL_3'),
        'address_selector' : {'class' : 'header-address text-left'},
        'get_address': methods.get_address_method_3,
        'price_url' : os.getenv('URL_3_price'),
        'price_selector' : 'tbody',
        'get_price' : methods.get_price_method_3,
        'min_prices_recording_sequence' : [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75],
        'max_prices_recording_sequence' : [58, 60, 61],
        'db_id' : 2,
        'service_type_id' : 1
    },
    {
        'url' : os.getenv('URL_4'),
        'address_selector': {'class': 'cursor-pointer flex flex-col gap-[5px]'},
        'get_address': methods.get_address_method_4,
        'price_url' : os.getenv('URL_4'),
        'price_selector': { 'class': 'p-[90px_24px_44px]'},
        'get_price' : methods.get_price_method_4,
        'min_prices_recording_sequence' : [76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92],
        'db_id' : 3,
        'service_type_id' : 2
    },
    {
        'url' : os.getenv('URL_5'),
        'address_selector' : {'class' : 't-descr_sm'},
        'get_address': methods.get_address_method_5,
        'price_url' : os.getenv('URL_5'),
        'price_selector' : { 'data-artboard-recid' : '330275433' },
        'get_price' : methods.get_price_method_5,
        'min_prices_recording_sequence' : [94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105],
        'db_id' : 4,
        'service_type_id' : 2
    } 
]