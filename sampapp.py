from flask import Flask, render_template, request
from fraudTransaction.logger import logging

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')