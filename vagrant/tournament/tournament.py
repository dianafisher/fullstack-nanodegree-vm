#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:

    def __init__(self, db_con_str="dbname=tournament"):
        """
        Creates a database connection with the connection string provided
        :param str db_con_str: Contains the database connection string, 
        with a default value when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor();

    def execute(self, sql_query_string, params=None, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: Contain the query string to be executed
        :param bool and_close: If true, closes the database connection after executing and commiting the SQL Query
        """
        try:            
            cursor = self.cursor()
            if params:
                cursor.execute(sql_query_string, params)
            else:       
                cursor.execute(sql_query_string)            
        
        except psycopg2.DatabaseError, e:
            # Rollback any changes
            if self.conn:
                self.conn.rollback()

            # Print error message
            print 'Error %s' % e

        finally:            
            if and_close:
                self.conn.commit()
                # Close the database connection.
                self.close()
            return {"conn": self.conn, "cursor": cursor if not and_close else None}    

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    DB().execute("DELETE FROM matches", None, True)


def deletePlayers():
    """Remove all the player records from the database."""

    DB().execute("DELETE FROM players", None, True)


def countPlayers():
    """Returns the number of players currently registered."""

    conn = DB().execute("SELECT count(*) FROM players")
    cursor = conn["cursor"].fetchall()
    
    # # Close the database connection.
    conn["conn"].close()
    
    # return result
    return cursor[0][0]    


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
       
    # Create query to insert the player name into the players table.
    # Follows http://initd.org/psycopg/docs/usage.html to avoid SQL
    # injection.
    query = "INSERT INTO players VALUES (%s)"

    # Hold the data to be inserted.
    data = (name,)

    # Execute the SQL query.    
    DB().execute(query, data, True)    


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = DB().execute("SELECT * FROM player_standings_view")
    cursor = conn["cursor"].fetchall()
    
    # # Close the database connection.
    conn["conn"].close()
    
    # return result
    return cursor 


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    # Create the SQL query to insert the winner and loser player ids.
    # Follows http://initd.org/psycopg/docs/usage.html to avoid SQL
    # injection.
    query = "INSERT INTO matches VALUES (%s,%s)"

    # Hold the data to be inserted in a variable.
    data = (winner, loser,)

    # Execute the SQL query.    
    DB().execute(query, data, True)    


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

    conn = DB().execute("SELECT odd_rows_view.id, odd_rows_view.name, even_rows_view.id, even_rows_view.name FROM odd_rows_view, even_rows_view WHERE even_rows_view.row_num = odd_rows_view.row_num + 1")
    cursor = conn["cursor"].fetchall()
    
    # # Close the database connection.
    conn["conn"].close()
    
    # return result
    return cursor     
