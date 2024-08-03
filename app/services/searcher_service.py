import time
import requests
from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json



SUPERMARKET_HEAD_URL = {
    'ahorramas': 'https://www.ahorramas.com', #V
    'carrefour': 'https://www.carrefour.es', #V
    'dia': '', #V
    'mercadona': '', #V
    'lidl': 'https://www.lidl.es/es/', #V
    'aldi': '' #V
}



driver = None

def initialize_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.javascript": 2,
            "profile.managed_default_content_settings.plugins": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.notifications": 2,
            "profile.managed_default_content_settings.automatic_downloads": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options)
    return driver

def close_driver():
    global driver
    if driver:
        driver.quit()
        driver = None


def search_product(product):
    SUPERMARKETS = ['mercadona', 'ahorramas', 'dia', 'carrefour', 'lidl', 'aldi']
    results = {}

    try:
        for market in SUPERMARKETS:
            print(f'extraccion de {market}')

            start_time = time.time()
            data = search_product_by_market(market, product)
            results[market] = json.loads(data)
            show_time(start_time, f'extraccon de{market}')
    except Exception as exc:
        print(f'Generated an exception: {exc}')

    finally:
        close_driver()

    for name in results.items():
        print(name)
        print(product)

    return json.dumps(results)
def search_product_by_market(market, product):
    initialize_driver()
    url = get_url_by_market(market, product)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Access-Control-Request-Headers': 'content-type',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Origin': 'https://www.dia.es',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Referer': 'https://www.dia.es/search?q=pechuga%20de%20pollo',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    MARKET_METHOD_INFO_EXTRACTION = {
        'ahorramas': request_get_with_headers,
        'carrefour': driver_get,
        'dia': request_get_with_headers,
        'mercadona': driver_get,
        'lidl': driver_get,
        'aldi': driver_get
    }

    if market in ['ahorramas', 'dia']:
        soup = MARKET_METHOD_INFO_EXTRACTION[market](market, url, headers)
    else:
        start_time = time.time()
        soup = MARKET_METHOD_INFO_EXTRACTION[market](market, url)
        show_time(start_time, 'extraccion de soup')

    MARKET_FUNCTIONS = {
        'ahorramas': get_product_info_ahorramas,
        'carrefour': get_product_info_carrefour,
        'dia': get_product_info_dia,
        'mercadona': get_product_info_mercadona,
        'lidl': get_product_info_lidl,
        'aldi': get_product_info_aldi
    }

    products = MARKET_FUNCTIONS[market](market, soup)
    return json.dumps(products)
def search_product__old(product : str) -> str:
    SUPERMARKETS = ['mercadona', 'ahorramas','dia','carrefour','lidl','aldi']
    results = {}
    with ThreadPoolExecutor(max_workers=len(SUPERMARKETS)) as executor:
        # Inicializar navegadores para cada mercado
        for market in SUPERMARKETS:
            initialize_driver(market, product)

        future_to_market = {executor.submit(search_product_by_market, market, product): market for market in
                            SUPERMARKETS}
        for future in as_completed(future_to_market):
            market = future_to_market[future]
            try:
                data = future.result()
                results[market] = json.loads(data)
            except Exception as exc:
                print(f'{market} generated an exception: {exc}')


    # Cerrar todos los navegadores al final
    close_driver()

    return json.dumps(results)

def search_product_by_market__old(market : str, product : str) -> str:
    url = get_url_by_market(market, product)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Access-Control-Request-Headers': 'content-type',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Origin': 'https://www.dia.es',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Referer': 'https://www.dia.es/search?q=pechuga%20de%20pollo',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    MARKET_METHOD_INFO_EXTRACTION = {
        'ahorramas': request_get_with_headers,
        'carrefour': driver_get,
        'dia': request_get_with_headers,
        'mercadona': driver_get,
        'lidl': driver_get,
        'aldi': driver_get
    }


    if market in ['ahorramas', 'dia']:
        soup = MARKET_METHOD_INFO_EXTRACTION[market](market, url, headers)
    else:
        start_time = time.time()
        soup = MARKET_METHOD_INFO_EXTRACTION[market](market, url)
        show_time(start_time, 'extraccion de soup')

    MARKET_FUNCTIONS = {
        'ahorramas': get_product_info_ahorramas,
        'carrefour': get_product_info_carrefour,
        'dia': get_product_info_dia,
        'mercadona': get_product_info_mercadona,
        'lidl': get_product_info_lidl,
        'aldi': get_product_info_aldi
    }

    products = MARKET_FUNCTIONS[market](market, soup)
    driver.quit()
    return json.dumps(products)

def show_time(start_time, function_name):
    end_time = time.time()

    # Calcular el tiempo transcurrido
    print(f'este es el tiempo que tarda la funcion de {function_name} --> {end_time - start_time}')

def request_get_with_headers(market, url, headers):
    response =  requests.get(url, headers=headers)
    soup = get_html_soup(response, market)
    return soup


def get_selector_by_market(market : str):
    MARKET_SELECTORS = {
        'ahorramas': '',
        'carrefour': 'section.ebx-grid',
        'dia': '',
        'mercadona': 'div.product-container',
        'lidl': 'div.grid-item-container',
        'aldi': 'div.tiles-grid'
    }
    return MARKET_SELECTORS[market]

def driver_get(market, url):

    page_souce = driver.get(url)

    wait = WebDriverWait(driver, 20)  # Esperar hasta 20 segundos
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, get_selector_by_market(market))))
    soup = get_html_soup(page_souce, market, driver)

    return soup


