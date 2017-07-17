import xlrd
import csv
import os

def csv_from_excel(excelfile, csvfile):
    wb = xlrd.open_workbook(excelfile)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(csvfile, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()

def batch_csv(folder, txtcondition):
    for filename in os.listdir(folder):
        if txtcondition in filename:
            csvfile = filename[:filename.index('.xls')] + '.csv'
            print filename
            print csvfile
            csv_from_excel(folder+filename, folder+csvfile)
'''
batch_csv('H:\\Data\\Student Network Map\\Grades\\', 'Term')
'''
