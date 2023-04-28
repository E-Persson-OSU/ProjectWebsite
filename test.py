import services.govdeals as gd
import json
import services.utils as ut
import services.db as db
from services.base_logger import logger


def test_max_rows():
    max_rows = gd.get_max_rows(28)
    print(max_rows)
    return max_rows


def test_get_rows(mr):
    rows = gd.get_rows(28, mr)
    print(len(rows))
    return rows


def test_trgc(rows):
    contents = gd.take_rows_give_contents(rows)
    print(len(contents))
    print(contents[0])


def create_json_dump(dump):
    with open("static\\bin\\test_rows.json", "w") as f:
        json.dump(dump, fp=f)
    print("Flush!")


def test_database():
    import sqlite3

    # Open a connection to the database
    conn = sqlite3.connect("database.db")

    # Create a cursor object
    c = conn.cursor()

    # Insert some test values in

    # Select the test values from the GovDeals table and print them to the console
    c.execute("SELECT * FROM GovDeals")
    rows = c.fetchall()
    for row in rows:
        print(row)

    # Close the connection to the database
    conn.close()


def test_init_db():
    import sqlite3

    # Connect to the database
    conn = sqlite3.connect("database.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the DROP TABLE command
    cursor.execute("DROP TABLE IF EXISTS GovDeals")

    # Execute the CREATE TABLE command
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS GovDeals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category INTEGER,
                    description TEXT,
                    location TEXT,
                    auction_close INTEGER,
                    current_bid TEXT,
                    info_link TEXT,
                    photo_link TEXT
                )"""
    )

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == "__main__":
    db.init_db()
    rows = gd.gather_listings()
    db.update_listings(rows)
    test_database()
    # l = []
    # db.init_db(l)
    # ut.update_govdeals()
