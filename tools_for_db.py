import psycopg2, traceback, numpy

def db_connect(database_str, user_str, password_str, host_str):
    try:
        conn = psycopg2.connect(database=database_str, user=user_str, password=password_str, host=host_str)
        cur = conn.cursor()
        print("Hello! Connected to database %s" %database_str)
        print_tables_available(cur)
        return cur
    except:
        traceback.print_exc()
        return None

# This function will connect to the canvas test database, but only for the local machine
# It needs a password passed in
def connect_canvas_test_db_local(password):
    result = db_connect(database_str="Canvas_TEST", user_str="postgres", password_str=password, host_str="localhost")
    return result


# This function will connect to the canvas test database
# It still requires a password and IP string (supplied to permitted users)
# Only permitted connections will actually respond though
def connect_canvas_test_db(password, host):
    result = db_connect(database_str="Canvas_TEST", user_str="postgres", password_str=password, host_str=host)
    return result

# This function lists the tables available from a database cursor
# It doesn't return anything but will exit on error
def print_tables_available(cur):
    try:
        sql_string = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
        cur.execute(sql_string)
        table_list = numpy.array(cur.fetchall())
        print("Tables available: ")
        print(table_list)
    except:
        traceback.print_exc()

def extract_table(table_name, cur):

    """
    This function extracts all records from a chosen database table, into an array.
    It does not restrict the fields or records selected from the table.
    If it encounters an error, it returns an empty array.
    Otherwise, it returns the selection in an array.
    Input: Table name string ('table_name'), cursor with connection to database.
    Ouput (when no error encountered): Array containing all the records and fields in the chosen table.
    Output (when error encountered): Empty array.
    """

    try:
        query = "SELECT * FROM public." + table_name + ";"

        # Extract table using SQL query
        print("Sending query:")
        print(query)

        cur.execute(query)

        # pass SQL result to output array named 'data_base'
        data_base = numpy.array(cur.fetchall())

        # if no errors have been encountered yet, it is safe to return the array
        print('Array size: ', data_base.shape)
        return data_base

    except:
        # if any errors are encountered, an empty array is returned
        traceback.print_exc()
        print('Error encountered extracting %s, will return empty array.' %table_name)
        return []

def extract_query(sql_query, cur):

    """
    This function extracts a query from a database, into an array.
    If it encounters an error, it returns an empty array.
    Otherwise, it returns the selection in an array.
    Input: SQL string, cursor with connection to database.
    Ouput (when no error encountered): Array containing all the query result.
    Output (when error encountered): Empty array.
    """

    try:
        # Extract SQL query
        print("Sending query:")
        print(sql_query)

        cur.execute(sql_query)

        # pass SQL result to output array named 'data_base'
        data_base = numpy.array(cur.fetchall())

        # if no errors have been encountered yet, it is safe to return the array
        print('Array size: ', data_base.shape)
        return data_base

    except:
        # if any errors are encountered, an empty array is returned
        traceback.print_exc()
        print('Error encountered extracting %s, will return empty array.' %sql_query)
        return []
