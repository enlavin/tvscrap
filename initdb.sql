CREATE TABLE shows (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    regexp_filter VARCHAR,
    min_size FLOAT,
    max_size FLOAT
);

CREATE TABLE episodes (
    id INTEGER PRIMARY KEY,
    show_id INTEGER,
    name VARCHAR,
    filename VARCHAR,
    torrent VARCHAR,
    size INTEGER,
    queued BOOLEAN,
    downloaded BOOLEAN,
    url VARCHAR
);

CREATE TABLE config (
    varname VARCHAR PRIMARY KEY,
    value VARCHAR
);

