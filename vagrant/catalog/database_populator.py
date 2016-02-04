from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

from datetime import datetime

engine = create_engine('sqlite:///minifigures.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
user1 = User(
	name="President Business",
	email="business@octan.com",
	picture='http://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2014/02/20/101432762-Lego_WPS_1920_biz-1.530x298.jpg?v=1394539906')
session.add(user1)
session.commit()

# Create categories
series1 = Category(user_id=1, name="Series 1")
session.add(series1)
session.commit()

series2 = Category(user_id=1, name="Series 2")
session.add(series2)
session.commit()

series3 = Category(user_id=1, name="Series 3")
session.add(series3)
session.commit()

# Add items to categories
zombie= Item(
	user_id=1,
	name="Zombie", 
	description="He's got a shovel and a turkey leg.", 
	category=series1,
	imageFilename='Zombie-261x300.jpg',
	dateAdded=datetime.utcnow(),
	lastUpdated=datetime.utcnow()
	)
session.add(zombie)
session.commit()

robot= Item(
	user_id=1,
	name="Robot",
	description="Shiny and metal.",
	category=series1,
	imageFilename='Robot-261x300.jpg',
	dateAdded=datetime.utcnow(),
	lastUpdated=datetime.utcnow()
	)
session.add(robot)
session.commit()

disco=Item(
	user_id=1,
	name="Disco Dude",
	description="Straight from the 70s.",
	category=series2,
	imageFilename='Disco-Dude-261x300.jpg',
	dateAdded=datetime.utcnow(),
	lastUpdated=datetime.utcnow()
	)
session.add(disco)
session.commit

mummy= Item(
	user_id=1,
	name="Mummy",
	description="Green skin with lots of bandages.",
	category=series3,
	imageFilename='Mummy-261x300.jpg',
	dateAdded=datetime.utcnow(),
	lastUpdated=datetime.utcnow()
	)
session.add(mummy)
session.commit()

