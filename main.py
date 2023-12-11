import sqlite3
import random
import pandas
from datetime import datetime
from my_logger import d, i, w, e

# Define a very large "number".
INFINITY = float('inf')

# Shortcuts for using SQL.
db = sqlite3.connect('airline.db') 
cursor = db.cursor()
sql = lambda query, params=(): cursor.execute(query, params)


def verify_input(inp, lower_bound, upper_bound):
    try:
        inp = int(inp)
        if (inp < lower_bound) or (inp > upper_bound): 
            raise IndexError
        return inp
    except ValueError:
        print(f'ERROR: "{inp}" is not an integer.', end=' ')
    except IndexError:
        print(f'ERROR: {inp} is is out of range.', end=' ')

    print('No data has been saved.')
    return None


def prompt_for_valid_input(lower_bound, upper_bound):
    while True:
        inp = input(' >>> ')
        inp = verify_input(inp, lower_bound, upper_bound)
        if inp == None:
            continue
        else:
            break
    return inp


def create_tables():
    # Create table Aircraft.
    sql('''
    CREATE TABLE IF NOT EXISTS Aircraft (
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
        origin TEXT,
        destination TEXT,
        departureTime INT,  -- UNIX time, DATETIME is not supported.
        landingTime INT,
        FOREIGN KEY (aircraftID) REFERENCES Aircraft (aircraftID) ON UPDATE CASCADE)
    ''')

    # Create table Pilots.
    sql('''
    CREATE TABLE IF NOT EXISTS Pilots (
        pilotID INT PRIMARY KEY,
        firstName TEXT,
        surname TEXT,
        dob INT)
    ''')

    # Create table AssignedPilots.
    sql('''
    CREATE TABLE IF NOT EXISTS AssignedPilots (
        pilotID INT,
        flightID INT,
        PRIMARY KEY (pilotID, flightID),
        FOREIGN KEY (pilotID) REFERENCES Pilots(pilotID) ON UPDATE CASCADE,
        FOREIGN KEY (flightID) REFERENCES Flights(flightID) ON UPDATE CASCADE)
    ''')

    db.commit()


def display_menu(options):
    print('\nAvailable options:')
    for key, value in sorted(options.items()):
        print(f'{key}. {value[0]}')


def quit_app():
    print("Thank you for using AirlineDB!")
    return


def select_table_name(tables):
    available_tables = {}
    print('Please choose a table:')

    for i, table in enumerate(tables, 1):
        table_name = table[0]

        print(f'{i}. {table_name}')
        available_tables[i] = table_name

    inp = prompt_for_valid_input(0, max(available_tables.keys()))
    if inp == 0:
        print("Returning to main menu...")
        return None
    else:
        return available_tables[inp]


def view_table():
    sql('SELECT name FROM sqlite_master WHERE type="table"')    
    tables = cursor.fetchall()
    table_name = select_table_name(tables)

    if table_name == None:
        return

    # Safe from SQL injections, since the user provides a number, not the table name.
    sql(f'SELECT * FROM {table_name}')

    rows = cursor.fetchall()
    columns = [ column[0] for column in cursor.description ]

    # Create a DataFrame from the rows and columns.
    dataframe = pandas.DataFrame(rows, columns=columns)
    # Start numbering rows from 1 instead of 0.
    dataframe.index = range(1, len(dataframe) + 1)

    print(dataframe)


def convert_to_unix_time(inp):
    try:
        # Ensure that the format is correct.
        valid_datetime = datetime.strptime(inp, '%d/%m/%Y %H:%M')
        # Convert to UNIX time (the number of seconds since January 1, 1970).
        unix_time = int(valid_datetime.timestamp())
        if unix_time < 0:
            raise ValueError

        return unix_time
    except ValueError:
        return None