def get_html_soup(response, market : str, driver = None):
    if market == 'dia' or market == 'ahorramas':
        content = response.content
    else:
        content = driver.page_source

    return BeautifulSoup(content, 'html.parser')
def get_url_by_market(market : str, product : str):
    SUPERMATKETS = {
        'ahorramas' : f'https://www.ahorramas.com/buscador?q={get_processed_product(product)}&search-button=&lang=null',
        'carrefour' : f'https://www.carrefour.es/?q={get_processed_product(product)}',
        'dia' : f'https://www.dia.es/search?q={get_processed_product(product)}',
        'mercadona' : f'https://tienda.mercadona.es/search-results?query={get_processed_product(product)}',
        'lidl': f'https://www.lidl.es/es/search?query={get_processed_product(product)}',
        'aldi': f'https://www.aldi.es/busqueda.html?query={get_processed_product(product)}&searchCategory=Submitted%20Search'
    }

    if market not in SUPERMATKETS:
        return None
    return SUPERMATKETS[market]

def get_merged_product_name(product_name : str, product_info : list):
    processed_product_info = [get_tag_info(info) for info in product_info]
    processed_product_name = product_name + ' ' + ' '.join(processed_product_info)
    return processed_product_name

def get_processed_product(product : str) -> str:
    return product.replace(' ', '+')

def get_product_info_ahorramas(market, soup):
    products = []

    for product in soup.find_all('div', class_='product'):

        products.append({
            'name': get_tag_info(product.find('h2', class_='link product-name-gtm')),
            'price': get_tag_info(product.find('span', class_='value')),
            'image': get_tag_info(product.find('img', class_='tile-image')),
            'link': SUPERMARKET_HEAD_URL[market] + get_tag_info(product.find('a', class_='product-pdp-link')),
            'price_kg': get_tag_info(product.find('span', class_='unit-price-per-unit'))
        })
    return products

def get_product_info_dia(market, soup):
    products = []
    product = soup.find('script', id='vike_pageContext')
    if product:
        # Extrae el contenido del script
        json_text = product.string

        data = json.loads(json_text)

        search_items = data.get('INITIAL_STATE', {}).get('header', {}).get('searchData', {}).get('search_items', [])

        for item in search_items:

            products.append({
                'name' : item['display_name'],
                'price' : item['prices']['price'],
                'image': item['image'],
                'link': item['url'],
                'price_kg': item['prices']['price_per_unit']
            })

    return products

def get_product_info_mercadona(market, soup):
    products = []
    for product in soup.find_all('div', class_='product-cell'):

        products.append({
            'name': get_merged_product_name(
                product_name=get_tag_info(product.find('h4', class_='subhead1-r product-cell__description-name')),
                product_info=product.find_all('span', class_='footnote1-r'),
            ),
            'price': get_tag_info(product.find('p', class_='product-price__unit-price')),
            'image': get_tag_info(product.find('img')),
            'link': get_tag_info(product.find('a', class_='product-pdp-link')),
            'price_kg': None
        })

    return products

def get_product_info_carrefour(market, soup):

    products = []
    for product in soup.find_all('div', class_='ebx-result__wrapper'):

        products.append({
            'name': get_tag_info(product.find('h1', class_='ebx-result-title ebx-result__title')),
            'price': get_tag_info(product.find('strong', class_='ebx-result-price__value')),
            'image': get_tag_info(product.find('img', class_='ebx-result-figure__img')),
            'link': SUPERMARKET_HEAD_URL[market] + get_tag_info(product.find('a', class_='ebx-result-link')),
            'price_kg': get_tag_info(product.find('span'))
        })
    return products

def get_product_info_lidl(market, soup):
    #TODO en el caso de lidl estamos cogiendo la info para web, para cogerla para phone debemos coger la ingo del div con la clase 'space c-10 p-r p-b product-grid-box-tile__wrapper show-phone'
    products = []


    for product in soup.find_all('section', class_='space p-r p-b hide-phone'):
        products.append({
            'name': get_tag_info(product.find('strong')),
            'price': get_tag_info(product.find('span', class_='price-pill--strikethrough')),
            'image': get_tag_info(product.find('img')),
            'link': SUPERMARKET_HEAD_URL[market] + get_tag_info(product.find('a', class_='track-impression')),
            'price_kg': get_tag_info(product.find('small', class_='baseprice'))
        })
    return products

def get_product_info_aldi(market, soup):

    products = []
    for product in soup.find_all('div', class_='mod-article-tile'):

        products.append({
            'name': get_merged_product_name(
                product_name=get_tag_info(product.find('span', class_='mod-article-tile__title')),
                product_info=product.find_all('span', class_='price__unit'),
            ),
            'price': get_tag_info(product.find('span', class_='price__wrapper')),
            'image': get_tag_info(product.find('img', class_='img-responsive')),
            'link': get_tag_info(product.find('a', class_='mod-article-tile__action')),
            'price_kg': get_tag_info(product.find('span', class_='price__base'))
        })
    return products


def get_tag_info(product):

   if product is None:
       return None
   if not product.name:
       return None

   tag_name = product.name

   TAG_TYPES = {
       'strong': product.get_text() if product else None,
       'h4': product.get_text() if product else None,
       'h1': product.get_text() if product else None,
       'h2': product.get_text() if product else None,
       'p': product.get_text() if product else None,
       'small': product.get_text() if product else None,
       'span' :  product.get_text() if product else None,
       'img' : product.get('src') if product else None,
       'a' : product.get('href') if product else None
   }

   if tag_name not in TAG_TYPES :
       return None
   return TAG_TYPES[tag_name]






