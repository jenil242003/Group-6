
import numpy as np
import flask
import pathlib
import sqlite3
import pickle
from flask import Flask, render_template, request

app=Flask(__name__)

base_path = pathlib.Path(r'C:\Python\Setup\.venv\FinalModels')
db_name = "model1.db"

db_path = pathlib.Path(r'C:\Python\Setup\.venv\FinalModels\Model2\Database\model1.db')


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')
    
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    loaded_model = pickle.load(open(r"C:\Python\Setup\.venv\FinalModels\Model2\SavedModel\model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/data")
def data():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM adult_data")
    data = cur.fetchall()
    conn.close()
    return render_template("data.html", data=data)

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        
        if int(result)==1:
            prediction='Income more than 50K'
        else:
            prediction='Income less that 50K'
            
        return render_template("result.html",prediction=prediction)

if __name__ == "__main__":
	app.run(debug=True)