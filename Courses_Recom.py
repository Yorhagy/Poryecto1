from flask import Flask, render_template, request
from sklearn.externals import joblib
from scipy.sparse import load_npz
import pandas as pd
import json
import psycopg2
from Model_Recommender import recommentation

#try:
    #conn = psycopg2.connect(dbname='Confama', user='postgres', host='cognos', password='Pragma2017+', port=22817)
    #conn.set_client_encoding('UTF8')
#except:
    #print ("I am unable to connect to the database")

#cur = conn.cursor()
#cur.execute('SELECT * FROM usuario_segmento LIMIT 10')
#rows = cur.fetchall()
#print(rows)

#cur.close()
#conn.close()


DATA = pd.read_csv('Comfama.csv')
MODEL = joblib.load('model_implict.pkl')
USER_COURSE = load_npz('usuario_cursos.npz')

app = Flask(__name__)

@app.route('/email', methods=['GET','POST'])
@app.route('/')
def index(email='-h-german@hotmail.com'):

    if request.method == 'POST':
        if request.form['email']:
            email = request.form['email']
        else:
            email = "david.botero@pragma.com.co"

        email = email.lower()
        cursos = recommentation(MODEL, USER_COURSE, DATA, user= '{}'.format(email)).recommendCourses()
    else:
        email = email.lower()
        cursos = recommentation(MODEL, USER_COURSE, DATA, user= '{}'.format(email)).recommendCourses()
    
    d = cursos.to_json(orient='records')
    return render_template('index.html',courses= json.loads(d))

@app.route('/filtros', methods=['GET','POST'])
def filtros():
    unidad = ['Programas de Bibliotecas']

    if request.method == 'POST':
        unidad = request.form.getlist('uo')
        print(unidad)
    
    DT = DATA[DATA.Unidad_Organizativa == '{}'.format(unidad[0])]
    usuarios = DT.Email[:10]
    cursos = recommentation(MODEL, USER_COURSE, DATA, user='-h-german@hotmail.com').recommendUser()   
    d = cursos.to_json(orient='records')
    u = usuarios.to_json(orient='records')
    return render_template('filtros.html',usuarios= json.loads(u), courses= json.loads(d))
       

if __name__ == "__main__":
    app.run(debug= True, port= 8000)