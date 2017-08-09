# Some tools for copying files
# made by Sarah as part of Canvas tasks July 2017, but potentially applicable for other tasks

import os, traceback, pathlib

# This function copies one file to another, but skips the header
# It completes the task line by line
# Hence it will work better for very large files than the quick copy
# But it is slower
# If successful it will copy input_file_name to output_file_name (except row one) and return True
# If errors encountered it will return False
# Last updated July 2017 by Sarah
def copy_file_noheader(input_file_name, output_file_name):
  result = False
  print(input_file_name)
  try:
    input_file = open(input_file_name, 'r', encoding='utf8')
    output_file = open(output_file_name, 'w', encoding='utf8')
    line_count = 0
    for line in input_file:
      if(line_count == 0):
        print("\t %sSkipping header file" %input_file_name)
      else:
        output_file.write(line)
        if((line_count % 1000) == 0):
          print("\t %s copying row %s" %(input_file_name, str(line_count)))
      line_count += 1
    result = True
    return(result)
  except:
    traceback.print_exc()
    print("Could not copy file %s\n" %input_file_name)
    return(result)

# This function prints the contents of a file to screen, one line at a time. 
# It doesn't return anything, it is just a check.
# It exits if an error is encountered.   
def print_file_content(input_file_name, limit_rows=30):
  print(input_file_name)
  try:
    input_file = open(input_file_name, 'r')
    line_num = 0
    for line in input_file:
      if (line_num <= limit_rows):
        print(line)
      line_num += 1
    return
  except:
    traceback.print_exc()
    print("Could not print file %s\n" %input_file_name)
    return

