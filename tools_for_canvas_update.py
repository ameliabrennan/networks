## tools_for_canvas_update.py
# This module the functions necessary for Canvas Postgres databaes updates
# Call the 'run_canvas_update' function externally, to initiate a database update process
# Dependencies from within RMIT Studios: 
# SQL files in the same directory as the module: canvas_schema_create.sql, canvas_date_table_create.sql
# Python modules in the same directory: tools_for_db.py, tools_for_file_copy.py, tools_for_lists.py, tools_for_email.py
# Generic Python modueles: traceback, numpy, os, time, json, psycopg2

import tools_for_db
import tools_for_file_copy
import tools_for_lists
import tools_for_email
import traceback, numpy, os, time, json

# Function: run_canvas_update
# This is the main function to call to initiate a Canvas database update (from another Python file)
## EXAMPLE CALL
## import canvas_update
## canvas_textfile_directory = "H:/CanvasData/unpackedFiles"
## config_file_name = "H:/CanvasData" + os.path.normpath("/") + "config.js"
## skip_list = ['requests']
## RUN_SYNC = True
## COPY_TEXT_FILES = True
## database_textfile_directory = "E:/unpackedFiles_noheader"
## database_name = "sarah_sandbox"
## run_canvas_update(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory, database_name, config_file_name, email_recipients)
def run_canvas_update(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory, database_name, config_file_name, email_recipients=[]):
  
  start_time = time.asctime()
  print("Started process: ", str(time.asctime()))
  current_table_list = canvas_update_part1_textfiles(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory, config_file_name)
  if (current_table_list != False):
    current_table_list = canvas_update_part2_database(current_table_list, database_name, database_textfile_directory)
  else:
    print("Problems with process, stopped at: ", str(time.asctime()))

  if (current_table_list != False):
    current_result = canvas_update_part3_summary(current_table_list, skip_list, database_name, email_recipients, database_textfile_directory, start_time)    
    print("Finished process: ", str(time.asctime()))
  else:
    print("Problems with process, stopped at: ", str(time.asctime()))


def canvas_update_part1_textfiles(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory, config_file_name):
  result = False
  try:
    print("\n*** Canvas update part 1: text files ***")

    canvas_schema_table_list = fetch_canvas_schema_table_list("")
    print("\n%s Tables found in Canvas schema.json" %str(len(canvas_schema_table_list)))
    tools_for_lists.print_list(canvas_schema_table_list)

    current_table_list = canvas_schema_table_list

    # Important: remove skip_list items, before proceeding
    current_table_list = tools_for_lists.remove_list_from_list(current_table_list, skip_list)

    if (RUN_SYNC == True):
      print("Running SYNC")
      sync_result = run_canvas_sync(config_file_name)
      print(sync_result)
      if (sync_result == True):
        unpacked_table_list = run_canvas_unpack(current_table_list, config_file_name)
    else:
       print("Skipping SYNC")

    if (COPY_TEXT_FILES == True): 
      current_table_list = copy_text_files_in_list_noheader(canvas_textfile_directory, database_textfile_directory, current_table_list)
      print("\n%s Canvas text files successfully copied across." %str(len(current_table_list)))
      tools_for_lists.print_list(current_table_list)

    return(current_table_list)  

  except:
    traceback.print_exc()
    return(result)


# This function runs the multiple parts of a full Canvas duplication
def canvas_update_part2_database(current_table_list, database_name, database_textfile_directory):
  result = False
  try:

    print("\n*** Canvas update part 2: database ***")

    print("Attempting connection to database: %s" %database_name)

    cur = tools_for_db.db_connect_cursor_autocommit(database_str=database_name, user_str="postgres", password_str="Robin", host_str="localhost")
    
    current_result = run_canvas_schema_sql(cur)
   
    db_canvas_table_list = fetch_db_canvas_table_list(cur, current_table_list)
    print("\n%d Canvas tables found in current database." %len(db_canvas_table_list))
    tools_for_lists.print_list(db_canvas_table_list)

    current_table_list = db_canvas_table_list

    current_table_list = truncate_tables_in_list(cur, current_table_list)
    print("\n%d Canvas tables successfully truncated." %len(current_table_list))

    current_table_list = import_canvas_text_files_to_tables(cur, database_textfile_directory, current_table_list, print_update=True)

    current_result = run_date_table_sql(cur)
    if (current_result == True):
      print("Have successfully added timestamp")
    else:
      print("Problems with timestamp")

    cur.close()
    return(current_table_list)

  except:
    traceback.print_exc()
    cur.close()
    return(result)

