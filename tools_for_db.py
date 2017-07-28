import psycopg2, traceback, numpy

def db_connect(database_str, user_str, password_str, host_str):
    try:
        conn = psycopg2.connect(database=database_str, user=user_str, password=password_str, host=host_str)
        cur = conn.cursor()
        return cur
    except:
        return None

def connect_canvas_test_db():
    result = db_connect(database_str="Canvas_TEST", user_str="postgres", password_str="Robin", host_str="localhost")
    return result

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
