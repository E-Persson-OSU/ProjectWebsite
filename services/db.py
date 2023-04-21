import sqlite3
from pathlib import Path
import logging

"""
global variables
"""
DB_PATH = Path("database.db")
SCHEMA_PATH = Path("static/db/") / "schema.sql"
LOGGING_PATH = Path("services/logs/") / "db.log"

logging.basicConfig(
    filename=LOGGING_PATH,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_db():
    return sqlite3.connect(DB_PATH)


# takes a two letter code and returns a list of source_ids that match that code
def get_ids_for_state(state_code="OH"):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT source_id FROM source_ids WHERE state = ?", (state_code,)
        )
        rows = cursor.fetchall()
        return rows


def get_source_ids():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT source_id FROM source_ids")
        rows = cursor.fetchall()
        return rows


def add_recent_db(recents):
    with get_db() as conn:
        cursor = conn.cursor()
        for recent in recents:
            cursor.execute(
                "INSERT INTO recents (id, name, book_date, mugshot) VALUES (?,?,?,?)",
                (None, recent["name"], recent["book_date"], recent["mugshot"]),
            )
        conn.commit()


def get_recent_db():
    records = []
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recents")
        rows = cursor.fetchall()
        for row in rows:
            record = {"name": row[1], "book_date": row[2], "mugshot": row[3]}
            records.append(record)
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
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SCHEMA_PATH) as f:
            cursor.executescript(f.read())
        conn.commit()


def init_source_ids(source_ids):
    with get_db() as conn:
        cursor = conn.cursor()
        for source_id in source_ids:
            logging.info(f"Adding {source_id['name']} to database")
            cursor.execute(
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
            conn.commit()


"""
------------------------------------------

            Internal Methods

------------------------------------------
"""