def insert_data():
    sql('SELECT name FROM sqlite_master WHERE type="table"')    
    tables = cursor.fetchall()
    table_name = select_table_name(tables)

    # Query for table schema.
    sql(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()

    # Query for foreign keys in the table.
    sql(f'PRAGMA foreign_key_list({table_name})')
    foreign_keys_info = cursor.fetchall()
    # Create a dictionary to map foreign key columns to their referenced tables and columns
    # (column 3 contains the foreign key column name, column 2 the referenced table, column 4 the referenced column)
    foreign_key_references = { fk_info[3]: (fk_info[2], fk_info[4]) for fk_info in foreign_keys_info }

    # Holds the input values to be inserted in the SQL query.
    values_to_be_inserted = []

    for column in columns:
        # Column format: (cid, name, type, notnull, dflt_value, pk).
        _, column_name, column_type, column_notnull, _, column_is_pk = column
        # Make column type lowercase.
        column_type = column_type.lower()

        input_is_valid = False

        # If the column is a primary key.
        # All primary keys (unless also a FK) are auto generated random integers.
        if (column_is_pk) and (column_name not in foreign_key_references):
            while (True):
                # TODO: Change back, for testing purposes only.
                generated_primary_key = random.randint(1, 100)
                # generated_primary_key = random.randint(1000000000, 9999999999)
                sql(f'SELECT {column_name} FROM {table_name}')
                # Flatten the list of fetched tuples.
                primary_keys = { key[0] for key in cursor.fetchall() }
                if generated_primary_key in primary_keys:
                    print('Congratulations! You have successfully generated a non-unique 10 digit primary key.')
                    print('Please consider buying a lottery ticket.')
                else:
                    # To be added to the `values_to_be_inserted` list later.
                    inp = generated_primary_key
                    input_is_valid = True
                    break

        if not input_is_valid:
            print(f'Please enter "{column_name}"', end='')

        is_first_attempt = True
        while (not input_is_valid):
            # Handle dates and time.
            if (column_name == 'dob') or (column_name.endswith("Time")):
                if is_first_attempt:
                    # DOB will also include `hh:mm`, however the user can just enter `00:00` or anything else.
                    print(' (exactly "DD/MM/YYYY hh:mm" or -1 for NULL).')
                is_first_attempt = False

                inp = input(" >>> ")

                # Check if -1 has been entered.
                try:
                    inp = int(inp)
                    if (inp == -1):
                        # Check if the value can be assigned NULL.
                        if not column_notnull:
                            inp = None
                            input_is_valid = True
                        else:
                            print(f'ERROR: "{column_name}" cannot be NULL. No data has been saved.')
                            input_is_valid = False
                    else:
                        print("ERROR: Invalid date format. No data has been saved.")
                        input_is_valid = False
                # Otherwise handle the entered date.
                except ValueError:
                    inp = convert_to_unix_time(inp)
                    if inp == None:
                        print("ERROR: Invalid date format. No data has been saved.")
                        input_is_valid = False
                    else:
                        input_is_valid = True

            # Handle `INTEGER` data type.
            # Account for both "INT" and "INTEGER", same with "BOOL".
            elif column_type.startswith('int'):
                # Hints are only displayed on the first attempt.
                if is_first_attempt:
                    print(' (or -1 for NULL).')
                is_first_attempt = False

                inp = prompt_for_valid_input(-1, INFINITY)

                if (inp == -1):
                    # Check if the value can be assigned NULL.
                    if not column_notnull:
                        inp = None
                        input_is_valid = True
                    else:
                        print(f'ERROR: "{column_name}" cannot be NULL. No data has been saved.')
                        input_is_valid = False
                else:
                    input_is_valid = True

            # Handle `BOOLEAN` data type.
            elif column_type.startswith('bool'):
                print(' (1 - TRUE, 0 - FALSE).')
                inp = prompt_for_valid_input(0, 1)
                input_is_valid = True
                
            # Handle `TEXT` data type.
            else:
                if is_first_attempt:
                    print(" (or -1 for NULL).")
                is_first_attempt = False

                inp = input(' >>> ')

                # Check if -1 has been entered.
                try:
                    inp = int(inp)
                    if (inp == -1):
                        # Check if the value can be assigned NULL.
                        if not column_notnull:
                            inp = None
                            input_is_valid = True
                        else:
                            print(f'ERROR: "{column_name}" cannot be NULL. No data has been saved.')
                            input_is_valid = False
                    else:
                        inp = str(inp)
                        input_is_valid = True
                # Any other input is valid, since it is a string.
                except ValueError:
                    input_is_valid = True

            # Check if the column is a foreign key and validate the input.
            if column_name in foreign_key_references:
                referenced_table, referenced_column = foreign_key_references[column_name]
                sql(f'SELECT EXISTS(SELECT 1 FROM {referenced_table} WHERE {referenced_column} = ?)', (inp,))
                exists = cursor.fetchone()[0]
                if not exists:
                    print(f'ERROR: "{inp}" does not exist in referenced table "{referenced_table}".')
                    input_is_valid = False
                else:
                    input_is_valid = True


        values_to_be_inserted.append(inp)

    # Create a string of '?' (placeholders).
    placeholders = ', '.join(['?'] * len(values_to_be_inserted))
    # Construct the column names string.
    column_names = ', '.join(column[1] for column in columns)

    try:
        sql(f'INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})', values_to_be_inserted)
    except Exception as e:
        print(f'ERROR: {e}. Please try again.')

    db.commit()


def search_data():
    pass


def update_data():
    pass


def delete_data():
    pass


def show_summary_statistics():
    # Total number of flights.
    sql('SELECT COUNT(*) FROM Flights')
    total_flights = cursor.fetchone()[0]
    print(f"Total number of flights: {total_flights}")

    # Average number of passengers per flight.
    sql('SELECT AVG(numOfPassengers) FROM Flights')
    avg_passengers = cursor.fetchone()[0]
    print(f"Average number of passengers per flight: {avg_passengers:.2f}")

    # Average flight duration.
    # Query to calculate the total sum of flight durations.
    sql('''
        SELECT SUM(landingTime - departureTime)
        FROM Flights
        WHERE departureTime IS NOT NULL AND landingTime IS NOT NULL
    ''')
    total_duration = cursor.fetchone()[0]

    # Query to count the number of flights with valid departure and landing times.
    sql('''
        SELECT COUNT(*)
        FROM Flights
        WHERE departureTime IS NOT NULL AND landingTime IS NOT NULL
    ''')
    total_flights = cursor.fetchone()[0]

    if (total_flights > 0) and (total_duration is not None):
        average_duration = total_duration / total_flights
        # Convert average duration from seconds to a more readable format.
        hours, remainder = divmod(average_duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Average flight time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
    else:
        print("No valid data available to calculate average flight time.")


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
    6: ("Summary Statistics", show_summary_statistics),
    7: ("Extra 1", extra1),
    8: ("Extra 2", extra2)
}


def main():
    create_tables()

    inp = None 
    while inp != 0:
        display_menu(options)

        inp = input(' >> ')
        inp = verify_input(inp, min(options.keys()), max(options.keys()))
        if inp == None: 
            continue

        selected_option = options.get(inp)
        execute_selected_option = selected_option[1]()

    db.close()

    
if __name__ == '__main__':
    main()

