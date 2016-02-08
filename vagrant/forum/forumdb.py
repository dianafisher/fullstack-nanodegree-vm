#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
#DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    query = "select content, time from posts order by time DESC"
    c.execute(query)
    rows = c.fetchall()
    posts = []
    for row in rows:      
      print row[1]
      print row[0]
      r = {'content': row[1], 'time': row[0]}
      posts.append(r)
    
    # posts.sort(key=lambda row: row['time'], reverse=True)
    DB.close()

    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")    
    t = time.strftime('%c', time.localtime())
    # DB.append((t, content))
    c = DB.cursor()
    query = "insert into posts values (%s)", (content)
    # "insert into posts (content) values ('%s')" % content
    # use query parameters instead of string concatenation!
    c.execute("insert into posts values (%s)", (content,))  
    DB.commit()
    DB.close()
    
