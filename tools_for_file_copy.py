# Some tools for copying files
# made by Sarah as part of Canvas tasks July 2017, but potentially applicable for other tasks

import os

# This function copies one file to another, but skips the header
# It completes the task in one go (i.e. not line by line)
# Hence it will fail for very large files, or (of course) if the input file does not exist
# If successful it will copy input_file_name to output_file_name (except row one) and return True
# If errors encountered it will return False
# Last updated July 2017
def copy_file_quickly_noheader(input_file_name, output_file_name):
  result = False
  try:
    with open(input_file_name, 'r') as fin:
      data = fin.read().splitlines(True)
    with open(output_file_name, 'w') as fout:
      fout.writelines(data[1:])
    result = True
    return(result)
  except:
    return(result)

# This function copies one file to another, but skips the header
# It completes the task line by line
# Hence it will work better for very large files than the quick copy
# But it is slower
# If successful it will copy input_file_name to output_file_name (except row one) and return True
# If errors encountered it will return False
# Last updated July 2017
def copy_file_slowly_noheader(input_file_name, output_file_name):
  result = False
  try:
    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')
    line_count = 0
    for line in input_file:
      if(line_count == 0):
        print("\nSkipping header file")
      else:
        output_file.write(line)
        print(str(line_count))
      line_count += 1
    result = True
    return(result)
  except:
    return(result)
   
