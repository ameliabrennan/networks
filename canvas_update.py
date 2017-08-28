## canvas_update.py
# This module runs the Canvas Postgres databaes update for Sarah's PC, the "canvas_current" database
# This includes running the SYNC, copying the files, implememnting the schemea, and uploading the files
# However, it has a lot of overlap with the other canvas_update scripts and is hoped to be significantly
# modified and streamlined after first backing up via Github


import tools_for_db
import tools_for_file_copy
import tools_for_lists
import canvas_schema_tools
import canvas_api_call
import tools_for_email
import traceback, numpy, os
import time


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
    canvas_table_list = canvas_schema_tools.return_canvas_table_list(canvas_schema_directory)
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

def canvas_update_part1_textfiles(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory):
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
      sync_result = canvas_api_call.run_canvas_sync("")
      print(sync_result)
      if (sync_result == True):
        unpacked_table_list = canvas_api_call.run_canvas_unpack(current_table_list)
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

    if (current_result == True):
      
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

    return(current_table_list)

  except:
    traceback.print_exc()
    return(result)

def canvas_update_summary(current_table_list, skip_list, database_name):
  result = False
  try:
    tools_for_lists.print_list(current_table_list)
    
    print("\n%d Canvas tables were successfully copied across to database, as listed above." %len(current_table_list))
    print("Database name: %s" %database_name)

    email_message = 'Canvas database updated: ' + database_name + ', at ' + str(time.asctime()) 
    if (len(skip_list) >= 1):
      email_message += ', excluding: '
      for table_name in skip_list:
        email_message += table_name
    else:
      email_message += ', all tables included' 

    #email_recipients = ['sarah.taylor@rmit.edu.au', 'amelia.brennan@rmit.edu.au', 'amitoze.nandha@rmit.edu.au', 'peter.ryan2@rmit.edu.au']
    email_recipients = ['sarah.taylor@rmit.edu.au']
    email_result = tools_for_email.send_gmail_withattachments('sarahcanvasreports@gmail.com', 'H:\SARAH_MISC_RMIT_STUDIOS\sarahcanvas.txt', email_recipients, email_message, [])

    result = email_result
    return(result)
  except:
    traceback.print_exc()
    return(result)


### MAIN

### CHOICES
canvas_textfile_directory = "H:/CanvasData/unpackedFiles"

# common text file locations
textfile_options = {}
textfile_options['E'] = os.path.normpath("E:/unpackedFiles_noheader")
textfile_options['C'] = os.path.normpath("C:/scratch/CanvasData/unpackedFiles_noheader")
textfile_options['studentcopy'] = os.path.normpath("C:/scratch/canvasData/unpackedFiles_noheader")

skip_list = ['requests']
RUN_SYNC = True
COPY_TEXT_FILES = True
database_textfile_directory = "E:/unpackedFiles_noheader"
database_name = "canvas_current"

current_table_list = canvas_update_part1_textfiles(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory)
current_table_list = canvas_update_part2_database(current_table_list, database_name, database_textfile_directory)
current_result = canvas_update_summary(current_table_list, skip_list, database_name)

print("Finished process: ", str(time.asctime()))
 



