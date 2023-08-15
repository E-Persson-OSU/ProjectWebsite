"""Module that runs the entire website python 3.10.8"""
import random
from flask import Flask, render_template, request
from services import jailbase as jb
from services import db
from services import govdeals as gd
from services import utils as ut
# from worker import conn
# from rq import Queue
# q = Queue(connection=conn)

# global variables
app = Flask(__name__)


def create_app() -> None:
    """creates the app and runs it"""
    source_ids = []
    # add these back when I figure out a way to make it faster. Threading?
    # source_ids = jb.getsourceids()

    db.init_db(source_ids)
    app.run()


@app.route("/")
def index():
    """opens main page of the website"""
    #    results = q.enqueue(ut.background_updates())
    ut.background_updates()
    return render_template("index.html")


@app.route("/jailbase")
def jailbase():
    """page for jail database searches"""
    # records = jb.getrecent(db.getrandomsourceid()) Get this working eventually
    randomsource = random.choice(db.get_source_ids())
    records = jb.getrecent(randomsource[0])
    return render_template("jailbase.html", records=records["records"])




@app.route("/jailbase/search/", methods=["POST", "GET"])
def jailbasesearch():
    """open page only after clicking search button, otherwise default values will be used"""
    if request.method == "POST":
        print("JBSEARCH POST")
        form_data = request.args.get("state")
        print(form_data)
        source_ids = []
        l_name = request.args.get("lname")
        f_name = request.args.get("fname")
        records = []
        source_ids = db.get_ids_for_state(form_data)
        records = jb.searchjailbase(source_ids, l_name, f_name)
        return render_template("jailbase.html", records=records)
    print("JBSEARCH GET")
    return app.redirect("/jailbase")


@app.route("/govdeals/")
def govdeals():
    """page for scraping govdeals site"""
    return app.redirect("/govdeals/1")


@app.route("/govdeals/<pagenum>", methods=["POST", "GET"])
def govdealspage(pagenum=1):
    """opens specific page of govdeals"""
    return render_template(
        "govdeals.html", items=PageResult(data=gd.db_all_listings(), page=int(pagenum))
    )


@app.route("/about")
def about():
    """my about page"""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """my contact page"""
    return render_template("contact.html")


@app.errorhandler(500)
def internalservererror():
    """error page"""
    return "page not found"


# Passing this a GovDeals object as <data> should work
class PageResult:
    """helper class for opening a specific page"""

    data = None
    def __init__(self, data, page=1, number=10):
        self.__dict__ = dict(zip(["data", "page", "number"], [data, page, number]))
        self.full_listing = [
            self.data.listings[i : i + number] for i in range(0, len(self.data), number)
        ]

    def __iter__(self):
        # pylint: disable=no-member
        for i in self.full_listing[self.page - 1]:
            yield i

    def __repr__(self):  # used for page linking
        # pylint: disable=no-member
        return f"/govdeals/{self.page + 1}"  # view the next page


if __name__ == "__main__":
    create_app()
