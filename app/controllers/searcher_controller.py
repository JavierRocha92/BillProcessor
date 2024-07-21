import json
from app.services.searcher_service import search_product as service_searcher_product
def search_product(market : str, product : str):
    return service_searcher_product(market, product)