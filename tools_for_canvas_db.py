# A set of functions for Canvas Postgres database connections, as at August 14th 2017
# Make sure to include the most recent 'tools_for_db' module in the same folder as this file

import tools_for_db

# This function will connect to the canvas_current database, and returns a CURSOR if successful
# It requires a password and IP string (supplied to permitted users)
# Only permitted connections will receive a response
# Returns a cursor to canvas_current if successful
# Returns None if not successful
def connect_canvas_cur(password, host):
    cur = tools_for_db.db_connect_cursor(database_str="canvas_current", user_str="postgres", password_str=password, host_str=host)
    print_canvas_timestamp(cur)
    return cur

# This function will connect to the canvas_current database, and returns a CONNECTION if successful
# It requires a password and IP string (supplied to permitted users)
# Only permitted connections will receive a response
# Returns a connection to canvas_current if successful (useful for Pandas SQL dataframes)
# Returns None if not successful
def connect_canvas_conn(password, host):
    conn = tools_for_db.db_connect_conn(database_str="canvas_current", user_str="postgres", password_str=password, host_str=host)
    return conn

# This function prints the most recent update date for the Canvas Postgres copy
# It relies on the table canvas_postgres_copy_timestamp
# If it finds this table it prints the records in this (should just be one date)
# If errors are encountered it exits with an apology message
def print_canvas_timestamp(cur):
  try:
    timestamp_sql = "SELECT date_updated::date FROM canvas_postgres_copy_timestamp"
    cur.execute(timestamp_sql)
    result = cur.fetchall()
    print("\nLast Canvas Postgres copy made at:")
    print(result[0][0])
  except:
    print("Sorry, could not find canvas_postgres_copy_timestamp")