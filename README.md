# Amity Room Allocation
Amity Room Allocation is a system that is used to allocate rooms to people. Room can either be offices or livingspaces. Offices  have a maximum capacity of 6 while living spaces have a maximum capacity of 4. Rooms are allocated to each person at random when they are added to the system.

Fellows can chose a living space or not. Staff can only be allocated an office and people can request for reallocation where they will be reallocated to a random room of the same type.

## Additional Features
### Operational
* Random room allocation.
* Fellows can not be reallocated to living spaces of opposite gender.
* Neither staff nor fellow can be added to Amity facility if there are no rooms
### Technical
* The system operates with a session database which holds data during the period the application is running. The session database is destroyed once the user quits the application or on Keyboard interrupt but the data is automatically saved to an application database by default called `default_amity.db`. The feature is called ``safe_mode``
* The system allows the user to load data from an existing database with validations to ensure the name of the database provided refers to an SQLite3 database and the database conforms to the application model i.e Contains ``persons`` and ``rooms`` tables.
* A user can also load peoples data from a text file by specifying the name of the text file.

**Note:** I case of an accidental system shutdown, forced shutdown or unexpected power outage, the application has the ability to maintain its state and continue on system restart which secures the system against accidental data loss. (Incase you added 200 records and the system shut down)

Create a virtual environment and activate it using [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Clone this repo:
```
$ git clone -b docopt-cmd --single-branch git@github.com:kimobrian/amity-booking.git 
```
for SSH and the following for HTTPS 

```git clone -b docopt-cmd --single-branch https://github.com/kimobrian/amity-booking.git```


Navigate to the `amity-booking` directory and install dependecies with:
```
$ cd amity-booking
$ pip install -r requirements.txt
```
Navigate into the application folder with:
```
$ cd application
```
Run the application with:
```
$ python app.py
```

To run tests, navigate into `application` folder and run ``nosetests``



