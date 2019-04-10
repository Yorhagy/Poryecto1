import pandas as pd

def puntaje(Score):
    frecuencia = []
    for j in Score:
        if j < 0.33:
            frecuencia.append('Bajo')
        elif j >= 0.33 and j < 0.66:
            frecuencia.append('Medio')
        else:
            frecuencia.append('Alto')
    return frecuencia

def PrintRecommender(data, recommendation):
    courses = []
    scores = []
    for course in recommendation:
        idx, score = course
        courses.append(data.Plan_de_Estudios.loc[data.Cod_Plan_de_Estudios == idx].iloc[0])
        scores.append(score)
    r = pd.DataFrame({'Curso': courses, 'Score': scores})
    r['Clasificación'] = puntaje(r.Score.values)
    return r

class recommentation:
    def __init__(self, model, user_course, data, user=None):
        self.data = data
        self.user = user
        self.model = model
        self.user_course = user_course

    def recommendCourses(self):
        id_ = self.data[self.data.Email == self.user].iloc[0, 4]
        recommendation = self.model.recommend(id_, self.user_course)
        return PrintRecommender(self.data, recommendation)

    def recommendUser(self):
        id_ = self.data.cod_Email[0]
        recommendation = self.model.recommend(id_, self.user_course)
        return PrintRecommender(self.data, recommendation)