from flask import Blueprint, request
from app.controllers.calculation_controller import get_month_price as controller_get_month_price, get_total_price as controller_get_total_price, get_expensive as controller_get_expensive, get_expensive_amount as controller_get_expensive_amount, get_most_ordered as controller_get_most_ordered


calculation = Blueprint('calculation', __name__)

@calculation.route('/expensive', methods=['GET'])
def get_expesnsive():
    return controller_get_expensive()
@calculation.route('/expensive_amount', methods=['GET'])
def get_expensive_amount():
    return controller_get_expensive_amount()
@calculation.route('/most_ordered', methods=['GET'])
def get_most_ordered():
    return controller_get_most_ordered()
@calculation.route('/total_price', methods=['GET'])
def get_total_price():
    return controller_get_total_price()
@calculation.route('/month_amount', methods=['GET'])
def gte_month_price():
    month = request.args.get('month')
    return controller_get_month_price(month)




