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

# imports for momentjs (for displaying relative dates)
import momentjs
from datetime import datetime


# impports for file upload
import os
from werkzeug import secure_filename
from flask import send_from_directory

# Configure file upload directory and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS =  set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

	return render_template('catalog.html', categories=categories, items=items)	
	# return 'Categories appear here.  Latest added items also appear.'

# Show items in a category (by category name)
@app.route('/catalog/<category_name>')
def showCategory(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id)	
	
	return render_template('category.html', category=category, items=items)	

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
# @app.route('/catalog/<int:category_id>/items/new', methods=['GET','POST'])
# def newItem(category_id):
# 	return 'Page to add an item to a category.'

# Create new item (using category_name)
@app.route('/catalog/<category_name>/items/new', methods=['GET','POST'])
def newItem(category_name):
	if request.method == 'POST':
		# Create the new item
		print 'adding item to category %s' % category_name
				
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		category = session.query(Category).filter_by(name = category_name).one()
		newItem = Item(
			name=request.form['name'], 
			category=category,
			description=request.form['description'],
			imageFilename=filename,
			dateAdded=datetime.utcnow(),
			lastUpdated=datetime.utcnow()
		)
		session.add(newItem)		
		session.commit()

		flash('New Item %s Successfully Created' % newItem.name)
		# redirect to show the items in the category.
		return redirect(url_for('showCategory', category_name=category_name))
	else:
		return render_template('newItem.html')
			
	return 'Page to add an item to a category.'	

# View item
@app.route('/catalog/<category_name>/<item_name>', methods=['GET', 'POST'])
def viewItem(category_name, item_name):
	"""Renders view to display item information.
	"""
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(category_id = category.id, name=item_name).one()	
	updated = momentjs.Momentjs(item.lastUpdated).fromNow()
	return render_template('item.html', item=item, updated=updated)	

# Update (edit) item
@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	category = session.query(Category).filter_by(name = category_name).one()
	editedItem = session.query(Item).filter_by(category_id = category.id, name=item_name).one()

	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']		

		if request.form['description']:
			editedItem.description = request.form['description']				

		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			editedItem.imageFilename=filename
		
		editedItem.lastUpdated=datetime.utcnow()
		session.add(editedItem)
		session.commit()
		flash('Item successfully edited')
		return redirect(url_for('viewItem', category_name=category_name, item_name=editedItem.name))
	else:
		return render_template('editItem.html', item=editedItem)
	

# Delete item (by id)	
@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
	return 'Page to delete an item'

# Delete item (by name)
@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
def deleteItemWithName(category_name, item_name):
	return 'Page to delete an item'

### File Uploads ###

def allowed_file(filename):
	"""Checks if filename has one of the allowed extensions as defined in ALLOWED_EXTENSIONS.	
	"""
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/catalog/upload', methods=['GET', 'POST'])
def upload_file():
	"""Uploads file to the 'uploads' directory.	
	"""
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print url_for('uploaded_file',filename=filename)
			return redirect(url_for('uploaded_file',
                                    filename=filename))
	else:
		return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


# photos = UploadSet('photos', IMAGES)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
# 	if request.method == 'POST' and 'photo' in request.files:
# 		filename = photos.save(request.files['photo'])
# 		rec = Photo(filename=filename, user=g.user.id)
# 		rec.store()
# 		flash("Photo saved.")
# 		return redirect(url_for('show', id=rec.id))
# 	return render_template('upload.html')

# @app.route('/photo/<id>')
# def show(id):
# 	photo = Photo.load(id)
# 	if photo is None:
# 		abort(404)
# 	url = photos.url(photo.filename)
# 	return render_template('show.html', url=url, photo=photo)

### JSON API endpoints ###

# Get entire catalog
@app.route('/catalog.json')
def catalogJSON():
	# get the categories from the database.
	categories = session.query(Category).order_by(asc(Category.name))

	return {}

# Get a category
@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
	return {}

# Get an item
@app.route('/catalog/<int:item_id>/JSON')
def itemJSON(item_id):
	return {}

### ATOM feed endpoint ###
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
			# links=[{'href' : 'none'}],
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