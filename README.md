## Quick Start

To run the app, all you need to do is run the following command in the project repository. Then login to the app using the details below in 'Login Details'

```python
$ python3 ./app.py
```

## Manual Setup

If for some reason the quick start method doesnt work, please use the below method: 

```python
# create a virtual environment
$ python3 -m venv pyenv

# activate it
$ source pyenv/bin/activate

# install all the dependencies
$ pip3 install -r requirements.txt

# run the app
$ python3 ./app.py
```


## Other comments on Installation =
This is a GUI (Graphical User Interface) application, which uses several libraries specified in the requirements.txt file.

If an error is thrown upon running the app, and it asks for a specific library, please run the following command in your IDE terminal “pip3 install <name of library>” or “pip install <name of library>” to install the necessary library. 

Begin the application by running app.py

A sqlite3 database file called RFG.db will exist upon running the app. If the database doesn’t exist for some reason, please run databaseSetup.py in your IDE terminal.

You can then create users and use features via the self-explanatory fields in the GUI 

## Login details

Admin login details: 

username: admin1, password: passadmin

Use these details to login to the Admin dashboard and use the system as an admin. Only one admin account exists. 

Volunteer login details: 

username: volunteerjames, password: passvolunteer

Use these details to login to the above volunteer profile. The app is loaded with several dummy volunteers. All the volunteer profiles have the same password: passvolunteer. 

## What does e-adam do and why? 
- E-Adam is a humanitarian emergency management system
- It’s designed to support humanitarian agencies in their support of refugees fleeing from natural disasters
-E-Adam can record details of these refugees, and allocate them to camps with the necessary resources to accommodate them e.g. food, camp capacity, volunteers and medical supplies
- There are two types of user accounts that can be created: Admins and Volunteers. These represent different types of staff that would work for a humanitarian agency. 
- Admins can create emergency plans, which represent the humanitarian agencies response to a particular emergency, the camps associated with that emergency and also the refugees in the camp. Admins can also manage the other user type accounts, 
- Volunteers can create emergency profiles that represent all of the information about a refugee e.g. their family size, name, medical conditions etc. 

## Technologies Used
-Python
-SQLite

## Libraries Used
• TKinter
• Pandas
• Geopandas
• Fiona
• Geopy
• Tkcalendar
• python-weather

## Developers

•	Adeyemi, Sola
•	Kwon, Ohhun
•	Nguyen, Charles
•	Solomon, Marc
•	Uddin, Thamanna
•	Ugwueze, Vincent
•	Vijay, Vivek

