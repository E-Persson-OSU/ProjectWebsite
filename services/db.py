import sqlite3
import os

"""global variables"""


def get_db():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db


"""
def addsourceid():
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO source_ids (city, name, state_full, address1, source_url, county, phone, state, source_id, zip_code, email, has_mugshots) \
              VALUES ('Menominee', 'Menominee Co Sheriff''s Dept', 'Michigan', '831 10th Ave', 'http://vinelink.com', 'Menominee County', '(906) 863-4441', 'MI', 'mi-mnsd', '49858', NULL, 1)")
"""


# takes a two letter code and returns a list of source_ids that match that code
def get_idsforstate(state_code="OH"):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT source_id FROM source_ids WHERE state = ?", (state_code,))
    rows = c.fetchall()

    return rows


def getsourceids():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT source_id FROM source_ids")
    rows = c.fetchall()
    db.close()
    return rows


def addrecentdb(recents):
    db = get_db()
    cursor = db.cursor()
    for recent in recents:
        cursor.execute(
            "INSERT INTO recents VALUES (?,?,?,?)",
            (None, recent["name"], recent["book_date"], recent["mugshot"]),
        )
    db.commit()
    db.close()


def getrecentdb():
    records = []
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM recents")
    rows = cursor.fetchall()
    for row in rows:
        record = {"name": "", "book_date": "", "mugshot": ""}
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


"""
------------------------------------------

            Init Methods

------------------------------------------
"""


def init_db(source_ids=[]):
    create_table()
    if len(source_ids) > 0:
        init_source_ids(source_ids)


def create_table():
    db = get_db()
    c = db.cursor()
    with open("static\db\schema.sql") as f:
        c.executescript(f.read())
    db.commit()
    db.close()


def init_source_ids(source_ids):
    db = get_db()
    c = db.cursor()
    for source_id in source_ids:
        print("Adding {} to database".format(source_id["name"]))
        c.execute(
            "INSERT INTO source_ids (id, city, name, state_full, address1, source_url, county, phone, state, source_id, zip_code, email, has_mugshots) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                None,
                source_id["city"],
                source_id["name"],
                source_id["state_full"],
                source_id["address1"],
                source_id["source_url"],
                source_id["county"],
                source_id["phone"],
                source_id["state"],
                source_id["source_id"],
                source_id["zip_code"],
                source_id["email"],
                source_id["has_mugshots"],
            ),
        )
        db.commit()
    db.close()


"""
------------------------------------------

            Internal Methods

------------------------------------------
"""
