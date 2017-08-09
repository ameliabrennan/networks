import tools_for_db, tools_for_file_copy
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

def db_table_import_data_from_text(cur, table_name, text_file_name):
  try:
    print("Copying %s into %s" %(file_name, table_name))
    sql_string = "COPY public." + table_name + " FROM '" + text_file_name + "' (FORMAT 'text', DELIMITER E'\\t', ENCODING 'UTF8');"
    print(sql_string)
  except:
    traceback.print_exc()
    return(result)  

def canvas_processing_part1_copy_text_files(input_directory, output_directory, table_list):
  copy_count = []
  try:    
    for table_name in table_list:
      print(table_name)
      input_file_name = input_directory + table_name + ".txt"
      output_file_name = output_directory + table_name + "_noheader.txt"
      print("Copying from %s to %s" %(input_file_name, output_file_name))
      result = tools_for_file_copy.copy_file_noheader(input_file_name, output_file_name)
      if(result==True):
        copy_count.append(table_name)        
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)


def canvas_processing_part2_input_text_files(cur, text_file_directory, table_list):
  copy_count = []
  try:    
    for table_name in table_list:
      print(table_name)
      text_file_name = output_directory + table_name + "_noheader.txt"
      print("Attempting copy from %s to %s" %(text_file_name, table_name))
      result = db_table_import_data_from_text(cur, table_name, text_file_name)
      if(result==True):
        copy_count.append(table_name)    
    return(copy_count)
  except:
    traceback.print_exc()
    return(copy_count)

def check_for_element_in_list(input_list, search_item):
  result = False
  try:
    for item in input_list:
      if item == search_item:
        result = True
    return(result)
  except:
    traceback.print_exc()
    return(None)

def print_list(input_list, str_prefix="", str_suffix=""):
  try:
    for item in input_list:
      print(str_prefix, str(item), str_suffix)
    return
  except:
    traceback.print_exc()
    return

def remove_item_from_list(input_list, remove_item="requests"):
  try:
    for item in input_list:
      if item == remove_item:
        input_list.remove(item)
    return(input_list)
  except:
    traceback.print_exc()
    return(None)

def initialise_canvas_schema_table_list(exclude_requests=True, canvas_schema_directory=""):
  try:
    canvas_table_list = canvas_schema_tools.return_canvas_table_list(canvas_schema_directory)
    if (exclude_requests == True):
      canvas_table_list = remove_item_from_list(canvas_table_list, "requests")
    return(canvas_table_list)
  except:
    traceback.print_exc()
    return(None)

def initialise_db_canvas_table_list(cur, canvas_table_list):
  try:
    db_table_list = tools_for_db.return_tables_available(cur)

    db_canvas_table_list = []
    for table_name in canvas_table_list:
      result = check_for_element_in_list(db_table_list, table_name)
      if (result == True):
        db_canvas_table_list.append(table_name)
    return(db_canvas_table_list)
  except:
    traceback.print_exc()
    return(None)

def message_about_requests(exclude_requests):
  try:
    if (exclude_requests == True):
      result = "Note that requests table IS EXCLUDED from current processing"
    else:
      result = "Note that requests table is NOT excluded from current processing"
    return(result)
  except:
    traceback.print_exc()

### MAIN

REQUESTS_EXCLUDE = True
input_directory = os.path.normpath("H:/CanvasData/unpackedFiles") + os.path.normpath("/")
output_directory = os.path.normpath("E:/unpackedFiles_OUTPUT") + os.path.normpath("/")

cur = tools_for_db.connect_canvas_test_db_local("PASSWORD HERE")

canvas_schema_table_list = initialise_canvas_schema_table_list(exclude_requests=REQUESTS_EXCLUDE)
print("\n%sTables found in Canvas schema.json" %str(len(canvas_schema_table_list)))
print_list(canvas_schema_table_list)
print(message_about_requests(REQUESTS_EXCLUDE))

db_canvas_table_list = initialise_db_canvas_table_list(cur, canvas_schema_table_list)
print("\n%s Canvas tables found in current database." %str(len(db_canvas_table_list)))
print_list(db_canvas_table_list)
print(message_about_requests(REQUESTS_EXCLUDE))

table_list_stage1 = canvas_schema_table_list
table_list_stage2 = canvas_processing_part1_copy_text_files(input_directory, output_directory, table_list_stage1)
#print("Files successfully copied:\n")
print_list(table_list_stage2)
#text_file_directory = output_directory
### CALL FILE COPYING PART HERE
#table_list_stage3 = canvas_processing_part1_copy_text_files(cur, text_file_directory, table_list_stage2)




