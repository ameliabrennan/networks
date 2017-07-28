# Canvas file copying workaround
# workaround for copying files from Canvas to E drive, without headers
# Postgres does not accept text files with tab delimiters (strange but true)
# This sript relies on the module tools_for_file_copying.py (written by Sarah July 2017)
# not an ideal scenario but works!!!

import os
import tools_for_file_copy


# This function copies an entire Canvas text file in one go, to a new file with no header
# It uses the module tools_for_file_copy.py, with the function 'copy_file_quickly_no_header'
# It will fail for very large files, or (of course) if the input file does not exist
# If successful it will copy a file with the same name as the table name in input_directory...
# out to txt file with the same name but no header, and a "_noheader" suffix, in output_directory...
# and return True
# If errors encountered it will return False
# Last updated July 2017
def copy_canvas_file_quickly(table_name, input_directory, output_directory):
  result = False
  input_file_name = input_directory + "/" + table_name + ".txt"
  output_file_name = output_directory + "/" + table_name + "_noheader.txt"
  print("Attempting quick copy from %s to %s" %(input_file_name, output_file_name))
  try:
    result = tools_for_file_copy.copy_file_quickly_noheader(input_file_name, output_file_name)
    return(result)
  except:
    print("Errors encountered")
    return(result)

# This function copies an entire Canvas text file LINE BY LINE, to a new file with no header
# It uses the module tools_for_file_copy.py, with the function 'copy_file_slowly_noheader'
# It will work more reliably for very large files (like 'requests'), but will be slower
# If successful it will copy a file with the same name as the table name in input_directory...
# out to txt file with the same name but no header, and a "_noheader" suffix, in output_directory...
# and return True
# If errors encountered it will return False
# Last updated July 2017
def copy_canvas_file_slowly_noheader(table_name, input_directory, output_directory):
  result = False
  input_file_name = input_directory + "/" + table_name + ".txt"
  output_file_name = output_directory + "/" + table_name + "_noheader.txt"
  print("Attempting quick copy from %s to %s" %(input_file_name, output_file_name))
  try:
    result = tools_for_file_copy.copy_file_slowly_noheader(input_file_name, output_file_name)
    return(result)
  except:
    print("Errors encountered")
    return(result)


## MAIN
# put canvas table name here
table_name = "enrollment_dim"

input_directory_name = os.path.normpath("H:/CanvasData/unpackedFiles/")
output_directory_name = os.path.normpath("E:/Imports_for_Canvas_TEST/")

result = copy_canvas_file_quickly(table_name, input_directory_name, output_directory_name)

