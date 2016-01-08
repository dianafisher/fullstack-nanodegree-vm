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

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# set up routes

@app.route('/')
@app.route('/restaurants')
# List restaurants
def listRestaurants():
	# query the database
	restaurants = session.query(Restaurant).all()	

	# return list of restaurants found
	return render_template('restaurants.html', restaurants=restaurants)	

# Create a new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	# Handle POST request
	if request.method == 'POST':
		restauraunt = Restaurant(name = request.form['name'])		
		session.add(restauraunt)
		session.commit()
		# flash("new restaurant created!")

		# Redirect back to the main page
		return redirect(url_for('listRestaurants'))
	else:
		# Handle GET request
		return render_template('newrestaurant.html')
	# return "page to create a new restaurant"

# Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	# Handle POST request
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
			session.add(editedRestaurant)
			session.commit()
			# flash("Restaurant edited!")
		return redirect(url_for('listRestaurants'))
	else:	
		# Handle GET request	
		return render_template('editrestaurant.html', restaurant_id = restaurant_id, restaurant = editedRestaurant)	

# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):	
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		# flash("Restaurant deleted!")
		return redirect(url_for('listRestaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant_id = restaurant_id, restaurant = restaurantToDelete)	

# Show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu/', methods=['GET', 'POST'])
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant=restaurant, items = items)	

# Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		# flash("Menu item edited!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:		
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		# flash("Menu item deleted!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToDelete)
    
# API endpoints (GET request)
@app.route('/restaurants/JSON')
def restrauntsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	# return JSON
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	# restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	# items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	item = session.query(MenuItem).filter_by(id = menu_id).one()

	# return JSON
	return jsonify(MenuItem=item.serialize)    

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)