import sqlite3
from pathlib import Path
from services.base_logger import logger

"""
global variables
"""
DB_PATH = Path("database.db")
SCHEMA_PATH = Path("static/db/") / "schema.sql"


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


# takes list of lists of dicts and adds them to database
def update_listings(rows):
    with get_db() as conn:
        cursor = conn.cursor()
        for row in rows:
            for d in row.all_listings():
                cursor.execute(
                    "INSERT INTO GovDeals (id, category, description, location, auction_close, current_bid, info_link, photo_link) VALUES(?,?,?,?,?,?,?,?)",
                    (
                        None,
                        row.category,
                        d["description"],
                        d["location"],
                        d["auction_close"],
                        d["current_bid"],
                        d["info_link"],
                        d["photo_link"],
                    ),
                )
        conn.commit()

    ...


"""
------------------------------------------

            Init Methods

------------------------------------------
"""


def init_db(source_ids=[]):
    logger.info("init_db")
    create_table()
    if len(source_ids) > 0:
        logger.info("Updating source IDs")
        init_source_ids(source_ids)
    else:
        logger.info("No changes to source IDs")


def create_table():
    logger.info("create_table")
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SCHEMA_PATH) as f:
            logger.info("Reading Schema")
            cursor.executescript(f.read())
        conn.commit()


def init_source_ids(source_ids):
    with get_db() as conn:
        cursor = conn.cursor()
        for source_id in source_ids:
            logger.info(f"Adding {source_id['name']} to database")
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
