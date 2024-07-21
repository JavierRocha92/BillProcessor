from flask import Blueprint, request
from ..controllers.searcher_controller import search_product as controller_searcher_product

searcher = Blueprint('searcher', __name__)

@searcher.route('/', methods=['GET'])
def search_product():
    market = request.args.get('market')
    product = request.args.get('product')
    return controller_searcher_product(market, product)

