from flask import Flask, request, render_template
import os
from filtro_data import DbFilter, AlS_implicit, MatrixTransformer
from Model_Recommendation import recommentation
import pandas as pd

#dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/db_comfama.csv'
data = pd.read_csv('/home/yorhagy/Escritorio/Comfama_recommendation/db_comfama.csv', nrows=10)

app = Flask(__name__)

@app.route('/')
def index():
    data_ = MatrixTransformer(data).matrix()
    model = AlS_implicit(data_).models()
    #data_ = DbFilter(data).filter_()
    cursos = recommentation(model, data_, userId='-h-german@hotmail.com').recommendCourses()
    return cursos.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug= True, port= 8000)