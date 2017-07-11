# Check str of unknown length and format for 8 or 9 digits with course_code structure
def return_course_code(str):
  while True:
    for i in range(len(str)):
      try:
        if check_str4_num4(str[i:i+8], 4, 4):
          try:
            if str[i+8:i+9].isalpha():
              return str[i:i+9]
            else:
              return str[i:i+8]
          except:
            return str[i:i+8] 
      except:
        return ""

# check first str_len of str sre alpha
# check next num_len of str are digit
def check_str_num(str, str_len=4, num_len=4):
  if len(str) != str_len + num_len):
    return False
    
  try:
    if not str[:str_len].isalph():
      return False
    if not str[str_len:].isdigit():
      return False
  except:
    return False
    
