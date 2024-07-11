class PDF_Processor():
    def __init__(self):
        pass

    # Metodo para processar la lista de strings de prodcuto
    def processText(self, p):
        # Insertamos en la posicion 0 el primer caracter de la posicion 0 que indica las unidades del producto
        p.insert(0, p[0].pop(0))
        # Ahora borramos la unidad de la posicion anterior que ahora pasa a ser la posicion 1
        # p[1] = p[0][1:]
        # Recorremos la lista para borrar los caracteres que no queramos en el procesamiento
        for i in range(0, len(p)):
            p[i] = p[i].replace(',', '.')
            p[i] = p[i].replace(' kg', '')
        return p

    def processLine(self, precio, pr, weight):
        # Realizamos un bucle for para recorrer la lista de producto y generar solo los campos necesarios
        # uniendolos segun el patron  para dejar solo los campos necesarios
        while (True):
            if weight == False:
                # buscamos si la segunda posicion de la lista contiene un precio
                if precio.search(pr[1]):
                    # Si la lomgitud de la lista es de dos entonces
                    if len(pr) == 2:
                        pr.insert(1, pr[1])
                    if len(pr) == 3:
                        # Si la longitud de la lista es de 3 entonces en la posicion 1 metemos unt exto vacio para que actue como el peso
                        pr.insert(1, '')
                    break
                else:
                    # Cuando no se encuentra la expresion regular vamos a guardar en la poscion cero lo que ya tenia mas lo que hay en
                    # la posicion 1 para formar en una sola poscion el nombre entero del producto
                    pr[0] += ' ' + pr[1]
                    pr.pop(1)
            else:
                """ EL ERROR ESTA AQUI YA QUE SI EL NOMBRE DE LS FRUTA ESTA COMPUESTO NOS VA A BORRAR LOS ELEMETNOS 
                CORRIDOS UNA POSICION A LA DERECHA"""

                # Si es una fruta lo que hacemos es borrar los datos que no nos sirvan para el procesamiento

                pr.pop(pr.index('€/kg'))
                pr.pop(pr.index('kg'))
                weight = False
        return pr, weight

    # Metodo para extraer la fecha del fichero para darla el formato correcto para la insercion

    def processDateInsert(self, date, hour):
        # primero vamos a meter en valor del año en la poscion 0
        date = date[6:] + date
        # ahora añadimos el dia en la ultima posicion
        date = date + date[4:6]
        # en este paso vamos a borrar en año que habia en la ultima posicion y la fecha de la primera para ello damos un nuevo valor a la variable saltandonos dichas posiciones
        # y asu vez lo concatenamos con lo separadores, y en el final le vamos a concatenar tambien la hora
        date = date[:4] + '-' + date[7:9] + '-' + date[14:] + ' ' + hour
        return date

    # metodo para darle formato correcto a los valores de una fecha pra realizar una consulta

    def processDateSelect(self, date):
        if len(date[0]) == 1:
            date[0] = '0' + date[0]
        if len(date[1]) == 1:
            date[1] = '0' + date[1]
        if len(date[2]) == 2:
            date[2] = '20' + date[2]
        return date

