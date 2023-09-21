\c postgres

DROP DATABASE IF EXISTS spotify_db ;


CREATE DATABASE spotify_db;

-- CREATE TABLE Users (
--     username TEXT PRIMARY KEY,
--     password TEXT,
--     name TEXT,
--     email TEXT,
--     userPlaylistID INTEGER,
--     followers TEXT,
--     following TEXT,
--     avatar TEXT

-- );

-- CREATE TABLE Posts(
--     post_id INTEGER PRIMARY KEY,
--     likes INTEGER,
--     images TEXT,
--     username TEXT REFERENCES Users(username)
-- );

-- CREATE TABLE Playlists(
--     id SERIAL,
--     playlist_id TEXT PRIMARY KEY,
--     username TEXT REFERENCES Users(username),
--     image TEXT,
--     description TEXT
-- );


-- CREATE TABLE Followers(
--     username TEXT PRIMARY KEY REFERENCES Users(username)
-- );

-- CREATE TABLE User_Posts(
--     id SERIAL PRIMARY KEY,
--     username TEXT REFERENCES Users(username),
--     post_id INTEGER REFERENCES Posts(post_id)
    
-- );

-- CREATE TABLE Following (
--     username TEXT PRIMARY KEY REFERENCES Users(username)
-- );


