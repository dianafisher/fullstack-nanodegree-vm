from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///df_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create categories
cat1 = Category(name="Video Games")
session.add(cat1)
session.commit()

cat2 = Category(name="Trains")
session.add(cat2)
session.commit()

cat3 = Category(name="DC Comics Super Heroes")
session.add(cat3)
session.commit()

cat4 = Category(name="Jurassic World")
session.add(cat4)
session.commit()
