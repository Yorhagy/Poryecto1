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
#cur.close()
#conn.close()

MODEL = joblib.load('model_implict.pkl')
USER_COURSE = load_npz('usuario_cursos.npz')

def contador(cursos):
    alta =len(cursos[cursos.Afinidad == 'Alta'])
    Media =len(cursos[cursos.Afinidad == 'Media'])
    Baja = len(cursos[cursos.Afinidad == 'Baja'])
    return [alta, Media, Baja]

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
    return render_template('personas.html',courses= json.loads(d), afilength=contador(cursos))

@app.route('/grupos', methods=['GET','POST'])
def grupos():
    unidad = ['Artes']
    if request.method == 'POST':
        unidad = request.form.getlist('uo')

    unit = ['Administración, mercadeo y finanzas', 'Arte Manual', 'Artes', 'Desarrollo Humano',
            'Formación Físico Deportiva', 'Gastronomía', 'Idiomas', 'Programas Recreativos',
            'Programas de Bibliotecas', 'Tecnología y arte audiovisual digital']

    idi = '0'
    ff = '0'
    a = '0'
    g = '0'
    ad = '0'
    dh = '0'
    pr = '0'
    taa = '0'
    am = '0'
    pdb = '0'
    for i in unidad:
        if i in unit:
            if i == 'Administración, mercadeo y finanzas':
                ad = '1'
            if i == 'Arte Manual':
                am = '1'
            if i == 'Artes':
                a = '1'
            if i == 'Tecnología y arte audiovisual digital':
                taa = '1'
            if i == 'Desarrollo Humano':
                dh = '1'
            if i == 'Formación Físico Deportiva':
                ff = '1'
            if i == 'Gastronomía':
                g = '1'
            if i == 'Programas Recreativos':
                pr = '1'
            if i == 'Idiomas':
                idi = '1'
            if i == 'Programas de Bibliotecas':
                pdb = '1'

    st = 'SELECT email FROM users_for_unit where idiomas=' + idi + ' and formacion_fisico_deportiva='+ff+ ' and artes='+a+' and gastronomia='+g+' and administracion_mercade_finanzas='+ad+' and desarrollo_humano='+dh+' and programas_recreativos='+pr+' and tecnologia_arte_audiovisual_digital='+taa+' and arte_manual='+am+' and programas_debibliotecas='+pdb

    cur.execute(st)
    data1 = cur.fetchall()

    #cur.close()
    #conn.close()


    DT = pd.DataFrame(data1, columns=['Email'])


    #DT = DATA[DATA.Unidad_Organizativa == '{}'.format(unidad[0])]
    cursos = recommentation(MODEL, USER_COURSE, data=DATA, data_=DT).recommendUser()   
    d = cursos.to_json(orient='records')
    usuarios = DT.Email
    uslength = len(usuarios)
    u = usuarios.to_json(orient='records')
    return render_template('grupos.html',usuarios= json.loads(u), courses= json.loads(d), uslength= uslength, afilength=contador(cursos))

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug= True, port= 8000)