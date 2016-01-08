from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# create an instance of Flask
app = Flask(__name__)

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# set up routes

@app.route('/')
@app.route('/restaurants')
# List restaurants
def listRestaurants():
	# query = session.query(Restaurant).all()
	# for r in query:
	# 	print r.name

	# print restaurants
	return render_template('restaurants.html', restaurants=restaurants)
	# return "page to list all restaurants"

# Create a new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	return "page to create a new restaurant"

# Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	return "page to edit a restaurant"

# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	return "page to delete a restaurant"

# Show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu/', methods=['GET', 'POST'])
def showMenu(restaurant_id):
	return "page to show a restaurant menu"

# Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	return "page to add a menu item"

# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a menu item"

# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	return "page to delete a menu item"

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)