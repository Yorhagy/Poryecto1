from implicit.als import AlternatingLeastSquares
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix

class DbFilter: 
    def __init__(self, data, categoria=None, unidad=None, genero=None, clas_Edad=None):
        self.categoria = categoria
        self.unidad = unidad
        self.genero = genero
        self.Edad = clas_Edad
        self.data = data
        
        if self.genero != None:
            self.data = self.data[self.data.genero == self.genero]
        if self.categoria != None:
            self.data = self.data[self.data.categoria_del_estudiante == self.categoria]
        if self.Edad != None:
            self.data = self.data[self.data.Edad == self.Edad]

    def filter_(self):
        if self.unidad != None:
            list_U = self.unidad 
            if len(list_U) == 1:
                self.data = self.data[self.data[''.join(list_U)] == 1]
            else:
                for u in list_U: 
                    self.data = self.data[self.data[u] == 1]            
            return self.data[['email', 'Vector_Plan_De_Estudios']]
        else:
            return self.data[['email', 'Vector_Plan_De_Estudios']]
        
class MatrixTransformer:
    def __init__(self, data):
        self.data = data
        
    def matrix(self):
        LISTCOURSES = [' '.join(i.split()) for i in list(self.data.Vector_Plan_De_Estudios)]

        VECTORCOURSES = ['act_acuáticas', 'act_recreativas', 'administración', 'ambiental', 
                         'animación_lectura', 'artes_audiovisuales_digital', 'artes_marciales', 
                         'artes_plásticas', 'baile_danza', 'bisutería', 'ciencias_computación', 
                         'competencias_empresariales', 'contabilidad_costos', 'dep_balón',
                         'dep_raqueta', 'dep_ruedas', 'deporte_familiar', 'dim_laboral',
                         'dim_personal', 'dim_social', 'elab_adornos', 'empleabilidad',
                         'emprendimiento', 'form_física', 'gimnasia', 'inglés_comp',
                         'inglés_niveles', 'logística_empresarial', 'mercadeo_ventas', 
                         'modistería', 'música', 'prep_bebidas_alimentos', 'presentación_personal', 
                         'protección_alimentos', 'puntadas_ganchillo', 'seg_servicios_generales', 
                         'supervacaciones', 'teatro', 'tec_alternativas']
        
        MATRIXPOINTS = []
        k = 0

        for courses in LISTCOURSES:
            for j in courses.split():
                if j in VECTORCOURSES:
                    MATRIXPOINTS.append([self.data.email[k], j])
            k+= 1
        
        self.data_ = pd.DataFrame(MATRIXPOINTS, columns=['user', 'course'])
        self.data_['user'] = self.data_['user'].astype('category').cat.codes.copy()
        self.data_['course'] = self.data_['course'].astype('category').cat.codes.copy()

        self.course_user = coo_matrix((np.ones(self.data_.shape[0]),
                                       (self.data_['course'], self.data_['user'])))
        
        self.list_email = list(self.data.email)
        self.list_courses = VECTORCOURSES
        return self
        
class AlS_implicit:
    def __init__(self, data):
        self.data = data.course_user
        
    def models(self):
        self.model = AlternatingLeastSquares(factors=25, regularization=100, iterations=40)
        self.model.fit(self.data * 10, show_progress=False)
        return self
                