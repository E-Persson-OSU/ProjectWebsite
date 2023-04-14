from flask import Flask, render_template, request
import services.jailbase as jb
import services.db as db
import random



"""global variables"""
app = Flask(__name__)

def create_app():
    """
    add these back when I figure out a way to make it faster. Threading?
    source_ids = jb.getsourceids()
    db.init_db(source_ids)
    """
    app.run()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jailbase')
def jailbase():
    #records = jb.getrecent(db.getrandomsourceid()) Get this working eventually
    randomsource = random.choice(db.getsourceids())
    records = jb.getrecent(randomsource['source_id'])
    return render_template('jailbase.html', records=records['records'])

"""open page only after clicking search button, otherwise default values will be used"""
@app.route('/jailbase/search/', methods = ['POST', 'GET'])
def jailbasesearch():
    if request.method == 'GET':
        print('JBSEARCH GET')
        form_data = request.args.get('state')
        print(form_data)
        state = request.args.get('state')
        l_name = request.args.get('lname')
        f_name = request.args.get('fname')
        source_ids = db.get_idsforstate(state)
        records = jb.searchjailbase(source_ids, l_name, f_name)
        return render_template('jailbase.html', records=records)
    if request.method == 'POST':
        print('JBSEARCH POST')


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