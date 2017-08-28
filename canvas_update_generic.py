import canvas_update

### MAIN

### CHOICES
canvas_textfile_directory = "H:/CanvasData/unpackedFiles"
config_file_name = "H:/CanvasData" + os.path.normpath("/") + "config.js"

# common text file locations
textfile_options = {}
textfile_options['E'] = os.path.normpath("E:/unpackedFiles_noheader")
textfile_options['C'] = os.path.normpath("C:/scratch/CanvasData/unpackedFiles_noheader")
textfile_options['studentcopy'] = os.path.normpath("C:/scratch/canvasData/unpackedFiles_noheader")

skip_list = ['']
RUN_SYNC = True
COPY_TEXT_FILES = True
database_textfile_directory = textfile_options['E']
database_name = "sarah_sandbox"

#email_recipients = ['sarah.taylor@rmit.edu.au', 'amelia.brennan@rmit.edu.au', 'amitoze.nandha@rmit.edu.au', 'peter.ryan2@rmit.edu.au']
email_recipients = ['sarah.taylor@rmit.edu.au']

run_canvas_update(RUN_SYNC, COPY_TEXT_FILES, skip_list, canvas_textfile_directory, database_textfile_directory, database_name, config_file_name, email_recipients)
