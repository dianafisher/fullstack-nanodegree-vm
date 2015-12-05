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
	name TEXT, 
	id SERIAL PRIMARY KEY
	);

-- Create the matches table. Each match references two players from the players table.
-- player1_score and player2_score columns hold the score for player 1 and player 2, respectively.  
-- A win earns a player 3 points, a tie earns each player 1 point.  A loss results in a score of 0 points.
CREATE TABLE matches (	
	player_id INTEGER REFERENCES players (id), 
	opponent_id INTEGER REFERENCES players (id),
	player_score INTEGER,
	CONSTRAINT match_id PRIMARY KEY (player_id, opponent_id)		
	);

-- Create a view to hold the standings.

CREATE VIEW match_count_view AS SELECT players.id, count(matches.player_id) AS matches FROM players LEFT JOIN matches on players.id = matches.player_id GROUP BY players.id ORDER BY matches;
CREATE VIEW match_wins_view AS SELECT players.id, count(matches.player_id) AS wins FROM players LEFT JOIN matches ON players.id = matches.player_id AND matches.player_score = 3 GROUP BY players.id ORDER BY wins DESC;
CREATE VIEW player_standings_view AS SELECT players.id, players.name, match_wins_view.wins, match_count_view.matches FROM players, match_wins_view, match_count_view WHERE players.id = match_count_view.id AND players.id = match_wins_view.id ORDER BY match_wins_view.wins DESC;

