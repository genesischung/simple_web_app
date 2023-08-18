DROP TABLE IF EXISTS auth;

CREATE TABLE IF NOT EXISTS test_table(
    id serial primary key);

CREATE TABLE IF NOT EXISTS auth(
    id serial PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL);