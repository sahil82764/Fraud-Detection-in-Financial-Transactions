from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')