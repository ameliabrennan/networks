#!/usr/bin/python

'''
NOTE: I am classifying anything unknown/unknown as unknown, and in the main script I am ignoring these files entirely.
WHAT IS binary/octet-stream??? And text/x-troff-mm???
'''

Word_list = ['msword', 'vnd.openxmlformats-officedocument.wordprocessingml.document', 'rtf']
PP_list = ['vnd.ms-powerpoint', 'vnd.openxmlformats-officedocument.presentationml.presentation', 'vnd.oasis.opendocument.presentation', 'vnd.openxmlformats-officedocument.presentationml.slideshow']
excel_list = ['vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'vnd.ms-excel', 'vnd.ms-excel.sheet.macroEnabled.12']
zips_list = ['zip', 'x-zip-compressed', 'x-7z-compressed']
pdf_list = ['pdf']
javascript_list = ['javascript', 'x-javascript', 'x-java-archive', 'postscript']
flash_list = ['x-shockwave-flash', 'x-flash-video', 'x-gzip']
web_list = ['html', 'xml', 'css', 'javascript', 'x-javascript']
database_list = ['msaccess']
fonts_list = ['font-woff', 'x-font-ttf']

def get_type_from_MIME(mime_type):
    '''
    Takes in a mime_type, sorts it into some more general human-readable type as a string and returns this string. If the mime_type is not recognised it returns the same mime_type.
    '''
    this_type = mime_type   # defaults to be its own type to start with
    start = mime_type[0:4]
    if start == 'imag':
        this_type = 'image'
    elif start == 'appl':
        subtype = mime_type[12:]    # strip 'application/' from name
        if subtype in pdf_list:
            this_type = 'pdf'
        elif subtype in Word_list:
            this_type = 'word_doc'
        elif subtype in PP_list:
            this_type = 'slides'
        elif subtype in excel_list:
            this_type = 'spreadsheet'
        elif subtype in zips_list:
            this_type = 'zipped'
        elif subtype in javascript_list:
            this_type = 'web_content'
        elif subtype in flash_list:
            this_type = 'flash'
        elif subtype in database_list:
            this_type = 'database'
        elif subtype in fonts_list:
            this_type = 'fonts'
        elif subtype == 'illustrator':
            this_type = 'illustrator'
        elif subtype == 'vnd.wolfram.nb':
            this_type = 'Mathematica_nb'
        elif subtype == 'vnd.visio':
            this_type = 'image'
    elif start == 'text':
        subtype = mime_type[5:]    # strip 'text/' from name
        if subtype in web_list:
            this_type = 'web_content'
        else:
            this_type = 'text'
    elif start == 'audi':
        this_type = 'audio'
    elif start == 'vide':
        this_type = 'video'
    elif start == 'unkn':
        this_type = 'unknown'
    elif start == 'bina':
        this_type = 'unknown'
    #print 'new type is : ' + this_type
    return this_type

'''
test = ['image/jpeg', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'image/png', 'unknown/unknown', 'audio/mp3', 'text/html', 'application/pdf', 'application/x-shockwave-flash']

for item in test:
    result = get_type_from_MIME(item)
    print item + ': ' + result + '\n'
'''
