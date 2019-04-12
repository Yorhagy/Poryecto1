import pandas as pd

class DbFilter():
    def __init__(self, data, unidad=None):
        self.data = data
        self.Email = data.Email
        self.unidad = unidad

    def filtro(self):
        user = list(set(self.Email.values))
        for i in user:
            d = self.data[self.Email == user]
            if len(d) == len(self.unidad):
                return d