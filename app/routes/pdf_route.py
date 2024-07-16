from flask import Blueprint
from app.controllers.pdf_controller import insert_pdf_data as controller_insert_pdf_data


pdf = Blueprint('pdf', __name__)

@pdf.route('/', methods=['GET'])
def insert_pdf_data():
    return controller_insert_pdf_data()
