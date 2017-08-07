import os, json, traceback
import canvas_schema_table_list

print("Testing")

# This function should be called when seeking a list of Canvas table names
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

# This function opens the Canvas schema.json file (with a defalut directory if none given)
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
