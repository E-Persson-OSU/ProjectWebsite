import sqlite3

import click
from flask import current_app
import os

"""global variables"""
rel_dir = "/static/db/schema.sql"


def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row

    return db

"""def init_db(absolute_dir):
    db = get_db()
    abs_file_path = os.path.join(absolute_dir,rel_dir)
    print(abs_file_path)
    with current_app.open_resource(rel_dir) as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()
    db.close()"""





def addrecentdb(recents):
    db = get_db()
    cursor = db.cursor()
    for recent in recents:
        cursor.execute("INSERT INTO recents VALUES (?,?,?,?)", (None, recent['name'], recent['book_date'], recent['mugshot']))
    db.commit()

def getrecentdb():
    records = {
        "name":"",
        "book_date": "",
        "mugshot": ""
    }
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM recents")
    rows = cursor.fetchall()
    for row in rows():
        records["name"] = row[1]
        records["book_date"] = row[2]
        records["mugshot"] = row[3]
    data = {"records": records}
    return data
    


    

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')