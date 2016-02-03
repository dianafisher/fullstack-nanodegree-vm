from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

# Define the user table.
class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))
	last_seen = Column(DateTime)

	@property
	def is_authenticated(self):
	    return True
	

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False, unique=True)	

	@property
	def serialize(self):
		"""Returns object data in easily serializeable format"""
		return {
			'name'	: self.name,
			'id'	: self.id
		}
	

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	dateAdded = Column(DateTime)
	lastUpdated = Column(DateTime)
	description = Column(String(250))
	imageFilename = Column(String(250))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	
	# make a foreign key reference to the Category in which this item resides
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)

	@property
	def serialize(self):
		"""Returns object data in easily serializeable format"""
		return {
			'name'	: self.name,
			'id'	: self.id,
			'dateAdded'	: self.dateAdded,
			'lastUpdated' : self.lastUpdated,
			'description'	: self.description,
			'imageFilename'	: self.imageFilename
		}

engine = create_engine('sqlite:///minifigures.db')
 

Base.metadata.create_all(engine)