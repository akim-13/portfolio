import sqlite3
import logging
import inspect


#################### DEBUGGING ####################
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
###################################################


# Shortcuts for using SQL.
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


def display_menu(options):
    print('Available options:')
    for key, value in sorted(options.items()):
        print(f'{key}. - {value[0]}')


def quit_app():
    print("Thank you for using AirlineDB!")
    return


def insert_data():
    pass


def search_data():
    pass


def update_data():
    pass


def delete_data():
    pass


def choose_summary_statistics():
    pass


def extra1():
    pass


def extra2():
    pass
    

options = {
    0: ("Quit", quit_app),
    1: ("Insert", insert_data),
    2: ("Search", search_data),
    3: ("Update", update_data),
    4: ("Delete", delete_data),
    5: ("Summary Statistics", choose_summary_statistics),
    6: ("Extra 1", extra1),
    7: ("Extra 2", extra2)
}


def main():
    create_tables()

    inp = None 
    while inp != 0:
        display_menu(options)

        inp = input('>> ')

        # Verify that the input is valid.
        try:
            inp = int(inp)
            num_of_options = len(options)
            if (inp < 0) or (inp >= num_of_options): raise
        except:
            print("ERROR: Please enter a valid integer.\n")
            continue

        selected_option = options.get(inp)
        execute_selected_option = selected_option[1]()

    db.close()

    
if __name__ == '__main__':
    main()

