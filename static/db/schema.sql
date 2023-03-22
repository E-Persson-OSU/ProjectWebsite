DROP TABLE IF EXISTS source_ids;

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
                 has_mugshots BOOLEAN)