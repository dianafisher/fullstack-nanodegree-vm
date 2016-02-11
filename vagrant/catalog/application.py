from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User, UserItem

# for generation of unique session token...
from flask import session as login_session
import random
import string

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

# imports for preventing cross-site request forgery
from flask.ext.seasurf import SeaSurf

# import for decorators
from functools import wraps

# Load client id from json file obtained from Google
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'][
    'client_id']
APPLICATION_NAME = 'Catalog Appliction'

# Create the app
app = Flask(__name__)

# Add SeaSurf for cross-site request forgery prevention
csrf = SeaSurf(app)

# Configure file upload directory and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Limit image file size to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

# Connect to the database and create database session
engine = create_engine('sqlite:///minifigures.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

'''Decorator for login check'''


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:            
            return redirect(url_for('showLogin', next=request.url))
    return decorated_function

def make_external(url):
    return urljoin(request.url_root, url)

'''Error Handlers'''


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


'''Routes'''


# Homepage - shows all current categories with the latest added items.
@app.route('/')
@app.route('/catalog/')
def index():
    # get the categories from the database.
    categories = session.query(Category).order_by(asc(Category.name))

    # Get the latest added items.  Limit to 15 items.
    items = session.query(Item).order_by(desc(Item.dateAdded)).limit(15).all()

    # check if user is logged in
    if 'username' not in login_session:
        return render_template('publicCatalog.html', categories=categories,
                               items=items)
    else:
        return render_template('catalog.html', categories=categories,
                               items=items)

def category_exists(item_name):
    category = session.query(Category).filter_by(name=category_name).first()
    return category is not None


# Show items in a category (by category name)
@app.route('/catalog/<category_name>')
def showCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))

    items = session.query(Item).filter_by(category_id=category.id)

    return render_template('category.html', category=category, items=items)


# Create new category
@app.route('/catalog/category/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    
    if request.method == 'POST':
        # Check to make sure a category with this name 
        # does not already exist        
        entered_name = request.form['name']
        category = session.query(Category).filter_by(name=entered_name).first()

        if category is None:
            category = Category(user_id=login_session['user_id'],
                            name=entered_name)
            session.add(category)
            session.commit()
            flash("New Category Created")
            return redirect(url_for('index'))
        else:
            flash('Category %s already exists.' % entered_name, 'error')
            return redirect(url_for('newCategory'))
    else:
        return render_template('newCategory.html')


# Edit Category
@app.route('/catalog/<category_name>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_name):
    # Get the category from the database by the category name.
    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))

    # Check that the logged in user has authorization to edit this category.
    if category.user_id != login_session['user_id']:
        # Inform the user.
        flash('You are not authorized to edit this category.', 'error')
        # Refresh the page.
        return redirect(url_for('showCategory', category_name=category_name))

    if request.method == 'POST':        
        
        if request.form['name']:
            # Check if the entered category name already exists in the database.
            entered_name = request.form['name']                        
            c = session.query(Category).filter_by(name=entered_name).first()
            if c is not None:
                flash('Category %s already exists.' % entered_name, 'error')
                return render_template('editCategory.html', category=category)
            else:
                category.name = request.form['name']
                session.add(category)
                session.commit()
                flash("Changes saved for category %s." % category.name)
                return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template('editCategory.html', category=category)


# Delete Category
@app.route('/catalog/<category_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_name):
    
    # Get the category from the database by the category name.
    category = session.query(Category).filter_by(name=category_name).first()

    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))


    # Check that the logged in user has authorization to delete category    
    if category.user_id != login_session['user_id']:
        # Inform the user.
        flash('You are not authorized to delete this category.', 'error')
        # Refresh the page.
        return redirect(url_for('showCategory', category_name=category_name))

    if request.method == 'POST':        
        # Delete the category.
        session.delete(category)
        session.commit()
        flash("%s Category Successfully Deleted" % category_name)
        return redirect(url_for('index'))
    else:
        return render_template('deleteCategory.html', category=category)


''' Items '''