# Function: canvas_update_part3_summary
# This function summarises the preceding Canvas update and sends an update email to the email_recipients list
def canvas_update_part3_summary(current_table_list, skip_list, database_name, email_recipients, database_textfile_directory, start_time):
  result = False
  try:
    finish_time = time.asctime()
    #report_file_name = database_textfile_directory +  os.path.normpath("/") + "canvas_update_report_" + str(time.asctime()).replace(" ", "_").replace(":", "_") + ".txt"    
    report_file_name = database_textfile_directory + "/" + "canvas_update_report_" + str(finish_time).replace(" ", "_").replace(":", "_") + ".txt"   
    report_file = open(report_file_name, 'w')

    tools_for_file_copy.print_write("%d tables were successfully updated from Canvas to Postgres database %s." %(len(current_table_list), database_name), report_file)

    tools_for_file_copy.print_write("\n\nUpdated tables:", report_file)
    for table_name in current_table_list:
      tools_for_file_copy.print_write("\n" + table_name, report_file)

    tools_for_file_copy.print_write("\n\nExcluded tables:", report_file)
    for table_name in skip_list:
      tools_for_file_copy.print_write("\n" + table_name, report_file)


    tools_for_file_copy.print_write("\n\nStart time: ", report_file)
    tools_for_file_copy.print_write(start_time, report_file)
    tools_for_file_copy.print_write("\nCompletion time: ", report_file)
    tools_for_file_copy.print_write(str(time.asctime()), report_file)

    tools_for_file_copy.print_write("\nDatabase name: %s" %database_name, report_file)
    print("Report file: %s" %report_file_name)

    report_file.close()

    if (len(email_recipients) >= 1):
      email_message = 'Canvas database updated: ' + database_name + ", " + str(finish_time)
      attach_files = []
      attach_files.append(report_file_name)
      email_result = tools_for_email.send_gmail_withattachments('sarahcanvasreports@gmail.com', 'H:\SARAH_MISC_RMIT_STUDIOS\sarahcanvas.txt', email_recipients, email_message, attach_files)

      result = email_result

    return(result)
  except:
    traceback.print_exc()
    return(result)

# This function should be called when seeking a list of Canvas table names from the json schema file
# It is a wrapper for the tasks of a) opening the json file and b) reading the table names
# It returns the list of table names found in the schema.json file in the canvas directory
# If errors are encountered it returns None.
def return_canvas_table_list(canvas_schema_directory=""):
  
  print("Attempting to fetch Canvas table list from schema.json...")
  
  try:
    schema_data = import_canvas_schema_from_json(canvas_schema_directory)
    canvas_table_list = read_canvas_schema_tables_recursively(schema_data, [])

    return(canvas_table_list)
  except:
    traceback.print_exc()
    return(None) 

# This function reads in the (complicated) Canvas data structure 
# and returns the list of unique table names. 
# The table names are hidden within lists of dictionaries and other varied
# types in the Canvas schema.json file. This function works recursively 
# to make sure it has read through the different levels of data for the 
# key word of 'tableName'. When it encounters this word in a tuple it adds
# the corresponding table name to the table_list object. 
# When it has finished looking through the data it returns the full populated
# table_list object, containing unique Canvas table names
def read_canvas_schema_tables_recursively(input_data, table_list, count=1):
  try:
    for k, v in input_data.items():
      if isinstance(v, dict):
        read_canvas_schema_tables_recursively(v, table_list, count)
      elif isinstance(v, str):  
        if(k == "tableName"):        
          table_list.append(v)
          count += 1
      elif isinstance(v, list):     
        for item in v:
          if isinstance(item, dict):
            read_canvas_schema_tables_recursively(item, table_list, count)    
    return(table_list)
  except:
    traceback.print_exc()
    return(None)

# This function opens the Canvas schema.json file (with a default directory if none given)
# It returns the data structure directly from the schema.json file: this is a nested 
# structure of lists, dictionaries, strings, etc. 
# It returns the full structure of data. 
# If any errors are encountered it returns None. 
def import_canvas_schema_from_json(canvas_schema_directory=""):
  try:
    if(canvas_schema_directory == ""):
      canvas_schema_directory = os.path.normpath("H:/CanvasData/dataFiles") 

    schema_file_name = canvas_schema_directory + os.path.normpath("/") + "schema.json"
    #print("\nREADING FROM SCHEMA FILE: %s" %schema_file_name)

    with open(schema_file_name) as schema_file:
      schema_data = json.load(schema_file)

    return(schema_data)
  except:
    traceback.print_exc()
    return(None)


def copy_text_files_in_list_noheader(canvas_textfile_directory, database_textfile_directory, table_list, print_update=False):
  copy_count = []
  try:    
    for table_name in table_list:
      input_file_name = canvas_textfile_directory + os.path.normpath("/") + table_name + ".txt"
      output_file_name = database_textfile_directory + os.path.normpath("/") + table_name + "_noheader.txt"
      if (print_update == True):
        print("Copying from %s to %s" %(input_file_name, output_file_name))   
      result = tools_for_file_copy.copy_file_noheader(input_file_name, output_file_name)
      if(result==True):
        copy_count.append(table_name)        
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)


def import_canvas_text_files_to_tables(cur, database_textfile_directory, table_list, print_update=False):
  copy_count = []
  try:    
    for table_name in table_list:
      text_file_name = database_textfile_directory + os.path.normpath("/") + table_name + "_noheader.txt"
      if (print_update == True):
        print("Copying from '%s'" %text_file_name)
        print("To '%s'" %table_name)
      result = tools_for_db.db_import_tabdelim_text_to_table(cur, table_name, text_file_name)
      if(result==True):
        copy_count.append(table_name)    
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)


