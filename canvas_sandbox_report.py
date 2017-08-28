## canvas_sandbox_report.py

import tools_for_email
import tools_for_db
import subprocess
import traceback
import time


# This function simply runs the whole SQL file qry_sandbox_report.sql as a command
# It is a quick way to run the SQL (prepared and tested in pgAdmin) for the sandbox file size report, 
# via Python, without recreating entirely in Python
# It uses a default location of the sql file, and the cursor to the database
# If successful, it runs the SQL for the sandbox report (including an export of a CSV file), and returns Trus
# If not successful, by encountering an error at any point, it returns False
def canvas_run_sandbox_report_sql(cur, sandbox_report_sql_file="H:/networks/qry_sandbox_report.sql"):
  result = False
  print("HERE - running SQL for sandbox report, from %s" %sandbox_report_sql_file)
  try:
    cur.execute(open(sandbox_report_sql_file, "r").read())
    result = True
    print("\nHave run SQL from %s" %(sandbox_report_sql_file))
    return(result)
  except:
    traceback.print_exc()
    return(result)

def return_sandbox_filecount_array(cur):
  result = False
  print("HERE - returning file size distribution")
  try:
    sql_string = "SELECT course_file_count FROM vw_sandbox_courses_with_counts;"
    cur.execute(sql_string)
    filecount_array = cur.fetchall()
    

### MAIN

# choose database name: canvas_current (located on Sarah's PC)
database_name = "canvas_current"

# connect to database with auto-commit cursor
cur = tools_for_db.db_connect_cursor_autocommit(database_str=database_name, user_str="postgres", password_str="Robin", host_str="localhost")

# call the function to run the sandbox report SQL, including an export of CSV file
sql_result = canvas_run_sandbox_report_sql(cur)

if (sql_result == True):
    ## Need to add better file information here, the file address should come from QGL process and not be hard coded
    sandbox_report_file = 'E:/canvas_sandbox_courses_with_filecounts_etc.csv'
    attachfiles = [sandbox_report_file]
    email_message = "Canvas sandbox report for today, generated at " + ' ' + str(time.asctime())
    email_result = tools_for_email.send_gmail_withattachments('sarahcanvasreports@gmail.com', 'H:\SARAH_MISC_RMIT_STUDIOS\sarahcanvas.txt', ['sarah.taylor@rmit.edu.au', 'pablo.munguia@rmit.edu.au'], email_message, attachfiles)


