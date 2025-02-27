import os, sys, django, re

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itproger1.settings')
django.setup()

### Функції витягання адрес
def get_address_method_1(soup, company):
    return soup.find(attrs=company['address_selector']).find(None).text.strip().split('\n')[0]

def get_address_method_2(soup, company):
    elements = soup.find_all(attrs=company['address_selector'])
    return elements[1].text.strip()   

def get_address_method_3(soup, company):
    elements = soup.find_all(attrs=company['address_selector'])
    return elements[0].text.strip().split('\n')[0]  

def get_address_method_4(soup, company):
    return soup.find(attrs=company['address_selector']).find(None).text.strip()

def get_address_method_5(soup, company):
    elements = soup.find_all('p')
    return elements[5].text.strip() + elements[7].text.strip()
     
     


### Функції витягання цін
def get_price_method_1(service_price_block): 
        service_price_elements = service_price_block.find_all('span')
        min_prices_list = []
        max_prices_list = []
        for service_price_element in service_price_elements:
                price_element_text = service_price_element.text
                if price_element_text and price_element_text.isnumeric():
                   min_prices_list.append(int(price_element_text))
                elif price_element_text and not price_element_text.isnumeric():
                    try:      
                        price_element_text_without_space = price_element_text.replace(' ', '')
                        price_element_range = re.findall(r'\d+', price_element_text_without_space)
                        for min_or_max_price_index, min_or_max_price in enumerate(price_element_range):
                             if min_or_max_price_index % 2 == 0:
                                  min_prices_list.append(int(min_or_max_price))
                             else:
                                  max_prices_list.append(int(min_or_max_price))

                    except: print('Помилка')
                else: continue
        return min_prices_list, max_prices_list

def get_price_method_3(service_price_block): 
        service_price_elements = service_price_block.find_all('strong')
        min_prices_list = []
        max_prices_list = []
        for service_price_element in service_price_elements:
                price_element_text = service_price_element.text
                if price_element_text and price_element_text.isnumeric():
                   min_prices_list.append(int(price_element_text))
                elif price_element_text and not price_element_text.isnumeric():
                    try:      
                        price_element_text_without_space = price_element_text.replace(' ', '')
                        price_element_range = re.findall(r'\d+', price_element_text_without_space)
                        for min_or_max_price_index, min_or_max_price in enumerate(price_element_range):
                             if min_or_max_price_index % 2 == 0:
                                  min_prices_list.append(int(min_or_max_price))
                             else:
                                  max_prices_list.append(int(min_or_max_price))

                    except: print('Помилка')
                else: continue       
        return min_prices_list, max_prices_list

def get_price_method_4(service_price_block): 
    service_price_elements = service_price_block.find_all(class_='tn-atom')
    min_prices_list = []

    for service_price_element in service_price_elements:
        price_element_text = service_price_element.text
        if "UAH" in price_element_text:
            price_element_text_without_space = price_element_text.replace(' ', '')
            price_element_range = re.findall(r'\d+', price_element_text_without_space)
            for min_or_max_price in price_element_range:
                min_prices_list.append(int(min_or_max_price))

    return min_prices_list

def get_price_method_5(service_price_block): 
    service_price_elements = service_price_block.find_all(class_='tn-atom')
    min_prices_list = []

    for service_price_element in service_price_elements:
        price_element_text = service_price_element.text
        if "грн" in price_element_text:
            price_element_text_without_space = price_element_text.replace(' ', '')
            price_element_range = re.findall(r'\d+', price_element_text_without_space)
            for min_or_max_price in price_element_range:
                min_prices_list.append(int(min_or_max_price))
    
    return min_prices_list


