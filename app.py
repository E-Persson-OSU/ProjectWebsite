from flask import Flask, render_template, request
import services.jailbase as jb
import services.db as db
import services.govdeals as gd
import random
from worker import conn
from rq import Queue
import services.utils as ut

q = Queue(connection=conn)

"""global variables"""
app = Flask(__name__)


def create_app():
    source_ids = []
    """
    add these back when I figure out a way to make it faster. Threading?
    source_ids = jb.getsourceids()
    
    """
    db.init_db(source_ids)
    app.run()


@app.route("/")
def index():
    results = q.enqueue(ut.background_updates())
    return render_template("index.html")


@app.route("/jailbase")
def jailbase():
    # records = jb.getrecent(db.getrandomsourceid()) Get this working eventually
    randomsource = random.choice(db.getsourceids())
    records = jb.getrecent(randomsource["source_id"])
    return render_template("jailbase.html", records=records["records"])


"""open page only after clicking search button, otherwise default values will be used"""


@app.route("/jailbase/search/", methods=["POST", "GET"])
def jailbasesearch():
    if request.method == "POST":
        print("JBSEARCH POST")
        form_data = request.args.get("state")
        print(form_data)
        source_ids = []
        l_name = request.args.get("lname")
        f_name = request.args.get("fname")
        try:
            source_ids = db.get_idsforstate(form_data)
            records = jb.searchjailbase(source_ids, l_name, f_name)
        except Exception as e:
            print(f"Error: {e}")
            records = []
        return render_template("jailbase.html", records=records)
    else:
        print("JBSEARCH GET")
        return app.redirect("/jailbase")


@app.route("/govdeals/")
def govdeals():
    return app.redirect("/govdeals/1")


@app.route("/govdeals/<pagenum>", methods=["POST", "GET"])
def govdealspage(pagenum=1):
    data = gd.load_json_dump()
    items = []
    for l in data:
        for row in l:
            items.append(row)
    return render_template("govdeals.html", items=PageResult(items, page=int(pagenum)))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(500)
def internalservererror():
    return "page not found"


class PageResult:
    def __init__(self, data, page=1, number=10):
        self.__dict__ = dict(zip(["data", "page", "number"], [data, page, number]))
        self.full_listing = [
            self.data[i : i + number] for i in range(0, len(self.data), number)
        ]

    def __iter__(self):
        for i in self.full_listing[self.page - 1]:
            yield i

    def __repr__(self):  # used for page linking
        return "/govdeals/{}".format(self.page + 1)  # view the next page


if __name__ == "__main__":
    create_app()
