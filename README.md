# user-story-manager-annakonda

It works with postgresql. The ORM technologie is sqlalchemy.
To be able to connect to your database you need to create a json file, which is next to "reporter.py", named "connection_data.json". 
The content of the file:
	{"passwd":"password_of_your_database", "db_name":"name_of_your_database"}
