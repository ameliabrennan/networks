# Functions for running Canvas API calls, via the CanvasDataCli, from within Python rather than the command line
# This can help with running the canvas_update.py script as a whole process, rather than needing to 
# Relies on Canvas secret credentials being within the user's system (sync requests will be rejected otherwise)
# Also relies on the config.js file existing, the default location refers to the location on Sarah's directory

import subprocess, os
import canvas_schema_tools
import tools_for_lists
import traceback

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

