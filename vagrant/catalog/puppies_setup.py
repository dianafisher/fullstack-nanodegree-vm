import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# create the base class for our classes to inherit
Base = declarative_base()

### Shelter class

class Shelter(Base):

	__tablename__ = 'shelter'

	# set up mappers
	name = Column(String(80), nullable = False)
	address = Column(String(250))
	city = Column(String(250))
	state = Column(String(20))
	zipCode = Column(String(10))
	website = Column(String)
	id = Column(Integer, primary_key = True)

### Puppy class
class Puppy(Base):

	__tablename__ = 'puppy'

	# set up mappers
	name = Column(String(80), nullable = False)
	dateOfBirth = Column(Date)
	gender = Column(String(6), nullable = False)
	picture = Column(String)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	weight = Column(Numeric(10))
	id = Column(Integer, primary_key = True)
	



### at end of file ###

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)