DROP TABLE IF EXISTS auth;
DROP TABLE IF EXISTS test_table;
DROP TABLE IF EXISTS info;
DROP TABLE IF EXISTS votes;

CREATE TABLE IF NOT EXISTS auth(
    id serial PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO auth(username, password)
VALUES
    ('admin', 'pbkdf2:sha256:260000$SmgTosRGiU5SgtKz$bb91019ab1b08d0f84c924b6a898bb7f15c835114e78dba9018a9cb7b6322e5a');

CREATE TABLE IF NOT EXISTS results(
    id serial PRIMARY KEY,
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    data JSON NOT NULL
);


CREATE TABLE IF NOT EXISTS pitstops(
    id serial PRIMARY KEY,
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    data JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS votes(
    id serial PRIMARY KEY,
    driver INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS info(
    id serial PRIMARY KEY,
    name TEXT NOT NULL,
    data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drivers(
    driverId TEXT PRIMARY KEY,
    givenName TEXT NOT NULL,
    familyName TEXT NOT NULL
);