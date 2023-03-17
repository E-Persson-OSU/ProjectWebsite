from flask import Flask, render_template, request
import services.jailbase as jb
import services.db as db
import random



"""global variables"""
app = Flask(__name__)

def create_app():
    source_ids = jb.getsourceids()
    db.init_db(source_ids)
    app.run()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jailbase')
def jailbase():
    #records = jb.getrecent(db.getrandomsourceid()) Get this working eventually
    randomsource = random.choice(jb.getsourceids)
    records = jb.getrecent(randomsource['source_id'])
    return render_template('jailbase.html', records=records['records'])

"""open page only after clicking search button, otherwise default values will be used"""
@app.route('/jailbase/search')
def jailbasesearch():
    form_data = request.form
    print(form_data)
    state = 'OH'
    l_name = 'persson'
    f_name = 'erik'
    records = jb.searchjailbase(state, l_name, f_name)
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