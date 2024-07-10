# Creamos la clase producto para crear objetos de este tipo
class Product(object):
    def __init__(self, ud, name, weight=None, ud_price=None, price=None):
        """ Este es el contrictor del objeto Product """
        self.ud = ud
        self.name = name
        self.weight = weight
        self.ud_price = ud_price
        self.price = price

    def __str__(self):
        return f'ud : {self.ud} name: {self.name} weight: {self.weight} precio ud: {self.ud_price}  price: {self.price} '


""" p = Product(1,'hola',1.22,1.33)
print(p) """