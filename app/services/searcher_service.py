
from ..db.Db import Db
import json
import requests
from bs4 import BeautifulSoup
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

    print('url')
    print(url)
    response = requests.get(url, headers=headers)
    products = []


    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        MARKET_FUNCTIONS = {
            'ahorramas': get_product_info_ahorramas(soup),
            'carrefour': get_product_info_carrefour(soup),
            'dia': get_product_info_dia(soup),
            'mercadona': get_product_info_mercadona(soup)
        }

        #TODO para cada funcion debemos de poner una cabeza para la url de los links que solo tienen la parte sin la cabecera de la url

        products = MARKET_FUNCTIONS[market]


    return json.dumps(products)

def get_url_by_market(market : str, product : str):
    SUPERMATKETS = {
        'ahorramas' : f'https://www.ahorramas.com/buscador?q={get_processed_product(product)}&search-button=&lang=null',
        'carrefour' : f'https://www.carrefour.es/?q={get_processed_product(product)}',
        'dia' : f'https://www.dia.es/search?q={get_processed_product(product)}',
        'mercadona' : f'https://tienda.mercadona.es/search-results?query={get_processed_product(product)}'
    }
    if market not in SUPERMATKETS:
        return None
    return SUPERMATKETS[market]

def get_processed_product(product : str) -> str:
    return product.replace(' ', '+')

def get_product_info_ahorramas(soup):
    products = []

    for product in soup.find_all('div', class_='product'):

        products.append({
            'image': get_processed_tag(product.find('img', class_='tile-image')),
            'link': get_processed_tag(product.find('a', class_='product-pdp-link')),
            'price': get_processed_tag(product.find('span', class_='unit-price-per-unit'))
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
                'image': item['image'],
                'link': item['url'],
                'price': item['prices']['price_per_unit']
            })

    return products

def get_product_info_mercadona(soup):
    products = []

    for product in soup.find_all('div', class_='product-cell'):
        pass
        #products.append({
        #    'image': get_processed_tag(product.find('img', class_='tile-image')),
        #    'link': get_processed_tag(product.find('a', class_='product-pdp-link')),
        #    'price': get_processed_tag(product.find('span', class_='unit-price-per-unit'))
        #})
    return products

def get_product_info_carrefour(soup):

    print('entro en la funicon')
    #print(soup)
    products = []
    for product in soup.find_all('div', class_='ebx-result__wrapper'):
        print('entro en el producto')
        print(product)
        products.append({
            'image': get_processed_tag(product.find('img', class_='ebx-result-figure__img')),
            'link': get_processed_tag(product.find('a', class_='ebx-result-link')),
            'price': get_processed_tag(product.find('div', class_='ebx-result__quantity'))
        })
    return products



def get_processed_tag(product):
   if product is None:
       return None
   if not product.name:
       return None

   tag_name = product.name

   TAG_TYPES = {
       'span' :  product.get_text() if product else None,
       'img' : product.get('src') if product else None,
       'a' : product.get('href') if product else None
   }

   if tag_name not in TAG_TYPES :
       return None
   return TAG_TYPES[tag_name]






