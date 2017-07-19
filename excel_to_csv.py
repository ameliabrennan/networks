# Assorted Excel to CSV functions
# This suite of functions will be very useful to the Data Science team, and will be expanded
# You will need to install the xlrd module on your machine

import xlrd
import csv
import os

# original function by Peter, will divert to the more specific csv_from_excel_onehseet function
def csv_from_excel(excelfile, csvfile):
  print("Refactored! Please consider using csv_from_excel_onesheet in future")
  result = csv_from_excel_onesheet(excelfile, csvfile)
  if (result == True):
    print("success!")


# converts an excel file and given sheet into a csv file
# defaults to Sheet1 only
# if the start and end columns are specified, it will only write those columns
# defaults to writing all columns
# Note: no error checking
def csv_from_excel_onesheet(excelfile, csvfile, sheetname='Sheet1', start_col=0, end_col=None):
    print("csv_from_excel_onseheet\n")
    print(excelfile)
    result = False
  #  try:
    wb = xlrd.open_workbook(excelfile)
    sh = wb.sheet_by_name(sheetname)
    your_csv_file = open(csvfile, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    print("ROWS IN SHEET: %s" %(str(sh.nrows)))
    num_rows = int(sh.nrows)
    for rownum in range(1, sh.nrows):
      print(str(rownum))
      #if((start_col==0) and (end_col==None)):
      print(str(sh.row_values(rownum)))
      #wr.writerow(sh.row_values(rownum))
      #else:
      #  print("Writing only columns between %s and %s" %(start_col, end_col))
      #  wr.writerow(sh.row_values(rownum, start_col, end_col))

    your_csv_file.close()
    result = True
  #  except:
  #    print('Encountered error in csv_from_excel')
  #    return(result)

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