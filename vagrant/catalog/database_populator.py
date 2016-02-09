#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

from datetime import datetime

engine = create_engine('sqlite:///minifigures.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
user1 = User(name="President Business",
             email="business@octan.com",
             picture='http://fm.cnbc.com/applications/cnbc.com/resources/img'
                     '/editorial/2014/02/20/'
                     '101432762-Lego_WPS_1920_biz-1.530x298.jpg?v=1394539906')
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
caveman = Item(user_id=1,
               name="Caveman",
               description="This would-be inventor from the prehistoric past "
                           "is always tinkering with sticks, rocks and the "
                           "occasional bricks he finds lying around, trying "
                           "to invent something new.",
               category=series1,
               imageFilename='Caveman-261x300.jpg',
               dateAdded=datetime.utcnow(),
               lastUpdated=datetime.utcnow())
session.add(caveman)
session.commit()

cheerleader = Item(user_id=1,
                   name="Cheerleader",
                   description='"Gimmie an L! Gimmie an E! Gimmie a G! '
                               'Gimmie an O! Yaaay!" The Cheerleader is '
                               'perpetually filled to bursting with energy,'
                               ' excitement and enthusiasm. She prefers '
                               'cartwheels and handsprings to plain old '
                               'ordinary walking, and she waves her pom-poms'
                               ' around wildly whenever she talks, which is '
                               'pretty much all of the time.',
                   category=series1,
                   imageFilename='Cheerleader-261x300.jpg',
                   dateAdded=datetime.utcnow(),
                   lastUpdated=datetime.utcnow())
session.add(cheerleader)
session.commit()

zombie = Item(user_id=1,
              name="Zombie",
              description="Slow in speed and even slower of mind, the"
                          " lumbering Zombie may look a little scary, "
                          "but he's completely harmless in every way. "
                          "Everything he does is slow, mindless and "
                          "repetitive, from zoning out while watching TV, "
                          "to waiting in line at the grocery store, "
                          "to stacking one brick on top of another to "
                          "build a perfectly even, completely featureless "
                          "wall that stretches along for miles and miles.",
              category=series1,
              imageFilename='Zombie-261x300.jpg',
              dateAdded=datetime.utcnow(),
              lastUpdated=datetime.utcnow())
session.add(zombie)
session.commit()

robot = Item(user_id=1,
             name="Robot",
             description="He's slow to react to things that he doesn't "
                         "expect, and prone to occasional short-circuits, "
                         "with a tendency to walk right into holes, "
                         "spin around suddenly in place or crash "
                         "through walls without even noticing.",
             category=series1,
             imageFilename='Robot-261x300.jpg',
             dateAdded=datetime.utcnow(),
             lastUpdated=datetime.utcnow())
session.add(robot)
session.commit()

disco = Item(user_id=1,
             name="Disco Dude",
             description="The Disco Dude has traveled back in time "
                         "to relive the days of disco dancing, "
                         "bell-bottom pants and the very first "
                         "LEGO Space sets.",
             category=series2,
             imageFilename='Disco-Dude-261x300.jpg',
             dateAdded=datetime.utcnow(),
             lastUpdated=datetime.utcnow())
session.add(disco)
session.commit()

alien = Item(user_id=1,
             name="Space Alien",
             description="Nobody knows where the Space Alien came "
                         "from or how it got here. It just showed up "
                         "one day with a map of the planet and an "
                         "Alien-to-Human dictionary, but neither one "
                         "works very well.",
             category=series3,
             imageFilename='Space-Alien-261x300.jpg',
             dateAdded=datetime.utcnow(),
             lastUpdated=datetime.utcnow())
session.add(alien)
session.commit()
