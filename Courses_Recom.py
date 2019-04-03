from flask import Flask, render_template, request
import os
from filtro_data import DbFilter, AlS_implicit, MatrixTransformer
from Model_Recommendation import recommentation
import pandas as pd
import json
import psycopg2


try:
    conn = psycopg2.connect(dbname='Confama', user='postgres', host='cognos', password='Pragma2017+', port=22817)
    conn.encoding
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()
cur.execute('SELECT * FROM usuario_segmento LIMIT 10')
rows = cur.fetchall()
print(rows)

cur.close()
conn.close()
#data = pd.read_csv('/home/yorhagy/Escritorio/Comfama_recommendation/db_comfama.csv')

app = Flask(__name__)

@app.route('/email', methods=['GET','POST'])
@app.route('/')
def index(correo='-h-german@hotmail.com'):

    data_ = MatrixTransformer(data).matrix()
    model = AlS_implicit(data_).models()
    if request.method == 'POST':
        if not request.form['email']:
            email = "david.botero@pragma.com.co"
        else:
            email = request.form['email']
        cursos = recommentation(model, data_, userId='{}'.format(email)).recommendCourses()
    else:
        #data_ = DbFilter(data).filter_()
        cursos = recommentation(model, data_, userId='{}'.format(correo)).recommendCourses()
    
    d = cursos.to_json(orient='records')
    return render_template('index.html',courses= json.loads(d))
    #return cursos.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug= True, port= 8000)