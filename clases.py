import pandas as pd

class DbFilter():
    def __init__(self, db, unidad, planEstudio):
        self.db = db
        self.unidad = unidad
        self. planEstudio = planEstudio

    def print_unidad(self):
        return self.unidad

    def print_planEstudio(self):
        return self.planEstudio

data = pd.read_csv('comfama_users1.csv', nrows=1000, usecols=('email', 'Vector_Unidad_Organizativa', 'Vector_Plan_De_Estudios'))




