DROP TABLE IF EXISTS auth;
DROP TABLE IF EXISTS post;

CREATE TABLE auth (
    id serial PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);