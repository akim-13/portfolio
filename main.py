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
sql = lambda query, params=(): cursor.execute(query, params)


def prompt_for_valid_input(lower_bound, upper_bound):
    inp = None
    while True:
        inp = input('>>> ')
        inp = verify_input(inp, lower_bound, upper_bound)
        if inp == None:
            continue
        else:
            break
    return inp


def verify_input(inp, lower_bound, upper_bound):
    try:
        inp = int(inp)
        if (inp < lower_bound) or (inp > upper_bound): 
            raise
        return inp
    except:
        print("ERROR: Please enter a valid integer.")
        return None


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
    print('\nAvailable options:')
    for key, value in sorted(options.items()):
        print(f'{key}. - {value[0]}')


def quit_app():
    print("Thank you for using AirlineDB!")
    return


def view_table():
    sql('SELECT name FROM sqlite_master WHERE type="table"')    
    tables = cursor.fetchall()

    available_tables = {}
    print('Please choose a table:')

    for i, table in enumerate(tables, 1):
        table_name = table[0]

        # Skip the bridging table.
        if table_name == 'AssignedPilots': 
            continue

        print(f'{i}. {table_name}')
        available_tables[i] = table_name

    inp = prompt_for_valid_input(0, max(available_tables.keys()))
    if inp == 0:
        print("Returning to main menu...")
        return

    # Safe from SQL injections, since user provides a number, not the table name.
    sql(f'SELECT * FROM {table_name}')
    # TODO: Format the output when actual data is available.
    print(cursor.fetchall())


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
    1: ("View Table", view_table),
    2: ("Insert", insert_data),
    3: ("Search", search_data),
    4: ("Update", update_data),
    5: ("Delete", delete_data),
    6: ("Summary Statistics", choose_summary_statistics),
    7: ("Extra 1", extra1),
    8: ("Extra 2", extra2)
}


def main():
    create_tables()

    inp = None 
    while inp != 0:
        display_menu(options)

        inp = input('>> ')
        inp = verify_input(inp, min(options.keys()), max(options.keys()))
        if inp == None: 
            continue

        selected_option = options.get(inp)
        execute_selected_option = selected_option[1]()

    db.close()

    
if __name__ == '__main__':
    main()

