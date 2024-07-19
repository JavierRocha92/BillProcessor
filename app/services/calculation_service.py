import json

from ..functions.service_functions import findExpensive, findExpensiveAmount, totalPrice,findMostOrdered, priceFilterMonth
def get_expensive():
    return json.dumps(findExpensive())
def get_expensive_amount():
    return json.dumps(findExpensiveAmount())
def get_most_ordered():
    return json.dumps(findMostOrdered())
def get_total_price():
    return json.dumps(totalPrice())
def get_month_price(month : str):
    return priceFilterMonth(month)

