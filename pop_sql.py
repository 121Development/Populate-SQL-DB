import mysql.connector
from mysql.connector import Error

# >>> YOUR DB INFO <<< #
host = "localhost"
user = "root"
password = "password"
database = "yourdatabasename"

# >>> SET BELOW ROUNDS VARIABLE TO 2 ROUNDS MORE THAN NUMBER OF LEVELS OF YOUR DB
# >>> PARENT TABLE, CHILD, CHILD OF CHILD ETC. EACH IS 1 LEVEL
rounds = 6

# Establish the connection and set cursor
try:
    conn = mysql.connector.connect(
        user=user, password=password, host=host, database=database)
    cursor = conn.cursor()
    print(f"\nSuccessfully connected to database {database}\n")
except Error as err:
    print(f"Error: '{err}'")

# Function to read passed query
def read_query(conn, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# Function to execute passed query
def execute_query(conn, query):
    try:
        cursor.execute(query)
        conn.commit()
    except Error as err:
        print(f"Error: '{err}'")

# Delete all data in all tables
def delete_data(conn, query):
    try:
        cursor.execute(query)
        conn.commit()
    except Error as err:
        return("Error")

# Loop to fetch all table names in DB
def get_all_table_names():
    sql = '''SHOW TABLES'''
    cursor.execute(sql)
    result = cursor.fetchall()
    table_names = [item for t in result for item in t] 
    return(table_names)

# Function to delete table data, takes variable rounds
def delete_table_data(rounds):
    n = 0
    while n < rounds:
        for name in table_names:
            delete_data(conn, f"DELETE FROM {name};")
        n += 1
    print("Sucessfully deleted all table data\n")

# CALLING FUNCTIONS
table_names = get_all_table_names()
delete_table_data(rounds)

# AFTER DELETION OF DATA STARTS INSERTION OF DATA HERE
print("Adding data to tables, check for Errors and fix them:")



# >>> CREATE YOUR DATASETS BELOW TO POPULATE TABLES 
# >>> REMEMBER TO EXECUTE / WRITE PARENT TABLES FIRST THEN CHILD AND CHILD OF CHILD
# >>> EXAMPLE OF VALUES FOR TABLE "foretag" AND EXECUTE FUNCTION
# >>> JUST COPY PASE THE BELOW FOR EACH TABLE WITH DATA YOU WANT

# >>> EXAMPLE - copy paste for each of your tables and adjust names between INSERT INTO ... VALUES and pop_...<<< 
# >>> columns in example are: foretagID(int), namn, orgNr, momsNr, gata, postNr, postOrt, kontaktPerson, email, telefon <<<
pop_foretag = """
INSERT INTO foretag VALUES
(1,"Bolaget AB", "556778-1422", "SE5567781422SE", "Agatan 1", "11235", "Stockholm", "Adam", "bolaget@bolaget.se", "0701234567");
"""
execute_query(conn, pop_foretag)
print("foretag")
# >>> END EXAMPLE <<<


# PRINTING ADDED DATA
print(f"\nData added to {len(table_names)} tables")
print("Printing table values:")

# PRINTS DATA FROM EACH TABLE FOR YOU TO CHECK THAT IT'S NOT EMPTY
for name in table_names:
    print(name, read_query(conn, f"SELECT * FROM {name}"))

# CLOSE CONN
cursor.close()
conn.close()