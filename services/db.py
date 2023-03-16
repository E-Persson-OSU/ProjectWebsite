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

def init_db():
    db = get_db()
    create_table()
    db.commit()
    db.close()

def create_table():
    conn = sqlite3.connect('database.db')  # Replace "your_database.db" with your actual database name
    c = conn.cursor()

    # Execute the SQLite3 command to create the table
    c.execute('DROP TABLE IF EXISTS recents;')

    c.execute('''
        CREATE TABLE recents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            bookdate TEXT,
            imglink TEXT
        );
    ''')

    conn.commit()
    conn.close()

def addrecentdb(recents):
    db = get_db()
    cursor = db.cursor()
    for recent in recents:
        cursor.execute("INSERT INTO recents VALUES (?,?,?,?)", (None, recent['name'], recent['book_date'], recent['mugshot']))
    db.commit()
    db.close()

def getrecentdb():
    records = []
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM recents")
    rows = cursor.fetchall()
    for row in rows:
        record = {
            "name":"",
            "book_date": "",
            "mugshot": ""
        }
        print(row[1])
        record["name"] = row[1]
        print(row[2])
        record["book_date"] = row[2]
        print(row[3])
        record["mugshot"] = row[3]
        records.append(record)
    print(len(records))
    # data = {"records": records}
    return records
