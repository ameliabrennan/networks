import tools_for_db
import tools_for_file_copy
import tools_for_lists
import canvas_schema_tools
import traceback, numpy, os


def canvas_bulk_processing_copy_text_files_noheader(input_directory, output_directory, table_list, print_update=False):
  copy_count = []
  try:    
    for table_name in table_list:
      input_file_name = input_directory + table_name + ".txt"
      output_file_name = output_directory + table_name + "_noheader.txt"
      if (print_update == True):
        print("Copying from %s to %s" %(input_file_name, output_file_name))   
      result = tools_for_file_copy.copy_file_noheader(input_file_name, output_file_name)
      if(result==True):
        copy_count.append(table_name)        
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)


def canvas_bulk_processing_import_text_files_to_tables(cur, text_file_directory, table_list, print_update=False):
  copy_count = []
  try:    
    for table_name in table_list:
      text_file_name = text_file_directory + table_name + "_noheader.txt"
      if (print_update == True):
        print("Copying from '%s'" %(os.path.basename(text_file_name)))
        print("To '%s'" %table_name)
      result = tools_for_db.db_import_tabdelim_text_to_table(cur, table_name, text_file_name)
      if(result==True):
        copy_count.append(table_name)    
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)


def canvas_bulk_processing_truncate_tables(cur, table_list):
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

def initialise_canvas_schema_table_list(canvas_schema_directory=""):
  try:
    canvas_table_list = canvas_schema_tools.return_canvas_table_list(canvas_schema_directory)
    return(canvas_table_list)
  except:
    traceback.print_exc()
    return(None)

def initialise_db_canvas_table_list(cur, canvas_table_list):
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

def canvas_bulk_processing_run_schema_sql(cur, schema_sql_file="H:/networks/canvas_schema_create.sql"):
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

# This function runs the multiple parts of a full Canvas duplication
def run_canvas_duplication(cur, raw_canvas_directory, textfile_direction, skip_list, COPY_TEXT_FILES):
  result = False
  try:
    canvas_schema_table_list = initialise_canvas_schema_table_list("")
    print("\n%s Tables found in Canvas schema.json" %str(len(canvas_schema_table_list)))
    tools_for_lists.print_list(canvas_schema_table_list)

    current_table_list = canvas_schema_table_list

    # Important: remove skip_list items at this point, before proceeding
    current_table_list = tools_for_lists.remove_list_from_list(current_table_list, skip_list)

    if (COPY_TEXT_FILES == True): 
      current_table_list = canvas_bulk_processing_copy_text_files_noheader(raw_canvas_directory, textfile_directory, current_table_list)
      print("\n%s Canvas text files successfully copied across." %str(len(current_table_list)))
      tools_for_lists.print_list(current_table_list)

    db_canvas_table_list = initialise_db_canvas_table_list(cur, canvas_schema_table_list)
    print("\n%s Canvas tables found in current database." %str(len(db_canvas_table_list)))
    tools_for_lists.print_list(db_canvas_table_list)

    current_table_list = db_canvas_table_list

    current_table_list = canvas_bulk_processing_truncate_tables(cur, current_table_list)
    print("\n%s Canvas tables successfully truncated." %str(len(current_table_list)))

    current_table_list = canvas_bulk_processing_import_text_files_to_tables(cur, textfile_directory, current_table_list, print_update=True)

    print("\n%s Canvas tables were successfully copied across to the database:" %str(len(current_table_list)))
    tools_for_lists.print_list(current_table_list)
    print("\n%s Canvas tables were successfully copied across to the database, listed above." %str(len(current_table_list)))
    print("\n%s Canvas file/s were asked to be excluded from processing:" %str(len(skip_list)))
    tools_for_lists.print_list(skip_list)

    result = True
    return(result)

  except:
    return(result)

### MAIN
raw_canvas_directory = os.path.normpath("H:/CanvasData/unpackedFiles") + os.path.normpath("/")

schema_sql_file = "H:/networks/canvas_schema_create.sql"
date_table_sql_file = "H:/networks/canvas_date_table_create.sql"

textfile_options = {}
textfile_options['E'] = os.path.normpath("E:/unpackedCanvasFiles") + os.path.normpath("/")
textfile_options['C'] = os.path.normpath("C:/scratch/CanvasData/unpackedFiles_noheader" + os.path.normpath("/"))

cur = tools_for_db.db_connect_cursor_autocommit(database_str="sarah_sandbox", user_str="postgres", password_str="Robin", host_str="localhost")

schema_result = canvas_bulk_processing_run_schema_sql(cur, schema_sql_file)

# CHOICES HERE
skip_list = ['requests']
COPY_TEXT_FILES = False
textfile_directory = textfile_options['E']

if (schema_result == True):
  duplication_result = run_canvas_duplication(cur, raw_canvas_directory, textfile_directory, skip_list, COPY_TEXT_FILES)
else:
  print("Could not run Canvas schema creation, could not proceed with copying files. Please check %s and try again." %schema_sql_file)

if (duplication_result == True):
  result = canvas_create_date_table(cur, date_table_sql_file)
  timestamp_sql = "SELECT date_updated::date FROM canvas_postgres_copy_timestamp"
  cur.execute(timestamp_sql)
  result = cur.fetchall()
  print("Timestamped as:")
  print(result[0][0])
  cur.close()
else:
  print("Errors encountered with Canvas duplication, new timestamp not created.")
