# Vamos a crear una conexion con la base de datos para insertar las compras con sus distintos productos
# Importamos sqlite3
import sqlite3

from ..functions.Db_functions import get_item_type
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
                            FOREIGN KEY (code) REFERENCES purchases(code) ON DELETE CASCADE
                                )''',
            'purchase' : '''CREATE TABLE IF NOT EXISTS purchases (
                                code INTEGER PRIMARY KEY NOT NULL,
                                date VARCHAR(16) NOT NULL,
                                price FLOAT(2,2) NOT NULL
                                   )''',
            'user' : '''CREATE TABLE IF NOT EXISTS users (
                                code INTEGER PRIMARY KEY NOT NULL,
                                email VARCHAR(100) NOT NULL,
                                password FLOAT(30) NOT NULL
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
    def insert(self, item):
        connection, cursor = self.connect()
        item_type = get_item_type(item)

        query_dict = {
            'product' : '''INSERT INTO articles(code, uds, name, weight, ud_price, price) VALUES(?,?,?,?,?,?)''',
            'purchase': '''INSERT INTO purchases(code, date,price) VALUES(?,?,?)''',
            'user': '''INSERT INTO users (email, password) VALUES(?,?)''',
        }

        try :
            cursor.execute(query_dict[item_type], item.to_list())
            response = {'success': True, 'message' : 'insertion pdf data succesfully'}
        except Exception as e:
            print(f'esta es el error que ha ocurrido {e}')
            response = {'success': False, 'message' : str(e)}

        cursor.close()
        connection.commit()
        connection.close()
        return response
    def insert_many(self, items):
        connection, cursor = self.connect()
        item_type = get_item_type(items[0])
        items = [item.to_list() for item in items]

        query_dict = {
            'product': '''INSERT INTO articles(code, uds, name, weight, ud_price, price) VALUES(?,?,?,?,?,?)''',
            'purchase': '''INSERT INTO purchases(code, date,price) VALUES(?,?,?)''',
        }
        try:
            cursor.executemany(query_dict[item_type], items)
            response = {'success': True, 'message' : 'insertion pdf data succesfully'}
        except Exception as e:

            response = {'success': False, 'message' : str(e)}

        cursor.close()
        connection.commit()
        connection.close()
        return response



