import imaplib
import email
import os
from ..config.credentials import EMAIL_CREDENTIALS
from ..db.Db import Db

def is_number(number : str):
    return number.replace(',','').isdigit()

def get_error_message(error):
    print(f' este es el error {error}')
    if 'UNIQUE' in error['message']:
        return 'this item is on database yet'


def get_unseen_emails():
    IMAP_SERVER = EMAIL_CREDENTIALS['imap_server']
    USERNAME = EMAIL_CREDENTIALS['username']
    DIR_TO_SAVE = EMAIL_CREDENTIALS['files_path']
    DESIRED_SENDER = EMAIL_CREDENTIALS['desired_sender']
    EMAIL_PASSWORD = EMAIL_CREDENTIALS['password']

    # Conectar al servidor IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(USERNAME, EMAIL_PASSWORD)

    # Seleccionar la bandeja de entrada
    mail.select("inbox")

    # Buscar correos electrónicos desde el 1 de julio hasta el 31 de julio
    status, messages = mail.search(None, f'(FROM "{DESIRED_SENDER}")')

    # Obtener la lista de IDs de los correos no leídos
    mail_ids = messages[0].split()


    # Lista para almacenar los nombres de los archivos PDF guardados
    nombres_archivos_guardados = []

    # Asegurarse de que la carpeta de destino exista
    if not os.path.isdir(DIR_TO_SAVE):
        os.makedirs(DIR_TO_SAVE)

    # Recorrer los correos no leídos
    for mail_id in mail_ids:

        status, msg_data = mail.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                from_ = msg.get("From")

                # Filtrar por remitente deseado
                if DESIRED_SENDER == from_:
                    # Si el correo tiene un cuerpo de texto o HTML
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename and filename.lower().endswith(".pdf"):
                                    filepath = os.path.join(DIR_TO_SAVE, filename)
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    nombres_archivos_guardados.append(filename)

    # Cerrar la conexión y cerrar sesión
    mail.close()
    mail.logout()

    return nombres_archivos_guardados



def findExpensive():
    query = '''
    SELECT name,AVG(price) precio_medio FROM ARTICLES WHERE name = (SELECT name FROM ARTICLES WHERE PRICE = 
    (SELECT MAX(price) FROM ARTICLES))'''
    article = Db().run_query(query)

    return {'product': article[0][0], 'price' : article[0][1]}
# Creamos una funcion para encontrar el articulo que mas dinero ha sido gastado en todas las compra
def findExpensiveAmount():
    query = '''
    SELECT name,ROUND(SUM(price),2) FROM ARTICLES GROUP BY name HAVING SUM(price) = 
    (SELECT MAX(total) FROM (SELECT SUM(price) AS total FROM ARTICLES GROUP BY name))'''
    article = Db().run_query(query)
    # mostramos por pantalla el articulo en el que mas dinero se ha gastad

    return {'product': article[0][0], 'price': article[0][1]}
# Creamos una funcion para encontrar el articulo que mas ha sido comprad
def findMostOrdered():
    # Llamamos a metodo de consulta para buscar el articulo que mas ha sido comprado
    article = Db().run_query('''
    SELECT name,SUM(uds) FROM ARTICLES GROUP BY name HAVING SUM(uds) = 
    (SELECT MAX(total) FROM (SELECT SUM(uds) AS total FROM ARTICLES GROUP BY name))''')
    # mostramos por pantalla el articulo mas comprad
    return {'product': article[0][0], 'uds' : article[0][1]}
# Metodo para calcular el precio historico de todas las compra
def totalPrice():
    price = Db().run_query('''
    SELECT ROUND(SUM(price),2) FROM purchases ''')
    # mostramos por pantalla la consulta que hemos recibid
    return {'price' : price[0][0]}
# Metodo para sacar el precio total de un mes y el precio media respecto al añ
def priceFilterMonth(month):
    # declaramos una lista con los nombres de los mese para mostrar la salida por pantall
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
              'Noviembre', 'Diciembre']
    # pasamos en valor de month a tipo string para poder trabajar con e
    month = str(month)
    # vamos a porcesar la varibale month para saber si tiene o no dos unidades para añadirle un cero el principio si solo tuviera un
    if len(month) == 1:
        month = '0' + month
    # guardamos lo que nos devuelven las consultas rn variables para poder operar con ella
    monthAmount = Db().run_query(f'''
             SELECT round(sum(price),2)  FROM purchases WHERE strftime('%m', date) = "{month}"''')
    yearAmount = Db().run_query('''
             SELECT SUM(price),COUNT(*) FROM purchases''')
    # realizmos la consulta con la fucnion que se puede ver a continuacion ya que es la indicada para procesar dates que estan guardadads como varchar en formato ISO
    print(f'El precio gastado en el mes : {months[int(month) - 1]} es de :',
          monthAmount[0][0],
          '€ el precio gastado en el año hasta ahora es de :',
          yearAmount[0][0],
          '€ el precio medio de gasto por compra en lo que va de año es de : ',
          round(float(yearAmount[0][0]) / float(yearAmount[0][1]), 2), ' €')

    # metodo para mostrar los prodcutos de una compra especifica en funcion de una fecha prporcionada







