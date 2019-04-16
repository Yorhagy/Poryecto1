import pandas as pd

def puntaje(Score):
    frecuencia = []
    for j in Score:
        if j < 0.33:
            frecuencia.append('Baja')
        elif j >= 0.33 and j < 0.66:
            frecuencia.append('Media')
        else:
            frecuencia.append('Alta')
    return frecuencia

def PrintRecommender(data, recommendation):
    courses = []
    scores = []
    for course in recommendation:
        idx, score = course
        courses.append(data.Plan_de_Estudios.loc[data.Cod_Plan_de_Estudios == idx].iloc[0])
        scores.append(score)
    r = pd.DataFrame({'Curso': courses, 'Score': scores})
    r['Afinidad'] = puntaje(r.Score.values)
    return r

class recommentation:
    def __init__(self, model, user_course, data, data_=None, user=None):
        self.data = data
        self.data_ = data_
        self.user = user
        self.model = model
        self.user_course = user_course

    def recommendCourses(self):
        id_ = self.data[self.data.Email == self.user].iloc[0, 4]
        recommendation = self.model.recommend(id_, self.user_course)
        return PrintRecommender(self.data, recommendation)

    def recommendUser(self):
        tr = self.data.merge(self.data_, on='Email' )
        id_ = tr.cod_Email.values[0]
        recommendation = self.model.recommend(id_, self.user_course)
        return PrintRecommender(self.data, recommendation)