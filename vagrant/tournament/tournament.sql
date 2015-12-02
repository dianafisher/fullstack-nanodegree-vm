-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database "tournament" and connect to that database before creating tables
\c vagrant
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
-- Connect to the tournament database
\c tournament
-- Create the Players table.
CREATE TABLE players (name TEXT, id SERIAL PRIMARY KEY);
-- Create the Matches table.
CREATE TABLE matches (player1_id INTEGER REFERENCES players (id), player2_id INTEGER REFERENCES players (id), id SERIAL PRIMARY KEY);
