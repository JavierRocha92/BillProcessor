
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

def get_purchases_on_db():
    query = '''SELECT code FROM purchases'''
    results = Db().run_query(query)
    results = [field[0] for field in results]
    return results

def insert_pdf_data():
    purchases_on_db = get_purchases_on_db()
    files = get_unseen_emails()
    message = 'None insertion done'
    success = False
    # 1. Creamos la ruta donde esta almacenado el fichero con los datos de la compra
    for file_name in files:

        path = f'C:\\Users\\javie\\PycharmProjects\\pythonProject\\app\\data\\{file_name}'
        # 2. Extraccion de los datos de la compra del fichero pdf en formato texto
        text = ext().get_pdf_text(path)
        lines = text.split('\n')


        # 3. Creamos un objeto compra llamando al metodo con los datos del pdf
        purchase_code = ext().get_purchase_code(lines)

        if int(purchase_code) not in purchases_on_db:
            success = True
            message = 'Insertion pdf successfully'
            print(f'Inserting product from {file_name} purchase...')
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

    return {'success': success , 'message': message }





