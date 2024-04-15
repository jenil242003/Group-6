import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import sqlite3
import pandas as pd

conn = sqlite3.connect('iris.db')

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("C:\Python\Setup\.venv\FinalModels\Model1\model.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route('/about')
def about():
    return render_template('about.html')

@flask_app.route("/predict", methods = ["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    return render_template("index.html", prediction_text = "The flower species is {}".format(prediction))

@flask_app.route('/data')
def display_data():
   
    conn = sqlite3.connect('C:\Python\Setup\.venv\FinalModels\Model1\iris_database.db')
    c = conn.cursor()
   
    c.execute('SELECT * FROM iris_processed')
    data = c.fetchall()
  
    conn.close()
   
    return render_template('data.html', data=data)
    
if __name__ == "__main__":
    flask_app.run(debug=True)