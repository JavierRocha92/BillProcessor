# Importyamos el atributo attrgettter de la libreria operator
from operator import attrgetter


# Creamos una clase de compras para almacenar los productos realizados en una misma
# compra por grupos y poder operar con ellos

class Purchase(object):
    products = []

    def __init__(self, code = None, date = None, total_product=None, total_price=None):
        """ Constructor e la clase Purchase """
        self.code = code
        self.date = date
        self.total_product = total_product
        self.total_price = total_price

    # Getter y Setter para 'code'
    @property
    def code(self):
        return self._code
    @code.setter
    def code(self, value):
        self._code = value
    # Getter y Setter para 'date'
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, value):
        self._date = value
    # Getter y Setter para 'total_product'
    @property
    def total_product(self):
        return self._total_product
    @total_product.setter
    def total_product(self, value):
        self._total_product = value
    # Getter y Setter para 'total_price'
    @property
    def total_price(self):
        return self._total_price
    @total_price.setter
    def total_price(self, value):
        self._total_price = value

    def to_list(self):
        return [self.code, self.date, self.total_price]

    def findExpensive(self):
        """ Este metodo develve el producto que mas cuesta en su precio por unidad """
        # Sacamos el producto con mayor precio pasandole como patametro key ud_price
        expensive = max(self.products, key=attrgetter('ud_price'))
        return expensive

    def findMostSpend(self):
        """ Este metodo devuelve el producto en el que mas dinero se ha gastado en la compra """
        # Sacamos el producto con mayor precio pasandole como patametro key price
        expensive = max(self.products, key=attrgetter('price'))
        return expensive

    def addProduct(self, p):
        """ Agrega al objeto Purchase un nuevo Product """
        self.products.append(p)

    def __str__(self):
        return f'code : {self.code} Date: {self.date} total items : {self.total_product} total price : {self.total_price}'

    def setTotalPrice(self):
        total = 0.0
        for product in self.products:
            total += float(product.price)
        total = round(total, 2)
        return total
