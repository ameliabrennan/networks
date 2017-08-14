import tools_for_db
import traceback, numpy, os


def canvas_create_date_table(cur, date_table_sql_file="H:/networks/canvas_schema_create.sql"):
  result = False
  try:
    cur.execute(open(date_table_sql_file, "r").read())
    result = True
    print("\nHave created canvas_postgres_copy_timestamp table.")
    return(result)
  except:
    traceback.print_exc()
    return(result)


### MAIN

# CONNECT TO DATABASE, NEED AUTOCOMMIT SETTING
# IMPROVE OPTIONS FOR CHOOSING A DIFFERENT DATABASE HERE
conn = tools_for_db.db_connect_conn(database_str="canvas_current", user_str="postgres", password_str="Robin", host_str="localhost")
conn.autocommit = True
cur = conn.cursor()
#cur = tools_for_db.connect_sarah_sandbox_db("Robin")

date_table_sql_file = "H:/networks/canvas_date_table_create.sql"
result = canvas_create_date_table(cur, date_table_sql_file)
