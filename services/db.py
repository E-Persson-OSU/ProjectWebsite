import sqlite3
from pathlib import Path
from services.base_logger import logger

"""
global variables
"""
DB_PATH = Path("database.db")
SQL_PATH = Path("static/db/")
SCHEMA_PATH = Path("static/db/") / "schema.sql"


def get_db():
    return sqlite3.connect(DB_PATH)


# takes a two letter code and returns a list of source_ids that match that code
def get_ids_for_state(state_code="OH"):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        with open(SQL_PATH / "select_sourceidstate.sql") as file:
            cursor.execute(file.read(), (state_code,))
        rows = cursor.fetchall()
        return rows


def get_source_ids():
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SQL_PATH / "select_sourceid.sql") as file:
            cursor.execute(file.read())
        rows = cursor.fetchall()
        return rows


def add_recent_db(recents):
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SQL_PATH / "insert_recent.sql") as file:
            for recent in recents:
                cursor.execute(
                    file.read(),
                    (None, recent["name"], recent["book_date"], recent["mugshot"]),
                )
        conn.commit()


def get_recent_db():
    records = []
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SQL_PATH / "select_allrecent.sql") as file:
            cursor.execute(file.read())
        rows = cursor.fetchall()
        for row in rows:
            record = {"name": row[1], "book_date": row[2], "mugshot": row[3]}
            records.append(record)
        return records


# takes list of lists of dicts and adds them to database
def update_listings(govdeals):
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SQL_PATH / "insert_govdeals.sql") as file:
            for listing in govdeals:
                cursor.execute(
                    file.read(),
                    (
                        listing.listingid,
                        listing.acctid,
                        listing.itemid,
                        listing.category,
                        listing.description,
                        listing.location,
                        listing.auction_close,
                        listing.current_bid,
                        listing.info_link,
                        listing.photo_link,
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
        with open(SQL_PATH) as f:
            logger.info("Reading Schema")
            cursor.executescript(f.read())
        conn.commit()


def init_source_ids(source_ids):
    with get_db() as conn:
        cursor = conn.cursor()
        with open(SQL_PATH / "insert_sourceids.sql") as file:
            for source_id in source_ids:
                logger.info(f"Adding {source_id['name']} to database")
                cursor.execute(
                    file.read(),
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
