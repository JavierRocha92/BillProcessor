import json
from app.services.searcher_service import search_product_by_market as service_search_product_by_market, search_product as service_search_product
def search_product_by_market(market : str, product : str):
    time_to_sleep = 1
    return service_search_product_by_market(market, product, time_to_sleep)

def search_product(product : str):
    return service_search_product(product)