from flask import Flask, render_template

import services.jailbase as jb
import services.db as db
import os
import threading
import http.client as client
import time


"""global variables"""
app = Flask(__name__)

def create_app():
    """for waitress"""
    app.run()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jailbase')
def jailbase():
    records = jb.getrecent()
    return render_template('jailbase.html', records=records)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(500)
def internalservererror():
    return "page not found"

if __name__ == "__main__":
    app.run()