from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# define the webserverHandler class
class webserverHandler(BaseHTTPRequestHandler):
	

	def do_GET(self):
		try:
			if self.path.endswith("/delete"):
				parts = self.path.split("/")
				restaurant_id = parts[2]
				print restaurant_id

				# get the restaurant from the database
				restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
				
				if restaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()	

					# Show confirmation.
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant_id					
					output += "<input type='submit' value='Delete'> </form>"
					output += "</body></html>"

					self.wfile.write(output)

			if self.path.endswith("/edit"):
				print self.path;
				parts = self.path.split("/")
				restaurant_id = parts[2]
				print restaurant_id
				# get the restaurant from the database
				restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
				
				if restaurant:

					print restaurant.name

					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()	
				
					output = ""
					output += "<html><body>"
					output += "<h1>Edit Restaurant</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant_id
					output += "<input name='restaurantName' type='text' placeholder='%s'>" % restaurant.name
					output += "<input type='submit' value='Rename'> </form>"
					output += "</body></html>"

					self.wfile.write(output)					

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()		
				
				output = ""
				output += "<html><body>"
				output += "<h1>Create a New Restaurant</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text" placeholder="New Restaurant Name"><input type="submit" value="Create"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()				
				
				restaurants = session.query(Restaurant).all()
				
				output = ""
				output += "<html><body>"
				output += "<h1>Restaurants</h1>"
				output += '<a href=/restaurants/new>Add a new restaurant</a><br></br>'
				for r in restaurants:
					print r.name
					output += "<div>"
					output += r.name + "</br>"					
					output += '<a href="/restaurants/%s/edit">Edit</a></br>' % r.id
					output += '<a href="/restaurants/%s/delete">Delete</a>' % r.id
					output += "</div></br>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>&#161 Hola !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)
		
	def do_POST(self):
		try:
			if self.path.endswith("/delete"):
				# get the restaurant from the database.
				parts = self.path.split("/")
				restaurant_id = parts[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
				if restaurant:
					# delete it from the database
					session.delete(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					# redirect to /restaurants
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurantName')

					# get the restaurant from the database.
					parts = self.path.split("/")
					restaurant_id = parts[2]
					print restaurant_id					
					restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
					
					# # Update restaurant.
					if restaurant:
						restaurant.name = messagecontent[0]
						session.add(restaurant)
						session.commit()

						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						# redirect to /restaurants
						self.send_header('Location', '/restaurants')
						self.end_headers()

			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					
					# Create a new restaurant.
					r = Restaurant(name = messagecontent[0])
					session.add(r)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					# redirect to /restaurants
					self.send_header('Location', '/restaurants')
					self.end_headers()


			# self.send_response(301)
			# self.send_header('Content-type', 'text/html')
			# self.end_headers()

			# ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			# if ctype == 'multipart/form-data':
			# 	fields = cgi.parse_multipart(self.rfile, pdict)
			# 	messagecontent = fields.get('message')

			# output = ""
			# output += "<html><body>"
			# print messagecontent[0]

			

			# # output += " <h2> Okay, how about this: </h2>"
			# output += "<h1> %s added</h1>" % messagecontent[0]
			# # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			# output += "</body></html>"
			# self.wfile.write(output)
			# print output

		except:
			print 'something went wrong...'


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
	
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':
	main()