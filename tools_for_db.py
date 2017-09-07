# A set of general-purpose database connection functions
# Mostly for use with PostgreSQL although some functions are more generic

import psycopg2, traceback, numpy, os

# This function attempts to connect to a PostgreSQL database
# It returns a CURSOR if successful
# Also prints a list of available tables
# Returns None if not successful
def db_connect_cursor(database_str, user_str, password_str, host_str):
  try:
    conn = psycopg2.connect(database=database_str, user=user_str, password=password_str, host=host_str)
    cur = conn.cursor()
    db_print_tables_available_with_rowestimates(cur)
    print("\nHello!")
    print("Successfully connected to database '%s' with a cursor object." %database_str)
    print("Don't forget to use cur.close() when you are finished. Thankyou.")
    return cur
  except:
    traceback.print_exc()
    return None

# This function connects to a database and returns a CONNECTION rather than a cursor
# This is useful for some tasks, particularly the Pandas SQL to dataframe module, and for autocommit settings
# Returns None if not successful
def db_connect_conn(database_str, user_str, password_str, host_str):
  try:
    conn = psycopg2.connect(database=database_str, user=user_str, password=password_str, host=host_str)
    print("\nHello!")
    print("Successfully connected to database '%s' with a connection object." %database_str)
    print("You will need to use a CURSOR to find out more about the database contents.")
    print("But you can use the Python Pandas 'read_sql' function with the connection.")
    print("Don't forget to use conn.close() when you are finished. Thankyou.")
    return(conn)
  except:
    traceback.print_exc()
    return None


# This function will connect a local database AND set the cursor to autocommit
# Autocommit means that changes cannot be rolled back
# This is helpful when running big updates like the Canvas Postgres copy, but is too risky for general querying ,it should not be a default
def db_connect_cursor_autocommit(database_str="sarah_sandbox", user_str="postgres", password_str="", host_str="localhost"):
  try:
    conn = db_connect_conn(database_str=database_str, user_str=user_str, password_str=password_str, host_str=host_str)
    conn.autocommit = True
    print("\nSetting connection object autocommit to True.")
    cur = conn.cursor()
    return(cur)
  except:
    traceback.print_exc()
    return None

# This function lists the tables available from a database cursor
# It doesn't return anything but will exit on error
def print_tables_available(cur):
  try:
    table_list = return_tables_available(cur)
    print("\nTables available are as follows: \n")
    for item in table_list:
      print(item)
  except:
    traceback.print_exc()

# This function RETURNS the tables available from a database cursor
# It will return False if an error encountered, or an array of table names if no error encountered
def return_tables_available(cur):
  result = False
  try:
    sql_string = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
    cur.execute(sql_string)
    table_list = numpy.array(cur.fetchall())
    for item in table_list:
      print(item)
    return(table_list)
  except:
    traceback.print_exc()
    return(result)

# This function RETURNS the tables available from a Postgres database cursor, along with ESTIMATED row counts
# It will return False if an error encountered, or an array of table names if no error encountered
def db_print_tables_available_with_rowestimates(cur):
  try:
    sql_string = "select relname, reltuples from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
    cur.execute(sql_string)
    #table_list = numpy.array(cur.fetchall())
    table_list = cur.fetchall()
    print("\nTables available, with estimated row counts, are as follows: \n")
    for item in table_list:
      print("%s (%s)" %(item[0], str(int(item[1]))))
    print("\nNote: row counts are estimates only")
  except:
    traceback.print_exc()


# This function extracts all records from a chosen database table, into an array.
# It does not restrict the fields or records selected from the table.
# If it encounters an error, it returns an empty array.
# Otherwise, it returns the selection in an array.
# Input: Table name string ('table_name'), cursor with connection to database.
# Ouput (when no error encountered): Array containing all the records and fields in the chosen table.
# Output (when error encountered): Empty array.
def db_extract_table_to_array(table_name, cur):
  try:
    query = "SELECT * FROM public." + table_name + ";"
    cur.execute(query)
    data_base = numpy.array(cur.fetchall())
    return data_base
  except:
    print(query)
    traceback.print_exc()
    print('Error encountered extracting %s, will return empty array.' %table_name)
    return []

# This function extracts a query from a database, into an array.
# If it encounters an error, it returns an empty array.
# Otherwise, it returns the selection in an array.
# Input: SQL string, cursor with connection to database.
# Ouput (when no error encountered): Array containing all the query result.
# Output (when error encountered): Empty array.
def db_extract_query_to_array(sql_query, cur, print_messages=True):    
  try:
    # Extract SQL query
    if(print_messages==True):
      print("Sending query:")
      print(sql_query)

    cur.execute(sql_query)

    data_base = numpy.array(cur.fetchall())

    # if no errors have been encountered yet, it is safe to return the array
    if(print_messages == True):
      print('Array size: ', data_base.shape)

    return(data_base)

  except:
    # if any errors are encountered, an empty array is returned
    traceback.print_exc()
    print('Error encountered extracting %s, will return empty array.' %sql_query)
    return []

# This function truncates a given table
# Remember that 'truncate' is a euphemism for 'delete all rows'!
# Hence, use with care
# Returns True if successful, False if not successful
# Note: deletions will only be visible immediately if cursor is set to autocommit
def db_table_truncate(cur, table_name, print_update=False):
  result = False
  try:
    if (print_update == True):
      print("Truncating %s" %table_name)
    sql_string = "TRUNCATE TABLE public." + table_name + ";"
    cur.execute(sql_string)
    result = True
    return(result)
  except:
    traceback.print_exc()
    return(result)  

# This function imports a tab delimited text file (text_file_name) to a Postgres table (table_name)
# Returns True if successful
# Returns False if not successful
# It does not truncate beforehand: it is up to the user to decide if this is appropriate
def db_import_tabdelim_text_to_table(cur, table_name, text_file_name, print_update=False):
  result = False
  try:
    if (print_update == True):
      print("Copying %s into %s" %(os.path.basename(text_file_name), table_name))
    sql_string = "COPY public." + table_name + " FROM '" + text_file_name + "' (FORMAT 'text', DELIMITER E'\\t', ENCODING 'UTF8');"
    cur.execute(sql_string)
    result = True
    return(result)
  except:
    traceback.print_exc()
    return(result)  