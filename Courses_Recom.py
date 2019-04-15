from flask import Flask, render_template, request
from sklearn.externals import joblib
from scipy.sparse import load_npz
import pandas as pd
import json
import psycopg2
from Model_Recommender import recommentation

try:
    conn = psycopg2.connect(dbname='Confama', user='postgres', host='cognos', password='Pragma2017+', port=22817)
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()
cur.execute('SELECT * FROM usuario_segmento')
data = cur.fetchall()

DATA = pd.DataFrame(data, columns=['Categoria', 'Email', 'Plan_de_Estudios', 'Unidad_Organizativa', 'cod_Email', 'Cod_Plan_de_Estudios', 'Cod_Unidad'])
cur.close()
conn.close()

MODEL = joblib.load('model_implict.pkl')
USER_COURSE = load_npz('usuario_cursos.npz')

app = Flask(__name__)

@app.route('/personas', methods=['GET','POST'])
def personas(email='-h-german@hotmail.com'):
    if request.method == 'POST':
        if request.form['email']:
            email = request.form['email']
        else:
            email = "-h-german@hotmail.com"

        email = email.lower()
        cursos = recommentation(MODEL, USER_COURSE, DATA, user= '{}'.format(email)).recommendCourses()
    else:
        email = email.lower()
        cursos = recommentation(MODEL, USER_COURSE, DATA, user= '{}'.format(email)).recommendCourses()
    d = cursos.to_json(orient='records')
    return render_template('personas.html',courses= json.loads(d))

@app.route('/grupos', methods=['GET','POST'])
def grupos():
    unidad = ['Artes']
    if request.method == 'POST':
        unidad = request.form.getlist('uo')

    DT = DATA[DATA.Unidad_Organizativa == '{}'.format(unidad[0])]
    cursos = recommentation(MODEL, USER_COURSE, data=DATA, data_=DT).recommendUser()   
    d = cursos.to_json(orient='records')
    usuarios = DT.Email
    uslength = len(usuarios)
    u = usuarios.to_json(orient='records')
    return render_template('grupos.html',usuarios= json.loads(u), courses= json.loads(d), uslength= uslength)

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug= True, port= 8000)