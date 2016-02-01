from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# for generation of unique session token...
from flask import session as login_session
import random, string

# imports for oauth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# imports for Atom feed
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed, FeedEntry

# Connect to the catalog database and create database session
engine = create_engine('sqlite:///df_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def make_external(url):
	return urljoin(request.url_root, url)

### Routes ###

# Homepage - shows all current categories with the latest added items.
@app.route('/')
@app.route('/catalog/')
def index():
	# get the categories from the database.
	categories = session.query(Category).order_by(asc(Category.name))

	# get the latest added items.
	items = session.query(Item).order_by(desc(Item.dateAdded))
	for i in items:
		print i.name

	return render_template('catalog.html', categories=categories)	
	# return 'Categories appear here.  Latest added items also appear.'

# Show items in a category (by id)
@app.route('/catalog/<int:category_id>/')
def showCategory(category_id):
	return 'Page to show items in a category.'

# Show items in a category (by category name)
@app.route('/catalog/<category_name>')
def showCategory(category_name):
	response = 'Page to show items in a category %s.' % category_name
	return response

# Create new category
@app.route('/catalog/category/new', methods=['GET', 'POST'])
def createCategory():
	return 'Page to create a new category.'

# Edit Category (by id)
@app.route('/catalog/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
	return 'Page to edit a category.'

# Edit Category (by category name)
@app.route('/catalog/<category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):
	return 'Page to edit a category %s.' % category_name	

# Delete Category (by id)
@app.route('/catalog/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
	return 'Page to delete a category.'

# Delete Category (by category name)
@app.route('/catalog/<category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
	return 'Page to delete category %s.' % category_name

### Items ####

# Create new item (using category_id)
@app.route('/catalog/<int:category_id>/items/new', methods=['GET','POST'])
def newItem(category_id):
	return 'Page to add an item to a category.'

# Create new item (using category_name)
@app.route('/catalog/<category_name>/items/new', methods=['GET','POST'])
def newItem(category_name):
	return 'Page to add an item to a category.'	

# Update (edit) item (by id)
@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
	return 'Page to edit an item'

# Update (edit) item (by name)
@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	return 'Page to edit an item'

# Delete item (by id)	
@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
	return 'Page to delete an item'

# Delete item (by name)
@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
	return 'Page to delete an item'

### JSON API endpoints ###

# Get entire catalog
@app.route('/catalog/JSON')
def catalogJSON():
	return {}

# Get a category
@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
	return {}

# Get an item
@app.route('/catalog/<int:item_id>/JSON')
def itemJSON(item_id):
	return {}

### ATOM endpoint ###
@app.route('/catalog/recent.atom')
def recent_feed():
	feed = AtomFeed('Recent Items',
		feed_url = request.url, 
		url = request.url_root,
		subtitle="Most recent items.")

	items = session.query(Item).order_by(asc(Item.dateAdded))
	print 
	for item in items:
		print item.category.name	
		categories = []	
		cat = {'term' : 'sports', 'label': 'none'}				
		categories.append(cat)
		print categories
		author = {'name': 'unknown', 'email': 'unknown@gmail.com'}

		entry = FeedEntry(item.name, item.description,
			content_type='html',
			author=author,
			links=[{'href' : 'none'}],
			categories=[{'term' : 'sports'}],
			added=item.dateAdded,
			id=request.url_root + 'catalog/items/' + str(item.id),
			published=item.dateAdded,
			updated=item.lastUpdated)

		# print entry.to_string()

		feed.add(entry)
		# feed.add(item.name, unicode(item.description),
		# 	content_type='html',
		# 	author=author,
		# 	categories=[item.category.name],
		# 	added=item.dateAdded,
		# 	id=request.url_root + 'catalog/items/' + str(item.id),
		# 	published=item.dateAdded,
		# 	updated=item.lastUpdated
		# 	)

	return feed.get_response()

# Run the server
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)	