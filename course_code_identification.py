# Trys to find section of txt with a known course code
## All known course codes start with 3 or 4 characters

def return_course_code(txt):
  # All known course code charaters
  course_code_chars_List = ['ACCT','AERO','AERS','AGRI','ARCH','AUTO','BAFI',
                            'BESC','BIOL','BUIL','BUSM','CELL','CHEM','CIVE',
                            'COMM','COSC','COTH','CUED','DENT','EASC','ECON',
                            'EEET','EMPL','ENVI','EXTL','GEDU','GEOM','GRAP',
                            'HUSO','HWSS','INTE','ISYS','JUST','LANG','LAW',
                            'LIBR','MANU','MATH','MEDS','MIET',
                            'MKTG','NONE','NURS','OART','OENG','OFFC','OHTH',
                            'OMGT','ONPS','OPSC','OTED','PERF','PHAR','PHIL',
                            'PHYS','POLI','PROC','PUBH','RADI','REHA','SOCU',
                            'SOSK','SPRT','TCHE','TOUR','VART']
  # loop through course_chars List
  for course_chars in course_code_chars_List:
    print
    print course_chars
    # check for course_chars in txt
    #
    i = 0
    # check for instances of course_chars then 4 digits
    ## loop until course_chars not found or end of string reached
    while True:
      try:
        if course_chars in txt[i:]:
          print "1: %i" %i
          print txt
          i = txt.index(course_chars[i:])
        
          print "2: %i" %i
          # check for 4 digits past course_chars
          ## if 4 digits after alpha_chars return course code
          ## else check rest of txt
          if txt[i+len(course_chars):i+len(course_chars)+4].isdigit():
            return txt[i:i+len(course_chars)+4]
          print "3: %i" %i
          txt = txt[i+len(course_chars):]
          i = 0
          print "4: %i" %i
        else:
          break
      except:
        break

  # return empty string if not couse_code found
  return ""

print return_course_code('sdfdsfLAW357fdsjLAW2345fhs')
    
        
        
             

                         
