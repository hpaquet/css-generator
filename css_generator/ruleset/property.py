

class Property:
    """Class that represent a style property"""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def css(self):
        return f"{self.name}: {self.value};"

    def to_dict(self):
        pass