import tools_for_db
import tools_for_file_copy
import tools_for_lists
import canvas_schema_tools
import traceback, numpy, os

def db_table_truncate(table_name, cur, print_message=True):
  result = False
  try:
    print("Truncating table %s" %table_name)
    sql_query = "TRUNCATE " + table_name + ";"
    result = True
    return(result)
  except:
    traceback.print_exc()
    return(result)


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
        print("Copying from %s to %s" %(text_file_name, table_name))
      result = db_table_import_text_to_table(cur, table_name, text_file_name)
      if(result==True):
        copy_count.append(table_name)    
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)


def db_table_import_text_to_table(cur, table_name, text_file_name, print_update=False):
  result = False
  try:
    if (print_update == True):
      print("Copying %s into %s" %(text_file_name, table_name))
    sql_string = "COPY public." + table_name + " FROM '" + text_file_name + "' (FORMAT 'text', DELIMITER E'\\t', ENCODING 'UTF8');"
    cur.execute(sql_string)
    result = True
    return(result)
  except:
    traceback.print_exc()
    return(result)  

def canvas_bulk_processing_truncate_tables(cur, table_list):
  truncate_count = []
  try:    
    for table_name in table_list:
      result = db_table_truncate(cur, table_name)
      if(result==True):
        truncate_count.append(table_name)    
    return(truncate_count)
  except:
    traceback.print_exc()
    return(truncate_count)


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
    return(result)
  except:
    traceback.print_exc()
    return(result)


### MAIN

#skip_list = ['requests', 'file_dim', 'quiz_question_answer_fact', 'wiki_page_dim']
skip_list = ['requests']
COPY_TEXT_FILES = True
raw_canvas_directory = os.path.normpath("H:/CanvasData/unpackedFiles") + os.path.normpath("/")
textfile_directory = os.path.normpath("E:/unpackedFiles_OUTPUT") + os.path.normpath("/")

# CONNECT TO DATABASE, NEED AUTOCOMMIT SETTING
# IMPROVE OPTIONS FOR MODIFICATION HERE
conn = tools_for_db.db_connect_conn(database_str="sarah_test", user_str="postgres", password_str="Robin", host_str="localhost")
conn.autocommit = True
cur = conn.cursor()
#cur = tools_for_db.connect_sarah_sandbox_db("Robin")

canvas_schema_table_list = initialise_canvas_schema_table_list("")
print("\n%s Tables found in Canvas schema.json" %str(len(canvas_schema_table_list)))
tools_for_lists.print_list(canvas_schema_table_list)

current_table_list = canvas_schema_table_list

# Important: remove files at this point, before proceeding
print("\n%s Tables to be excluded from processing:" %str(len(skip_list)))
tools_for_lists.print_list(skip_list)
current_table_list = tools_for_lists.remove_list_from_list(current_table_list, skip_list)
print("\n%s Tables to continue processing:" %str(len(current_table_list)))
tools_for_lists.print_list(current_table_list)

if (COPY_TEXT_FILES == True): 
  current_table_list = canvas_bulk_processing_copy_text_files_noheader(raw_canvas_directory, textfile_directory, current_table_list)
  print("\n%s Canvas files successfully copied across." %str(len(current_table_list)))
  tools_for_lists.print_list(current_table_list)

schema_sql_file = "H:/networks/canvas_schema_create.sql"
result = canvas_bulk_processing_run_schema_sql(cur, schema_sql_file)

if (result == True):

  db_canvas_table_list = initialise_db_canvas_table_list(cur, canvas_schema_table_list)
  print("\n%s Canvas tables found in current database." %str(len(db_canvas_table_list)))
  tools_for_lists.print_list(db_canvas_table_list)

  current_table_list = db_canvas_table_list

  current_table_list = canvas_bulk_processing_truncate_tables(cur, current_table_list)
  print("\n%s Canvas tables successfully truncated." %str(len(current_table_list)))

  current_table_list = canvas_bulk_processing_import_text_files_to_tables(cur, textfile_directory, current_table_list)
  print("\n%s Canvas tables were successfully copied across to the database." %str(len(current_table_list)))
  tools_for_lists.print_list(current_table_list)
  print("\n%s Canvas tables were successfully copied across to the database." %str(len(current_table_list)))
  print("\n%s Canvas file/s were asked to be excluded from processing:" %str(len(skip_list)))
  tools_for_lists.print_list(skip_list)

else:

  print("Could not run schema sql, please check and try again.")




