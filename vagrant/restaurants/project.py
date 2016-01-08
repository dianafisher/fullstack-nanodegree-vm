from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# create instance of the Flask class
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# API endpoints (GET request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	# return JSON
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	# restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	# items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	item = session.query(MenuItem).filter_by(id = menu_id).one()

	# return JSON
	return jsonify(MenuItem=item.serialize)


# decorators
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant=restaurant, items = items)
	# output = ''
	# for i in items:
	# 	output += i.name
	# 	output += '</br>'
	# 	output += i.price
	# 	output += '</br>'
	# 	output += i.description
	# 	output += '</br>'
	# 	output += '</br>'
	# return output


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])

def newMenuItem(restaurant_id):
    # Handle POST request
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		# newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")

		# Redirect back to the main page
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		# Handle GET request
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)
    # return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])

def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Menu item edited!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		#USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])

def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToDelete)
    


# if executing with Python interpreter..
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	# enable debug support
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)