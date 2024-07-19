from ..models.Purchase import Purchase
from ..models.Product import Product
from ..models.User import User

def get_item_type(item):
    if (isinstance(item, Product)):
        return 'product'
    if (isinstance(item, Purchase)):
        return 'purchase'
    if (isinstance(item, User)):
        return 'user'