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

-- Create the players table.
CREATE TABLE players (
	name TEXT,  -- the full player name
	id SERIAL PRIMARY KEY  -- give each player a unique id.
);

-- Create the matches table. Each match references two players from the players table - the winner of the match and the loser of the match.
CREATE TABLE matches (	
	winner_id INTEGER REFERENCES players (id),  -- winner_id has players.id as a foreign key.
	loser_id INTEGER REFERENCES players (id),   -- loser_id has players.id as a foreign key.	
	CHECK (winner_id <> loser_id), -- prevent having a player matched up with themselves.
	id SERIAL PRIMARY KEY  -- give each match a unique id.
);

-- Create a unique index to prevent rematches between players.
CREATE UNIQUE INDEX matches_unique_idx ON matches
	(greatest(winner_id, loser_id), least(winner_id, loser_id));

-- Create a view to hold the player standings.
CREATE VIEW player_standings_view AS select id, name, (SELECT count(*) FROM matches WHERE players.id = matches.winner_id) AS wins, (SELECT count(*) FROM matches WHERE players.id = matches.winner_id OR players.id = matches.loser_id) AS matches FROM players ORDER BY wins DESC;

-- Create views to assist with grouping players for matches.

-- Create view to select even numbered rows in the player_standings_view and hold them in a separate view.
CREATE VIEW even_rows_view AS SELECT id, name, wins FROM (SELECT id, name, wins, (row_number() OVER (ORDER BY wins DESC)) % 2 AS rn FROM player_standings_view) sub WHERE sub.rn = 0;
-- Create view to select odd numbered rows in the player_standings_view and hold them in a separate view.
CREATE VIEW odd_rows_view AS SELECT id, name, wins FROM (SELECT id, name, wins, (row_number() OVER (ORDER BY wins DESC)) % 2 AS rn FROM player_standings_view) sub WHERE sub.rn != 0;

CREATE VIEW eview AS SELECT id, name, num FROM (SELECT id, name, (row_number() OVER (ORDER BY wins DESC)) AS num FROM even_rows_view) sub;
CREATE VIEW oview AS SELECT id, name, num FROM (SELECT id, name, (row_number() OVER (ORDER BY wins DESC)) AS num FROM odd_rows_view) sub;