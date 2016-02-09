# LEGO Minifigures Catalog

A catalog web application written in Python and Flask.  Users can create categories and add minifigures to any category which they have created.  A "My Collection" section is available for users to indicate they own (physical versions of) minigures listed in the app.

OAuth2 user authentication is supported via Google.

### Requirements

- Vagrant VM (https://www.vagrantup.com/downloads)
- VirtualBox (https://www.virtualbox.org/wiki/Downloads)
- Python 2.7 or higher
- [SQLAlchemy](http://www.sqlalchemy.org/download.html)
- Flask-SeaSurf (https://flask-seasurf.readthedocs.org/en/latest/)

### Installation
1. Clone the GitHub repository.  This repository contains a shell script pg_config.sh which automates the installation and configuration of the Vagrant VM.  This includes installation of the psycopg2 PostGreSQL adapter.

	$ git clone https://github.com/dianafisher/fullstack-nanodegree-vm.git

2. Launch the Vagrant virtual machine.

	$ cd vagrant
	$ vagrant up

3. Log into the Vagrant virtual machine.

	$ vagrant ssh

4. Change directories to enter the catalog directory.

	$ cd \vagrant\catalog

5. Create the catalog database from the database_setup.py file provided.
	
	$ python database_setup.py

6. Optionally, pre-populate the catalog databse by executing the database_populator.py script provided

	$ database_populator.py

7. To support user authentication, register the app at [Google](https://console.developers.google.com/project).  Download the client_secrets.json 

 