DROP TABLE IF EXISTS GovDeals;

CREATE TABLE IF NOT EXISTS GovDeals (
                listingid INTEGER PRIMARY KEY,
                acctid INTEGER,
                itemid INTEGER,
                category INTEGER,
                description TEXT,
                location TEXT,
                auction_close INTEGER,
                current_bid TEXT,
                info_link TEXT,
                photo_link TEXT
);

CREATE TABLE IF NOT EXISTS source_ids  (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 city TEXT,
                 name TEXT,
                 state_full TEXT,
                 address1 TEXT,
                 source_url TEXT,
                 county TEXT,
                 phone TEXT,
                 state TEXT,
                 source_id TEXT,
                 zip_code TEXT,
                 email TEXT,
                 has_mugshots BOOLEAN);