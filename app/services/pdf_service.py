
from app.db.Db import Db
def getAll():
    Db().create_tables()
    result = Db().run_query(sql='select * from purchase')
    print('estos son los resultados que hemos obtenido')
    print(result)
    return 'hola desde el servicio'
