from flask import Flask
from flask_cors import CORS
# Importacion de todos los Blueprint que hemos creado

from app.routes.pdf_route import pdf as pdf_bp

# Creamos una instacia de la aplicacion
app = Flask(__name__)
# Envolvemos la aplicacion en la politica ce CORS para hacer peticiones cruzadas desde nuestro pc
CORS(app, expose_headers='Authorization', resources={r"/*": {"origins": "http://localhost:4200"}})


app.register_blueprint(pdf_bp, url_prefix='/pdf')


# Definir una ruta para la API
@app.route('/', methods=['GET'])
def index():
    return '¡Bienvenido a mi aplicación Flask!'
# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)