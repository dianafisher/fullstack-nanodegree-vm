## Tournament Results

Tournament Results keeps track of players and matches in a game tournment.  The tournament uses the Swiss system for pairing players in each round of the tournament. 

### Requirements
- Vagrant VM (https://www.vagrantup.com/downloads)
- VirtualBox (https://www.virtualbox.org/wiki/Downloads)
- Python 2.7.10
- psycopg2 PostgreSQL adapter for Python

### Installation
1. Clone the GitHub repository.  This repository contains a shell script pg_config.sh which automates the installation and configuration of the Vagrant VM.  This includes installation of the psycopg2 PostGreSQL adapter.

	$ git clone https://github.com/dianafisher/fullstack-nanodegree-vm.git

2. Launch the Vagrant virtual machine.

	$ cd vagrant
	$ vagrant up

3. Log into the Vagrant virtual machine.

	$ vagrant ssh

4. Change directories to enter the tournament directory.

	$ cd \vagrant\tournament

5. Launch postgreSQL
	
	$ psql

6. Create the tournament database from the tournament.sql file provided.

	vagrant=> \i tournament.sql

	You should now see the following output:

		You are now connected to database "vagrant" as user "vagrant".
		DROP DATABASE
		CREATE DATABASE
		You are now connected to database "tournament" as user "vagrant".
		CREATE TABLE
		CREATE TABLE
		CREATE INDEX
		CREATE VIEW
		CREATE VIEW
		CREATE VIEW
		
		tournament=>

7. Now that the database has been created you can run the tournament_test.py script.

	To remain in the same terminal, first quit postgreSQL

		tournament=> \q

	Then ruun the tournament_test Python script

		$ python tournament_test.py

	Alternatively, you can open a separate terminal and ssh into the Vagrant VM in the new terminal.

	$ vagrant ssh
	$ cd \vagrant\tournament
	$ python tournament_test.py