# Create new item
@app.route('/catalog/<category_name>/items/new', methods=['GET', 'POST'])
@login_required
def newItem(category_name):
    """Creates a new item in the databse for the specified category.
    A user must be logged in to add an item to a category,
    but they do not have to own the category.
    """
    # Get the category from the database by the category name.
    category = session.query(Category).filter_by(name=category_name).first()

    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Create the new item
        filename = ''
        # If an image has been uploaded, save it to the file system.
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        item_name = request.form['name']              
        item = session.query(Item).filter_by(name=item_name).first()    
        if item is not None:
            flash('%s already exists.  Please use a different name.' % item_name, 'error')
            # render_template('newItem.html')
            return redirect(url_for('newItem', category_name=category_name))

        # Create a new Item object.
        created_item = Item(user_id=login_session['user_id'],
                            name=request.form['name'],
                            category=category,
                            description=request.form['description'],
                            imageFilename=filename,
                            dateAdded=datetime.utcnow(),
                            lastUpdated=datetime.utcnow())

        # Commit the new item to the databse.
        session.add(created_item)
        session.commit()

        # Inform the user.
        flash('New Item %s Successfully Created' % created_item.name)
        # Redirect to show the items in the category.
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        # GET request, so show the page to create a new item.
        return render_template('newItem.html')


# View item
@app.route('/catalog/<category_name>/<item_name>', methods=['GET', 'POST'])
def viewItem(category_name, item_name):
    """Renders view to display item information."""

    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))

    item = session.query(Item).filter_by(name=item_name).first()    
    if item is None:
        flash('Item %s not found.' % item_name, 'error')
        return redirect(url_for('index'))

    item = session.query(Item).filter_by(category_id=category.id,
                                         name=item_name).one()

    updated = momentjs.Momentjs(item.lastUpdated).fromNow()
    user = session.query(User).filter_by(id=item.user_id).first()
    if user is None:
        flash('Item creator not found', 'error')
        return redirect(url_for('index')) 

    return render_template('item.html', item=item, updated=updated, user=user)


# Update/Edit item
@app.route('/catalog/<category_name>/<item_name>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_name):

    # Get the Category and Item to be edited.
    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))

    # Get the item to edit.
    editedItem = session.query(Item).filter_by(category_id=category.id,
                                               name=item_name).first()
    
    # If the item is not found, display an error and refresh
    if editedItem is None:
        print 'cannot find item %s' % item_name
        flash('Item %s not found.' % item_name, 'error')
        return redirect(url_for('index'))

    # Check that the logged in user has authorization to edit this item.
    if editedItem.user_id != login_session['user_id']:
        # Inform the user.
        flash('You are not authorized to modify this item. Please create your '
              'own item in order to modify.', 'error')
        # Refresh the page.
        return redirect(url_for('viewItem', category_name=category_name,
                                item_name=editedItem.name))

    # Handle the POST request
    if request.method == 'POST':
        if request.form['name']:
            entered_name = request.form['name']
            print 'entered name', entered_name
            print 'item name', editedItem.name
            # If the user enters a new name, check that it does not already exist.
            if entered_name != item_name:
                item = session.query(Item).filter_by(name=entered_name).first()    
                if item is not None:                
                    flash('Item with name %s already exists.' % entered_name, 'error')
                    return render_template('editItem.html', item=editedItem)
                else:
                    editedItem.name = entered_name

        if request.form['description']:
            editedItem.description = request.form['description']

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Check that this is a new file.  Delete the old file if it is.
            if filename is not editedItem.imageFilename:
                # Delete the old image file
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], editedItem.imageFilename))

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                editedItem.imageFilename = filename

        editedItem.lastUpdated = datetime.utcnow()
        session.add(editedItem)
        session.commit()
        flash('Item successfully edited')
        return redirect(url_for('viewItem', category_name=category_name,
                                item_name=editedItem.name))
    else:
        return render_template('editItem.html', item=editedItem)


# Delete item
@app.route('/catalog/<category_name>/<item_name>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_name):
    
    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        flash('Category %s not found.' % category_name, 'error')
        return redirect(url_for('index'))

    itemToDelete = session.query(Item).filter_by(category_id=category.id,
                                                 name=item_name).first()

    # If the item is not found, display an error and refresh
    if itemToDelete is None:
        flash('Item %s not found.' % item_name, 'error')
        return redirect(url_for('index'))

    # Check that the logged in user has authorization to edit this item.
    if itemToDelete.user_id != login_session['user_id']:
        # Inform the user.
        flash('You are not authorized to delete this item. Please create your '
              'own item in order to delete.', 'error')
        # Refresh the page.
        return redirect(url_for('viewItem', category_name=category_name,
                                item_name=itemToDelete.name))

    if request.method == 'POST':
        # Delete the item image from the database
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], itemToDelete.imageFilename))

        # Delete the item from the database
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('deleteItem.html', category_name=category_name,
                               item_name=item_name, item=itemToDelete)


''' File Uploads '''


def allowed_file(filename):
    """Checks if filename has one of the allowed extensions as defined in
    ALLOWED_EXTENSIONS.
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/catalog/upload', methods=['GET', 'POST'])
def upload_file():
    """Uploads file to the 'uploads' directory.
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print url_for('uploaded_file',filename=filename)
            return redirect(url_for('uploaded_file', filename=filename))
    else:
        return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


