import json

from app.services.calculation_service import get_month_price as service_get_month_price, get_expensive as service_get_expensive, get_total_price as service_get_total_price, get_most_ordered as service_get_most_ordered, get_expensive_amount as service_get_expensive_amount

def get_expensive():
    return service_get_expensive()
def get_expensive_amount():
    return service_get_expensive_amount()
def get_most_ordered():
    return service_get_most_ordered()
def get_total_price():
    return service_get_total_price()
def get_month_price(month : str):
    return service_get_month_price(month)
