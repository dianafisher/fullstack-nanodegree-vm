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
    
    # Obtain a cursor object from the connection.
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
    
    # Obtain a cursor object from the connection.
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
    
    # Obtain a cursor object from the connection.
    c = conn.cursor()

    # Execute the SQL query to count the number of rows in the players table.
    c.execute("SELECT count(*) FROM players")

    # The count will be the first column of the first and only row.
    result = c.fetchall()[0][0]

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

    # Create empty connection object
    conn = None

    try:
        # Open the database connection.
        conn = connect()
        
        # Obtain a cursor object from the connection.
        c = conn.cursor()

        # Create the SQL query to insert the player name into the players table.
        # Follows http://initd.org/psycopg/docs/usage.html to avoid SQL injection.
        query = "INSERT INTO players VALUES (%s)"

        # Hold the data to be inserted.
        data = (name, )

        # Execute the SQL query.
        c.execute(query, data)    

        # Commit changes made to the database.
        conn.commit()

    except psycopg2.DatabaseError, e:
        # Rollback any changes.
        if conn:
            conn.rollback()

        # Print error message
        print 'Error %s' % e
    
    finally:
        # Close the database connection.
        if conn:
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

    # Open the database connection.
    conn = connect()
    
    # Obtain a cursor object from the connection.
    c = conn.cursor()

    # Execute the SQL query to count the number of rows in the players table.
    c.execute("SELECT * FROM player_standings_view")

    # Obtain the rows returned by the query.
    result = c.fetchall()
 
    # Close the database connection.
    conn.close()

    # Return the result.
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = None

    try:
        # Open the database connection.
        conn = connect()
        
        # Obtain a cursor object from the connection.
        c = conn.cursor()

        # Create the SQL query to insert the winner and loser player ids.  
        # Follows http://initd.org/psycopg/docs/usage.html to avoid SQL injection.
        query = "INSERT INTO matches VALUES (%s,%s)"

        # Hold the data to be inserted in a variable.
        data = (winner, loser, )

        # Execute the SQL query.
        c.execute(query, data)    

        # Commit changes to the database.
        conn.commit()

    except psycopg2.DatabaseError, e:
        # Rollback any changes
        if conn:
            conn.rollback()

        # Print error message
        print 'Error %s' % e
    
    finally:
        # Close the database connection.
        if conn:
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

    # Open the database connection.
    conn = connect()
    
    # Obtain a cursor object from the connection.
    c = conn.cursor()
   
    # Execute SQL query.
    # This SQL query performs a self join on the player_standings_view to obtain tuples of players having the same number of wins.
    c.execute("SELECT a.id, a.name, b.id, b.name FROM player_standings_view AS a, player_standings_view AS b WHERE a.id < b.id AND a.wins = b.wins")

    # Obtain the rows returned by the query.
    result = c.fetchall()

    # Close the database connection.
    conn.close()

    # Return the result.
    return result
