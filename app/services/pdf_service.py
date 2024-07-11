
from app.db.Db import Db
from ..models.PDF_Extractor import PDF_Extractor as ext
import os
from ..models.Purchase import Purchase
from ..db.Db import Db

def insert_purchase(purchase):
    Db().insert(purchase)

def insert_product(product):
    Db().insert(product)



def getAll():
    #1. Creamos la ruta donde esta almacenado el fichero con los datos de la compra
    file_name = 'fichero2'
    path = f'C:\\Users\\javie\\PycharmProjects\\pythonProject\\app\\data\\{file_name}.pdf'
    #2. Extraccion de los datos de la compra del fichero pdf en formato texto
    text = ext().get_pdf_text(path)
    lines = text.split('\n')

    print('estas son las lineas')
    print(lines)

    #3. Creamos un objeto compra llamando al metodo con los datos del pdf
    purchase_code = ext().get_purchase_code(lines)
    purchase_date = ext().get_purchase_date(lines)
    purchase_price = ext().get_purchase_price(lines)


    purchase = Purchase(code=purchase_code, date=purchase_date, total_price=purchase_price)
    purchase.products = ext().get_articles(lines, purchase_code)
    insert_purchase(purchase)

    for product in purchase.products:
        insert_product(product)


    return f'estos son los datos de la compra {purchase_date}'

