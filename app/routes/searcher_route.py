from flask import Blueprint, request
from ..controllers.searcher_controller import search_product_by_market as controller_search_product_by_market, search_product as controller_search_product

searcher = Blueprint('searcher', __name__)

@searcher.route('/', methods=['GET'])
def search_product_by_market():
    market = request.args.get('market')
    product = request.args.get('product')
    return controller_search_product_by_market(market, product)
@searcher.route('/all_markets', methods=['GET'])
def search_product():
    product = request.args.get('product')
    return controller_search_product(product)


