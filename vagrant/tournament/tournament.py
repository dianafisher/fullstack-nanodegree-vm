#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Open the database connection.
    conn = connect()
    
    # Obtain a cursor.
    c = conn.cursor()

    # Execute the SQL query to clear the matches table.
    c.execute("DELETE FROM matches")

    # Commit.
    conn.commit()

    # Close the database connection.
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    # Open the database connection.
    conn = connect()
    
    # Obtain a cursor.
    c = conn.cursor()

    # Execute the SQL query to clear the players table.
    c.execute("DELETE FROM players")

    # Commit.
    conn.commit()

    # Close the database connection.
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # Open the database connection.
    conn = connect()
    
    # Obtain a cursor.
    c = conn.cursor()

    # Execute the SQL query to count the number of rows in the players table.
    c.execute("SELECT count(*) FROM players")

    # The count will be the first column of the first and only row.
    result = c.fetchall()[0][0]

    # Commit.
    conn.commit()

    # Close the database connection.
    conn.close()

    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Open the database connection.
    conn = connect()
    
    # Obtain a cursor.
    c = conn.cursor()

    # Execute the SQL query to insert the player name into the players table.
    c.execute("INSERT INTO players VALUES (%s)", (name,))

    # Commit.
    conn.commit()

    # Close the database connection.
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 # Open the database connection.
    conn = connect()
    
    # Obtain a cursor.
    c = conn.cursor()

    # Execute the SQL query to insert the winner and loser player ids into the matches table.

    # c.execute("INSERT INTO matches VALUES (%s,%s) RETURNING id", (winner,loser,))
    # query = "INSERT INTO matches VALUES (%s,%s) RETURNING id"
    # c.execute(query, (winner, loser,))
    # match_id = c.fetchone()[0]
    # print 'just added match with id ', match_id

    c.execute("INSERT INTO matches VALUES (%s,%s,%s)", (winner, loser, 3,))    
    # Commit.
    conn.commit()

    c.execute("INSERT INTO matches VALUES (%s,%s,%s)", (loser, winner, 0,))
    
    # Commit.
    conn.commit()

    # Close the database connection.
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


