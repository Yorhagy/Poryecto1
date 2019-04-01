import pandas as pd
from filtro_data import DbFilter, AlS_implicit, MatrixTransformer
from Model_Recommendation import recommentation
import os
import json

#class ConsultaBaseDatos:
 #   def __init__(self, data, )

#dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/db_comfama.csv' 

data = pd.read_csv('db_comfama.csv', nrows=10)

data_ = MatrixTransformer(data).matrix()
model = AlS_implicit(data_).models()       

cursos = recommentation(model, data_, userId='-h-german@hotmail.com').recommendCourses()

courses = cursos.to_json()
d = json.loads(courses)
for user in d:
    print(user)
#r_cursos = recommentation(model, data_).relatedItems('dim_personal')

#data2 = DbFilter(data, unidad=['Arte'], categoria='A', genero='Masculino').filter_()
#r_cursos_2 = recommentation(model, data_, userId='-h-german@hotmail.com').relatedUser(data2)
