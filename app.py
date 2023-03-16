from flask import Flask, render_template
import services.jailbase as jb
import services.db as db
import http.client as client



"""global variables"""
app = Flask(__name__)

def create_app():
    db.init_db()
    jb.getrecent()
    app.run()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jailbase')
def jailbase():
    records = db.getrecentdb()
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
    create_app()