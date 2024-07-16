
from app.db.Db import Db
from ..models.PDF_Extractor import PDF_Extractor as ext
import os
from ..models.Purchase import Purchase
from ..db.Db import Db
from ..functions.service_functions import get_error_message, get_unseen_emails
import json

def insert_purchase(purchase):
    return Db().insert(purchase)

def insert_product(product):
    Db().insert(product)



def insert_pdf_data():



    files = get_unseen_emails()

    message = ''
    # 1. Creamos la ruta donde esta almacenado el fichero con los datos de la compra
    for file_name in files:
        print(f'Inserting product from {file_name} purchase...')
        path = f'C:\\Users\\javie\\PycharmProjects\\pythonProject\\app\\data\\{file_name}'
        # 2. Extraccion de los datos de la compra del fichero pdf en formato texto
        text = ext().get_pdf_text(path)
        lines = text.split('\n')


        # 3. Creamos un objeto compra llamando al metodo con los datos del pdf
        purchase_code = ext().get_purchase_code(lines)
        purchase_date = ext().get_purchase_date(lines)
        purchase_price = ext().get_purchase_price(lines)

        purchase = Purchase(code=purchase_code, date=purchase_date, total_price=purchase_price)
        purchase.products = ext().get_articles(lines, purchase_code)

        result = insert_purchase(purchase)

        if result['success']:
            for product in purchase.products:
                insert_product(product)
        else:
            message = get_error_message(result)

        response = {'success': result['success'], 'message': message if message else result['message']}

    return json.dumps('hola masquina')



