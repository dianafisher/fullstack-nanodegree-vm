import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# create the base class for our classes to inherit
Base = declarative_base()

### Restaurant class

class Restaurant(Base):

	__tablename__ = 'restaurant'

	# set up mappers
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

### MenuItem class
class MenuItem(Base):

	__tablename__ = 'menu_item'

	# set up mappers
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		# Returns object data in easily serializeable format.
	    return {
	    	'name': self.name,
	    	'description': self.description,
	    	'id': self.id,
	    	'price': self.price,
	    	'course': self.course
	    }
	

### at end of file ###

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.create_all(engine)