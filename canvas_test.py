import tools_for_db, tools_for_file_copy
import traceback, numpy, os

def table_row_count(table_name, cur, print_message=True):
  result = False
  try:
    sql_query = "SELECT count(*) FROM " + table_name + ";"
    result = tools_for_db.extract_query(sql_query, cur, print_messages=False)
    if(print_message==True):
      print("%s has %s rows\n" %(table_name, str(result[0][0])))
    return(result[0][0])
  except:
    traceback.print_exc()
    return(result)

def table_truncate(table_name, cur, print_message=True):
  result = False
  try:
    print("Truncating table %s" %table_name)
    sql_query = "TRUNCATE " + table_name + ";"
    result = True
    return(result)
  except:
    traceback.print_exc()
    return(result)

def db_print_table_rowcounts(cur):
  table_list = tools_for_db.return_tables_available(cur)
  for table_name in table_list:
    result = table_row_count(table_name[0], cur)

def table_import_data_from_text(cur, table_name, text_file_name):
  try:
    print("Copying %s into %s" %(file_name, table_name))
    sql_string = "COPY public." + table_name + " FROM '" + text_file_name + "' (FORMAT 'text', DELIMITER E'\\t', ENCODING 'UTF8');"
    print(sql_string)
  except:
    traceback.print_exc()
    return(result)  

def canvas_processing_part1_copy_text_files(input_directory, output_directory, table_list):
  successful_copies = []
  try:
    
    for table_name in table_list:
      print(table_name)
      input_file_name = input_directory + table_name + ".txt"
      output_file_name = output_directory + table_name + "_noheader.txt"
      print("Attempting copy from %s to %s" %(input_file_name, output_file_name))
      result = tools_for_file_copy.copy_file_noheader(input_file_name, output_file_name)
      if(result==True):
        successful_copies.append(table_name)
    
    return(successful_copies)
  except:
    traceback.print_exc()
    return(successful_copies)


def canvas_processing_part2_input_text_files(cur, text_file_directory, table_list):
  successful_copies = []
  try:    
    for table_name in table_list:
      print(table_name)
      text_file_name = output_directory + table_name + "_noheader.txt"
      print("Attempting copy from %s to %s" %(text_file_name, table_name))
      result = table_import_data_from_text(cur, table_name, text_file_name)
      if(result==True):
        successful_copies.append(table_name)
    
    return(successful_copies)
  except:
    traceback.print_exc()
    return(successful_copies)


cur = tools_for_db.connect_canvas_test_db_local("Robin")
#print_rows_in_tables_available(cur)
   

# this list of canvas table names does not include requests
canvas_table_name_list = ["account_dim", "assignment_dim", "assignment_fact", "course_dim", "enrollment_dim", "enrollment_fact", "enrollment_term_dim", "file_dim", "file_fact", "submission_dim"]

canvas_table_name_list = ["role_dim", "submission_fact", "user_dim"]

input_directory = os.path.normpath("E:/unpackedFiles_INPUT") + os.path.normpath("/")
print(input_directory)
output_directory = os.path.normpath("E:/unpackedFiles_OUTPUT") + os.path.normpath("/")
print(output_directory)

table_list_stage1 = canvas_table_name_list
table_list_stage2 = canvas_processing_part1_copy_text_files(input_directory, output_directory, table_list_stage1)
print("Files successfully copied:\n")
print(table_list_stage2)
text_file_directory = output_directory
### CALL FILE COPYING PART HERE
#table_list_stage3 = canvas_processing_part1_copy_text_files(cur, text_file_directory, table_list_stage2)




