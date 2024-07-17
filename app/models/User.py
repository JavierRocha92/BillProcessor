class User:
    def __init__(self, email, password):
        """Constructor de la clase User"""
        self._email = email  # Atributo protegido por convención
        self._password = password  # Atributo protegido por convención

    # Getter para el atributo email
    def get_email(self):
        return self._email

    # Setter para el atributo email
    def set_email(self, new_email):
        self._email = new_email

    # Getter para el atributo password
    def get_password(self):
        return self._password

    # Setter para el atributo password
    def set_password(self, new_password):
        self._password = new_password

    # Método especial para representación de cadena (to string)
    def __str__(self):
        return f"User(email='{self._email}', password='{self._password}')"
    def to_list(self):
        return [self._email, self._password]


