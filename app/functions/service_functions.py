import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime
from ..config.credentials import EMAIL_CREDENTIALS

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

    # Definir las fechas de inicio y fin para julio

    start_date = "17-jul-2023"
    end_date = "02-dec-2023"

    # Buscar correos electrónicos desde el 1 de julio hasta el 31 de julio
    status, messages = mail.search(None, f'(FROM "{DESIRED_SENDER}" SINCE {start_date} BEFORE {end_date})')

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



