from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy import create_engine

Base = declarative_base()


# Define the user table.
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Returns object data in easily serializeable format"""
        return {'name': self.name, 'id': self.id}


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    dateAdded = Column(DateTime)
    lastUpdated = Column(DateTime)
    description = Column(String(1000))
    imageFilename = Column(String(250))

    # Create a foreign key with the User table to store which user created
    # this item.
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Create a foreign key reference to the Category in which this item resides.
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)    
    # Propogate the deletion of the category in which this item resides to also delete this item.
    category = relationship(Category, backref=backref('Category', cascade="all, delete-orphan"), single_parent=True)

    @property
    def serialize(self):
        """Returns object data in easily serializeable format"""
        return {'name': self.name,
                'id': self.id,
                'dateAdded': self.dateAdded.isoformat(),
                'lastUpdated': self.lastUpdated.isoformat(),
                'description': self.description,
                'imageFilename': self.imageFilename}


'''Create a mapping between users and items.  This is used to store what
items each user has.'''


class UserItem(Base):
    __tablename__ = 'useritems'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship(User)

    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship(Item)


engine = create_engine('sqlite:///minifigures.db')

Base.metadata.create_all(engine)