def truncate_tables_in_list(cur, table_list):
  truncate_count = []
  try:    
    for table_name in table_list:
      result = tools_for_db.db_table_truncate(cur, table_name)
      if(result==True):
        truncate_count.append(table_name)    
    return(truncate_count)
  except:
    traceback.print_exc()
    return(truncate_count)


def fetch_canvas_schema_table_list(canvas_schema_directory=""):
  try:
    canvas_table_list = return_canvas_table_list(canvas_schema_directory)
    return(canvas_table_list)
  except:
    traceback.print_exc()
    return(None)


def fetch_db_canvas_table_list(cur, canvas_table_list):
  try:
    db_table_list = tools_for_db.return_tables_available(cur)
    db_canvas_table_list = []
    for table_name in canvas_table_list:
      result = tools_for_lists.check_for_element_in_list(db_table_list, table_name)
      if (result == True):
        db_canvas_table_list.append(table_name)
    return(db_canvas_table_list)
  except:
    traceback.print_exc()
    return(None)


def run_canvas_schema_sql(cur, schema_sql_file="H:/networks/canvas_schema_create.sql"):
  result = False
  try:
    cur.execute(open(schema_sql_file, "r").read())
    result = True
    print("\nHave created Canvas schema on database.")
    return(result)
  except:
    traceback.print_exc()
    return(result)

# This function runs the SQL to create a special table called canvas_postgres_copy_timestamp
# This table is a single row with a datestamp in it, useful for checking when the Canvas update was last run.
def run_date_table_sql(cur, date_table_sql_file="H:/networks/canvas_schema_create.sql"):
  result = False
  try:
    cur.execute(open(date_table_sql_file, "r").read())
    result = True
    print("\nHave created canvas_postgres_copy_timestamp table.")
    return(result)
  except:
    traceback.print_exc()
    return(result)


#### Functions for running Canvas API calls, via the CanvasDataCli, from within Python rather than the command line ####
# These functions can help with running the canvas_update.py script as a whole process
# They rely on Canvas secret credentials being within the user's system (sync requests will be rejected otherwise)
# Also relies on the config.js file. The default location refers to the location on Sarah's directory

# Function: run_canvas_sync
# This function runs the Canvas SYNC process by using the CanvasDataCli 'sync' command line argument
# It needs the Canvas API secrets to be included in the user system
# If the user does not have these secrets, the sync process will not run successfully
# Note that the Canvas sync process will fetch many, many zipped .gz files from Canvas and place them in the directory
# that is specified in the config.js file (in the default location given here)
# The sync process harvests the most up-to-date Canvas data, but the data is inside many zipped files (more than one per table)
# Hence, more work is needed after the sync process, to get the files ready for the database
# If the subprocess call returns a 0 (success), then the function returns True
# if any errors are encountered, it returns False
def run_canvas_sync(config_file_name):
  result = False
  try:
    if (config_file_name == ""):
      config_file_name = "H:/CanvasData" + os.path.normpath("/") + "config.js"
    print("config_file_name: ", config_file_name)
    sync_args = "canvasDataCli sync -c " + config_file_name
    print(sync_args)
    subprocess_result = subprocess.check_call(sync_args, shell=True)
    if (subprocess_result == 0):
      result = True
    return(result)
  except:
    return(result)


# Function: run_canvas_unpack_single_table
# This function unpacks a single Canvas table using the CanvasDataCli 'unpack' command line argument
# If the subprocess call returns a 0 (success), then the function returns True
# if any errors are encountered, it returns False
def run_canvas_unpack_single_table(table_name, config_file_name):
  result = False
  try:
    if (config_file_name == ""):
      config_file_name = "H:/CanvasData" + os.path.normpath("/") + "config.js"
    print("config_file_name: ", config_file_name)
    unpack_args = "canvasDataCli unpack -c " + config_file_name + " -f " + table_name
    print(unpack_args)
    subprocess_result = subprocess.check_call(unpack_args, shell=True)    
    if (subprocess_result == 0):
      result = True
    return(result)
  except:
    return(result)

# Function: run_canvas_unpack
# This function attempts to unpack a list of Canvas tables using looped calls to the 
# CanvasDataCli 'unpack' command line argument
# It loops through the list of names in 'table_list', and sends these to the function 'run_canvas_unpack_single_table'
# It will continue trying to unpack tables even if not all are successful: this way the unpack process can be selective
# and not dependent on all files having data
# It returns a list of the tables that were successfully unpacked (this will be [] if none were successful)
def run_canvas_unpack(table_list, config_file_name):
  result = False
  unpacked_table_list = []
  try:
    for table_name in table_list:
      unpack_result = run_canvas_unpack_single_table(table_name, config_file_name)
      if (unpack_result == True):
        unpacked_table_list.append(table_name)
    return(unpacked_table_list)
  except:
    traceback.print_exc()
    return(result)

