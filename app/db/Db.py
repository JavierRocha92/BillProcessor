# Vamos a crear una conexion con la base de datos para insertar las compras con sus distintos productos
# Importamos sqlite3
import sqlite3
#import processor as proc
from app.models.Product import Product
from app.models.Purchase import Purchase

class Db():
    def __init__(self):
        pass

# Creamos un metodo para conectarnos a la base de datos
    @staticmethod
    def connect():
        connection = sqlite3.connect('Purchase.db')
        cursor = connection.cursor()
        return connection, cursor


    # Creamos una funcion para consultar los datos de una tabla
    def run_query(self, sql):
        connection, cursor = self.connect()

        if (cursor.execute(sql)):
            return cursor.fetchall()
        else:
            print('error database connection')
        cursor.close()
        connection.commit()
        connection.close()

    def run_query_many(self):
        pass

    def create_tables(self):
        create_query_dict = {
            'article' : '''CREATE TABLE IF NOT EXISTS articles (
                            code NOT NULL,
                            uds INTEGER NOT NULL,
                            name VARCHAR(20) NOT NULL,
                            weight FLOAT(2,2) NOT NULL,
                            ud_price FLOAT(2,2) NOT NULL,
                            price FLOAT(2,2) NOT NULL,
                            PRIMARY KEY (code, name),
                            FOREIGN KEY (code) REFERENCES purchase(code)
                                )''',
            'purchase' : '''CREATE TABLE IF NOT EXISTS purchase (
                                code INTEGER PRIMARY KEY NOT NULL,
                                date VARCHAR(16) NOT NULL,
                                price FLOAT(2,2) NOT NULL
                                   )'''
        }
        connection, cursor = self.connect()
        for table, query in create_query_dict.items():
            if (cursor.execute(query)):
                print(f'Table {table} has been succesfully created')
            else:
                print(f'Something went wrong with {table} table')
        cursor.close()
        connection.commit()
        connection.close()



    # Creamos una funcion para consultar los datos de una tabla
    def insert(self, item,):
        connection, cursor = self.connect()
        item_type = self.get_item_type(item)

        query_dict = {
            'product' : '''INSERT INTO articles(code, uds, name, weight, ud_price, price) VALUES(?,?,?,?,?,?)''',
            'purchase': '''INSERT INTO purchase(code, date,price) VALUES(?,?,?)''',

        }
        if (cursor.execute(query_dict[item_type], item.to_list())):
            print('Insertion succesfully')
        else:
            print('Something went wrong')



        cursor.close()
        connection.commit()
        connection.close()

    def insert_many(self, items):
        connection, cursor = self.connect()
        item_type = self.get_item_type(items[0])
        items = [item.to_list() for item in items]

        query_dict = {
            'product': '''INSERT INTO articles(code, uds, name, weight, ud_price, price) VALUES(?,?,?,?,?,?)''',
            'purchase': '''INSERT INTO purchase(code, date,price) VALUES(?,?,?)''',
        }

        if cursor.executemany(query_dict[item_type], items):
            print('Insertion succesfully')
        else:
            print('Something went wrong')
        cursor.close()
        connection.commit()
        connection.close()

    def get_item_type(self, item):

        if(isinstance(item, Product)):
            return 'product'
        if (isinstance(item, Purchase)):
            return 'purchase'


    # Creamos una funcion para encontrar el articulo mas caro de las compras segun el precio de la unidad

    def findExpensive(self):
        # Llamaos a metodo para sacar el nombre y el precio medio del articulo que sea mas caro por su ud_price

        article = self.run_query('''
        SELECT name,AVG(price) precio_medio FROM ARTICLES WHERE name = (SELECT name FROM ARTICLES WHERE PRICE = 
        (SELECT MAX(price) FROM ARTICLES))''')

        # mostramos por pantalla el articulo en el que mas dinero se ha gastado

        print(f'El articulo mas caro  es : {article[0][0]} con un precio media por unidad de  : {article[0][1]} €')


    # Creamos una funcion para encontrar el articulo que mas dinero ha sido gastado en todas las compras

    def findExpensiveAmount(self):
        # Llamamos a metodo de consulta para buscar el articulo mque mas dinero se ha gastado
        article = self.run_query('''
        SELECT name,ROUND(SUM(price),2) FROM ARTICLES GROUP BY name HAVING SUM(price) = 
        (SELECT MAX(total) FROM (SELECT SUM(price) AS total FROM ARTICLES GROUP BY name))''')

        # mostramos por pantalla el articulo en el que mas dinero se ha gastado

        print(f'El articulo en el que mas dinero te has gastado es : {article[0][0]} con un balance de : {article[0][1]} €')


    # Creamos una funcion para encontrar el articulo que mas ha sido comprado

    def findMostOrdered(self):
        # Llamamos a metodo de consulta para buscar el articulo que mas ha sido comprado
        article = self.run_query('''
        SELECT name,SUM(uds) FROM ARTICLES GROUP BY name HAVING SUM(uds) = 
        (SELECT MAX(total) FROM (SELECT SUM(uds) AS total FROM ARTICLES GROUP BY name))''')

        # mostramos por pantalla el articulo mas comprado

        print(f'El articulo mas comprado es : {article[0][0]} con un total de {article[0][1]} uidades')


    # Metodo para calcular el precio historico de todas las compras

    def totalPrice(self):
        price = self.run_query('''
        SELECT ROUND(SUM(price),2) FROM PURCHASE ''')

        # mostramos por pantalla la consulta que hemos recibido

        print(f'El precio total es : {price[0][0]}')


    # Metodo para sacar el precio total de un mes y el precio media respecto al año

    def priceFilterMonth(self, month):
        # declaramos una lista con los nombres de los mese para mostrar la salida por pantalla

        months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre']

        # pasamos en valor de month a tipo string para poder trabajar con el

        month = str(month)

        # vamos a porcesar la varibale month para saber si tiene o no dos unidades para añadirle un cero el principio si solo tuviera una

        if len(month) == 1:
            month = '0' + month

        # guardamos lo que nos devuelven las consultas rn variables para poder operar con ellas

        monthAmount = self.run_query(f'''
                 SELECT round(sum(price),2)  FROM purchase WHERE strftime('%m', date) = "{month}"''')
        yearAmount = self.run_query('''
                 SELECT SUM(price),COUNT(*) FROM purchase''')
        # realizmos la consulta con la fucnion que se puede ver a continuacion ya que es la indicada para procesar dates que estan guardadads como varchar en formato ISO
        print(f'El precio gastado en el mes : {months[int(month) - 1]} es de :',
              monthAmount[0][0],
              '€ el precio gastado en el año hasta ahora es de :',
              yearAmount[0][0],
              '€ el precio medio de gasto por compra en lo que va de año es de : ',
              round(float(yearAmount[0][0]) / float(yearAmount[0][1]), 2), ' €'
              )

        # metodo para mostrar los prodcutos de una compra especifica en funcion de una fecha prporcionada


    '''DEBEMOS DE AÑADIR EL METODO PARA MOSTRAR LA COMPRA QUE SE LLAMA SHOWPURCHASE'''
