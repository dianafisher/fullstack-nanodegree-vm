# LEGO Minifigures Catalog

A catalog web application written in Python and Flask.  Users can create categories (e.g. 'Series 1', 'Star Wars', etc.) and add minifigures to any category (even if they did not create that category).  However, only the creator of a category can modify it's name or delete the category.

Additionally, users may only modify or delete minifigures which they have created.

A "My Collection" section is available for users to indicate they own (physical versions of) minigures listed in the app.  A user can add any item to their collection even if they did not create the item.

OAuth2 user authentication is supported via Google sign in.

### Features
- CRUD of categories and items in database
- JSON and Atom feed endpoints
- Image upload for items
- cross-site request forgery prevention
- Google sign-in for user authentication


### Requirements

- Vagrant VM (https://www.vagrantup.com/downloads)
- VirtualBox (https://www.virtualbox.org/wiki/Downloads)
- Python 2.7 or higher
- [SQLAlchemy](http://www.sqlalchemy.org/download.html)
- Flask-SeaSurf (https://flask-seasurf.readthedocs.org/en/latest/) for CSRF prevention

### Installation
1. Clone the GitHub repository.  This repository contains a shell script pg_config.sh which automates the installation and configuration of the Vagrant VM.  This includes installation of the psycopg2 PostGreSQL adapter.

	$ git clone https://github.com/dianafisher/fullstack-nanodegree-vm.git

2. Change directories to enter the vagrant directory and launch the Vagrant virtual machine
	
	```sh
	$ cd vagrant
	$ vagrant up
	```

4. Log into the Vagrant virtual machine.

	```sh
	$ vagrant ssh
	```

5. Change directories to enter the catalog directory.

	```sh
	$ cd \vagrant\catalog
	```

6. Create the catalog database from the database_setup.py file provided.
	
	```sh
	$ python database_setup.py
	```

7. Optionally, pre-populate the catalog databse by executing the database_populator.py script provided.

	```sh
	$ python database_populator.py
	```

### Running

Launch the app by executing application.py with the Python interpreter.
	
	$ python application.py	

Open a web browser and go to http://localhost:8000 


 