
from ..db.Db import Db
import json
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def search_product(market : str, product : str) -> str:
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

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    contenido = driver.page_source

    driver.quit()

    soup = BeautifulSoup(contenido, 'html.parser')

    MARKET_FUNCTIONS = {
        'ahorramas': get_product_info_ahorramas(soup),
        'carrefour': get_product_info_carrefour(soup),
        'dia': get_product_info_dia(soup),
        'mercadona': get_product_info_mercadona(soup),
        'lidl': get_product_info_lidl(soup),
        'aldi': get_product_info_aldi(soup)
    }

    # TODO para cada funcion debemos de poner una cabeza para la url de los links que solo tienen la parte sin la cabecera de la url

    #TODO crear metodo para devolver las cabecera de las url de la imagen ya que vienen en relativo
    products = MARKET_FUNCTIONS[market]


    return json.dumps(products)



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

def get_product_info_ahorramas(soup):
    products = []

    for product in soup.find_all('div', class_='product'):

        products.append({
            'name': get_tag_info(product.find('h2', class_='link product-name-gtm')),
            'price': get_tag_info(product.find('span', class_='value')),
            'image': get_tag_info(product.find('img', class_='tile-image')),
            'link': get_tag_info(product.find('a', class_='product-pdp-link')),
            'price_kg': get_tag_info(product.find('span', class_='unit-price-per-unit'))
        })
    return products

def get_product_info_dia(soup):

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

def get_product_info_mercadona(soup):
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

def get_product_info_carrefour(soup):

    products = []
    for product in soup.find_all('div', class_='ebx-result__wrapper'):

        products.append({
            'name': get_tag_info(product.find('h1', class_='ebx-result-title ebx-result__title')),
            'price': get_tag_info(product.find('strong', class_='ebx-result-price__value')),
            'image': get_tag_info(product.find('img', class_='ebx-result-figure__img')),
            'link': get_tag_info(product.find('a', class_='ebx-result-link')),
            'price_kg': get_tag_info(product.find('span'))
        })
    return products

def get_product_info_lidl(soup):
    #TODO en el caso de lidl estamos cogiendo la info para web, para cogerla para phone debemos coger la ingo del div con la clase 'space c-10 p-r p-b product-grid-box-tile__wrapper show-phone'
    products = []
    for product in soup.find_all('section', class_='space p-r p-b hide-phone'):
        products.append({
            'name': get_tag_info(product.find('strong')),
            'price': get_tag_info(product.find('span', class_='price-pill--strikethrough')),
            'image': get_tag_info(product.find('img')),
            'link': get_tag_info(product.find('a', class_='track-impression')),
            'price_kg': get_tag_info(product.find('small', class_='baseprice'))
        })
    return products

def get_product_info_aldi(soup):

    products = []
    for product in soup.find_all('div', class_='mod-article-tile'):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(product)

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






