import PyPDF2 as pf
from ..models.PDF_Processor import PDF_Processor as proc
from ..db.Db import Db
import re
from ..models.Product import Product
from ..functions.service_functions import is_number
class PDF_Extractor():
    def __init__(self):
        pass


    def get_pdf_text(self, path):
        # Abrimos el fichero con la libreria pypdf
        pdf_obj = open(path, 'rb')
        # Gaurdamos en un variable el objeto reader y le pasamos el objet pdf que hemos creado antes
        pdf_reader = pf.PdfReader(pdf_obj)
        # vamos a decirle que pagina queremos que lea del fichero pdf
        page_obj = pdf_reader.pages[0]
        # creamos una variable text para guatrdar el texto
        return page_obj.extract_text()


    # metodo para procesar la fecha que extraemos del pdf para realizar una inserccion

    def get_purchase_date(path, lines):
        data = lines[4].split()
        purchase_date = proc().processDateInsert(data[0], data[1])
        return purchase_date

    def get_purchase_code(self, lines) -> str:
        data = lines[4].split()
        purchase_code = data[3]
        return purchase_code

    def get_purchase_price(self, lines) -> str:
        MATCH_WORD = 'TOTAL (€)'
        total_price = list(filter(lambda line : MATCH_WORD in line, lines))
        total_price = total_price[0] if len(total_price) else None

        if total_price:
            total_price = total_price.replace(MATCH_WORD, '').strip()

        return total_price

    # Metodo para extraeer los articulos de el texto dado como parametro
    def get_final_line(selfself, lines):
        TOTAL_WORD = 'TOTAL (€)'
        PARKING_WORD = '1PARKING 0,00'
        if PARKING_WORD in lines:
            print('entro aqui porque esixte la palabra parking')
            final_index = next((i for i, line in enumerate(lines) if PARKING_WORD in line), -1)
        else:
            final_index = next((i for i, line in enumerate(lines) if TOTAL_WORD in line), -1)
        return final_index
    def get_ud(self, product : list):
        return product[0][0]

    def get_name(self, product : list):
        name = ''
        pattern = r'^[\d,]+$'
        field_counter = 0
        for field in product:
            field_counter += 1
            if not re.match(pattern, field) or field_counter == 1:
                name += f' {field}'
            else:
                '''TODO tenemos que preguntar si el primer campo son solo numero para no quitarlos YA QUE ES PARTE 
                DEL NOMBRE Y NO HACE REFERENCIA A LAS UNIDADES'''

                return name[2:]

    def get_weight(self, product):
        pattern = r'^[\d,]+$'
        if Product().is_weigth(product):
            for field in product:

                if re.match(pattern, field):
                    return field
        return 0
    def get_udprice(self, product):
        print('este es el prodicto')
        print(product)
        if Product().is_weigth(product):
            return product[-3]
        else:
            return product[-2] if is_number(product[-2]) else product[-1]

    def get_price(self, product):
        return product[-1]

    def create_products(self, products : list, purchase_code : str) ->list[Product]:
        return list(map(lambda product : Product(
                                            purchase_code,
                                            self.get_ud(product),
                                            self.get_name(product),
                                            self.get_weight(product),
                                            self.get_udprice(product),
                                            self.get_price(product)), products))

    def get_articles(self,lines, purchase_code):
        product_is_in_subcategory = False
        SUBCATGORIES = ['PESCADO']
        FIRST_LINE = 7
        FINAL_LINE = self.get_final_line(lines)

        prodcuts_data = []

        for line in lines[FIRST_LINE:FINAL_LINE]:

            product_as_list = line.split()
            if product_as_list[0] not in SUBCATGORIES:

                if (Product().is_weigth(product_as_list)):
                    prodcuts_data[-1] += product_as_list
                else :
                    prodcuts_data.append(procces_uds(product_as_list))
        return self.create_products(prodcuts_data, purchase_code)

def procces_uds(product : list):
    if not is_number(product[0][0]):
        product[0]= '1' + product[0]
    return product