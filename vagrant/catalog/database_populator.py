from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

from datetime import datetime

engine = create_engine('sqlite:///df_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create categories
cat1 = Category(name="Video Games")
session.add(cat1)
session.commit()

game1= Item(
	name="LEGO Dimensions", 
	description="Combine building and crazy mash-up gaming with this LEGO DIMENSIONS Starter Pack, including game disc, LEGO Toy Pad with Gateway bricks, 3 minifigures and a 3-in-1 Batmobile.", 
	category=cat1,
	dateAdded=datetime.utcnow(),
	lastUpdated=datetime.utcnow())
session.add(game1)
session.commit()

game2= Item(
	name="LEGO Marvel's Avengers",
	description="Avengers Assemble! Experience the first console videogame featuring characters and storylines from the blockbuster film Marvel's The Avengers and the much anticipated sequel Marvel's Avengers: Age of Ultron, and more. Play as the most powerful Super Heroes in their quest to save humanity.",
	category=cat1,
	dateAdded=datetime.utcnow(),
	lastUpdated=datetime.utcnow())
session.add(game2)
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