''' JSON API endpoints '''


# JSON for entire catalog
@app.route('/catalog/JSON')
def catalogJSON():
    # get the categories from the database.
    categories = session.query(Category).order_by(asc(Category.name))
    cats = [c.serialize for c in categories]

    # get the items for each category.
    for category in cats:
        items = session.query(Item).filter_by(category_id=category['id'])
        category['items'] = [i.serialize for i in items]

    return jsonify(Cateogries=cats)


# JSON for a specific category
@app.route('/catalog/<category_name>/items/JSON')
def categoryNameItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return jsonify(Item=[i.serialize for i in items])


# JSON for a specific category (by id)
@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(Item=[i.serialize for i in items])


# JSON for a specific item in a category
@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemByNameJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(category_id=category.id,
                                         name=item_name).one()
    return jsonify(Item=item.serialize)


# JSON for a specific item in a category (by id)
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(category_id=category_id,
                                         id=item_id).one()
    return jsonify(Item=item.serialize)


''' ATOM feed endpoint '''


@app.route('/catalog/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Items', feed_url=request.url, url=request.url_root,
                    subtitle="Most recent items.")

    items = session.query(Item).order_by(asc(Item.dateAdded))

    for item in items:
        categories = []
        cat = {'term': item.category.name, 'label': 'none'}
        categories.append(cat)

        author = {'name': item.user.name, 'email': item.user.email}

        item_id = request.url_root + 'catalog/items/' + str(item.id)

        entry = FeedEntry(item.name, item.description,
                          content_type='html',
                          author=author,
                          categories=categories,
                          added=item.dateAdded,
                          id=item_id,
                          published=item.dateAdded,
                          updated=item.lastUpdated)

        feed.add(entry)

    return feed.get_response()


''' Users '''


# User login
@app.route('/login')
def showLogin():
    # creates an anti-forgery state token
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        xrange(32))
    login_session['state'] = state
    # print 'The current session state is %s' % login_session['state']
    return render_template('login.html', STATE=state)


# User helper methods
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route("/userPicture")
def userPicture():
    return login_session['picture']


# User logout
@app.route("/logout")
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            print 'deleting session values...'
            del login_session['credentials']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['provider']
            flash("You have successfully been logged out.")
            return redirect(url_for('index'))
    else:
        flash("Not logged in.")
        return redirect(url_for('index'))


''' Methods to handle users adding items to their collection. '''


@app.route('/catalog/<category_name>/<item_name>/add')
def addToUserCollection(category_name, item_name):
    # Check that a user is logged in.
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(category_id=category.id,
                                         name=item_name).one()

    # Get the id of the current logged in user.
    user_id = login_session['user_id']

    # Check to see if this item already exists in the user's collection.
    userItem = session.query(UserItem).filter_by(user_id=user_id,
                                                 item_id=item.id).first()

    if userItem is None:
        # Add the new mapping to the databse.
        userItem = UserItem(user_id=login_session['user_id'], item_id=item.id)
        session.add(userItem)
        session.commit()
        flash("%s added to your collection." % item_name)
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        flash("%s is already in your collection." % item.name, 'error')
        return redirect(url_for('showCategory', category_name=category_name))


@app.route('/catalog/myCollection')
@login_required
def userCollection():

    # Get the id of the current logged in user.
    user_id = login_session['user_id']

    # Query the database with a join to get the user's items.
    items = session.query(Item).join(UserItem).filter(
        UserItem.item_id == Item.id).all()

    return render_template('userItems.html', items=items)


''' Google Sign In OAUTH2 Authentication '''


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print request.args['state']
    print 'The current session state is %s' % login_session['state']
    print 'The request session state is %s' % request.args.get('state')

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # Exchange the code for a credentials object
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # print 'result: ', result
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in.
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    # print login_session

    # See if user exists..
    user_id = getUserID(login_session['email'])
    if not user_id:
        # user does not exist in our database, create a new user.
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: ' \
              '150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    # print "done!"
    return output


'''
Disconnect from Google
Revokes the current user's token and resets their login_session
'''


@app.route("/gdisconnect")
def gdisconnect():
    # Disconnect connected user.
    # print 'login_session:', login_session
    credentials = login_session['credentials']
    # print 'User name is: '
    # print login_session['username']

    if credentials is None:
        # print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    # print 'In gdisconnect access token is %s', access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # print 'result is '
    # print result

    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Run the app
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
