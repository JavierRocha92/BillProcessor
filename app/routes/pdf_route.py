from flask import Blueprint
from app.controllers.pdf_controller import getAll


pdf = Blueprint('pdf', __name__)

@pdf.route('/', methods=['GET'])
def save_purchase_from_pdf():
    return getAll()
