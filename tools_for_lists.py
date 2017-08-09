import traceback

def check_for_element_in_list(input_list, search_item):
  result = False
  try:
    for item in input_list:
      if item == search_item:
        result = True
    return(result)
  except:
    traceback.print_exc()
    return(None)

def print_list(input_list, str_prefix="", str_suffix=""):
  try:
    for item in input_list:
      print(str_prefix, str(item), str_suffix)
    return
  except:
    traceback.print_exc()
    return

def remove_item_from_list(input_list, remove_item=""):
  try:
    for item in input_list:
      if item == remove_item:
        input_list.remove(item)
    return(input_list)
  except:
    traceback.print_exc()
    return(None)

def remove_list_from_list(input_list, remove_list):
  try:
    for remove_item in remove_list:
      for item in input_list:
        if item == remove_item:
          input_list.remove(item)
    return(input_list)
  except:
    traceback.print_exc()
    return(None)