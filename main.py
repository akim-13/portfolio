import sqlite3
import logging
import inspect

############ DEBUGGING ############ 
lvl = logging.DEBUG 
fmt = '%(lineno)s: [%(levelname)s] %(msg)s'
logging.basicConfig(level = lvl, format = fmt)
def d(log):
    frame = inspect.currentframe().f_back
    logging.getLogger().debug(log, stacklevel=2)
def i(log):
    frame = inspect.currentframe().f_back
    logging.getLogger().info(log, stacklevel=2)
def w(log):
    frame = inspect.currentframe().f_back
    logging.getLogger().warning(log, stacklevel=2)
def e(log):
    frame = inspect.currentframe().f_back
    logging.getLogger().error(log, stacklevel=2)
################################### 

db = sqlite3.connect('airline.db') 
cursor = db.cursor()
sql = lambda query: cursor.execute(query)

def create_tables():
    # Create table Aircrafts.
    sql('''
    CREATE TABLE IF NOT EXISTS Aircrafts (
        aircraftID INT PRIMARY KEY,
        maxCapacity INT,
        accessible BOOLEAN,
        model TEXT)
    ''')

    # Create table Flights.
    sql('''
    CREATE TABLE IF NOT EXISTS Flights (
        flightID INT PRIMARY KEY,
        aircraftID INT NOT NULL,
        numOfPassengers INT,
        origin VARCHAR(50),
        destination VARCHAR(50),
        departureTime INT,  -- UNIX time, DATETIME is not supported.
        landingTime INT,
        FOREIGN KEY (aircraftID) REFERENCES Aircrafts(aircraftID))
    ''')

    # Create table Pilots.
    sql('''
    CREATE TABLE IF NOT EXISTS Pilots (
        pilotID INT PRIMARY KEY,
        firstName TEXT,
        surname TEXT,
        dob TEXT)
    ''')

    # Create table AssignedPilots.
    sql('''
    CREATE TABLE IF NOT EXISTS AssignedPilots (
        pilotID INT,
        flightID INT,
        PRIMARY KEY (pilotID, flightID),
        FOREIGN KEY (pilotID) REFERENCES Pilots(pilotID),
        FOREIGN KEY (flightID) REFERENCES Flights(flightID))
    ''')

    db.commit()

    i('Airline database and tables created successfully.')

def main():

    create_tables()

    db.close()

    
if __name__ == '__main__':
    main()

