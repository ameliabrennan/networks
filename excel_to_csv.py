# Assorted Excel functions
# This suite of functions will be very useful to the Data Science team, and will be expanded
# You will need to install the xlrd module on your machine
# Note that this set of tools is now geared to Python 3.6...I hope it is backwards compatible...

import xlrd
import csv
import os

# This function copies a single sheet (named 'Sheet1') from an Excel file, to a csv file
# It is the original function by Peter and will divert to the more specific 'csv_from_excel_onesheet' function
# It calls the function 'csv_from_excel_onesheet' and uses the default sheetname ('Sheet1')
# If successful in copying the Excel sheet it returns True
# If errors encountered in copying the Excel sheet it returns False
# Last updated July 2017
def csv_from_excel(excelfile, csvfile):
  print("Refactored! Please consider using csv_from_excel_onesheet in future")
  result = csv_from_excel_onesheet(excelfile, csvfile)
  if (result == True):
    print("success!")

# This function converts one sheet in a given Excel file, to a csv file
# The sheet name defaults 'Sheet1', but can be specified
# If the start and end columns are specified in the optional start_col and end_col, it will only write those columns
# It defaults to writing all columns in the given sheet, out to the csv file
# Last updated July 2017
def csv_from_excel_onesheet(excelfile, csvfile, sheetname='Sheet1', start_col=0, end_col=None):
    print("csv_from_excel_onseheet\n")
    print(excelfile)
    result = False
    try:
      wb = xlrd.open_workbook(excelfile)
      sh = wb.sheet_by_name(sheetname)
      your_csv_file = open(csvfile, 'w')
      wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
      print("ROWS IN SHEET: %s" %(str(sh.nrows)))
      num_rows = int(sh.nrows)

      for rownum in range(0, sh.nrows):
        print(str(rownum))
        if((start_col==0) and (end_col==None)):
          print(str(sh.row_values(rownum)))
          wr.writerow(sh.row_values(rownum))
        else:
          print("Writing only columns between %s and %s" %(start_col, end_col))
          wr.writerow(sh.row_values(rownum, start_col, end_col))

      your_csv_file.close()
      result = True
    except:
      print('Encountered error in csv_from_excel')
      return(result)

# Coverts all .xls and .xlsx files in the folder into csv files with the same name
# txtcondition is a optional string that must be contained in the filename  
def batch_csv(folder, txtcondition=''):
    for filename in os.listdir(folder):
        if (('.xls' in filename)
            and 
            (txtcondition in filename
            or txtcondition == '')):
            csvfile = filename[:filename.index('.xls')] + '.csv'
            print(filename)
            print(csvfile)
            csv_from_excel(folder+filename, folder+csvfile)

def test_call():
  print("function working")



def open_excel_file(excel_file_name):
  result = False
  try:
    wb = xlrd.open_workbook(excel_file_name)
    print("Opened %s" %excel_file_name)
    return(wb)
  except:
    return(result)  

def open_excel_sheet(wb, sheet_name):
  result = False
  try:
    sh = wb.sheet_by_name(sheet_name)
    return(sh)
  except:
    return(result)

def display_sheet_content(wb, sh):
  for rownum in xrange(sh.nrows):
    print(str(sh.row_values(rownum)))

  for colnum in xrange(sh.ncols):
    print(str(sh.col_values(colnum)))

def excel_column_to_array(wb, sh, colnum, ignore_header=True):
  result = False
  new_array = []

  if (ignore_header == True):
    startrow = 1
  else:
    startrow = 0

  for rownum in range(startrow, sh.nrows):
    print("Reading column %s row %s: %s" %(colnum, rownum, sh.cell_value(rownum, colnum)))
    new_array.append(sh.cell_value(rownum, colnum))
  return(new_array)
