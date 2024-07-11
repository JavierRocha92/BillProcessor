# Creamos la clase producto para crear objetos de este tipo
class Product(object):
    def __init__(self,purchase_code = None,  ud= None, name = None, weight=None, ud_price=None, price=None):
        """ Este es el contrictor del objeto Product """
        self.purchase_code = purchase_code
        self.ud = ud
        self.name = name
        self.weight = weight
        self.ud_price = ud_price
        self.price = price

    def __str__(self):
        return f'ud : {self.ud} name: {self.name} weight: {self.weight} precio ud: {self.ud_price}  price: {self.price} '

        # Getter y Setter para 'ud'

    @property
    def ud(self):
        return self._ud

    @ud.setter
    def ud(self, value):
        self._ud = value

    # Getter y Setter para 'name'
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Getter y Setter para 'weight'
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    # Getter y Setter para 'udprice'
    @property
    def udprice(self):
        return self._udprice

    @udprice.setter
    def udprice(self, value):
        self._udprice = value

    # Getter y Setter para 'price'
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
    def is_weigth(self, text_list : list):
        return True if 'kg' in text_list else False

    def to_list(self):
        return [self.purchase_code, self.ud, self.name, self.weight, self.ud_price, self.price]

""" p = Product(1,'hola',1.22,1.33)
print(p) """