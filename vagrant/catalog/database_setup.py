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

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False, unique=True)

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	dateAdded = Column(DateTime)
	lastUpdated = Column(DateTime)
	description = Column(String(250))
	
	# make a foreign key reference to the Category in which this item resides
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)


engine = create_engine('sqlite:///df_catalog.db')
 

Base.metadata.create_all(engine)