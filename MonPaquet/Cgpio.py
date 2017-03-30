

class Cgpio(object):
    """definition de la classe gpio qui contiendra le nom, type, id et valeur possible de chaque gpio"""

    # def __init__(self, id=100, nom="gpio_0", range=[],value=0):
    def __init__(self):
        """constructeur"""

    def setValue(self, value):
        if value in self.range:
            self.value = value
        else:
            print(self.nom + " ne peut pas prendre la valeur : " + value)
            self.value = "0"