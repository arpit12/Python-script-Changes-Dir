
Python that detects the changes in a given Directory and logs the changes in a mysql database.
######################## How to Run #############################

1.)	Install python-mysqldb connector :-
	sudo apt-get install python-mysqldb

2.)	Simply run this file in your system , so it will create database table .
	Pre-requeste : Login in mysql console and create test database , with username and password both root or whatever you have just update those in script.py
	Run :- 
	python database.py # This scripts check for new files/dir every 3 seconds .

	This will create table files in database test with following schema:-
	where file_name = "name of file." and
	comment = " information about dir/sub-dir/files (added/deleted/modified) "

    It will prints on console also whatever operations did and also inserts same in database and if data added in sub-dir then will insert both features added 
    and modified as new file append to sub-dir.

	+----+-----------+----------+
	| id | file_name | comment  |
	+----+-----------+----------+

	This script will treat your current path as source path and checks files/dir/sub-dir from that dir and
	prints all file/dir names in mysql wherever you when create/modify/rename file/data . 

################################################################

