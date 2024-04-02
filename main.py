from flask import Flask, render_template, request, send_file
from flask import Response
from flask_cors import CORS, cross_origin
from datetime import datetime
from sklearn.externals import joblib
import os


from datetime import datetime
import pandas as pd
from sklearn.externals import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
#dashboard.bind(app)
CORS(app)

@app.route("/")
@cross_origin()
def home():
    return render_template('homepage.html')


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/index')
def index():
    return render_template('index.html')



