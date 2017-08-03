import sqlite3 as sq
import numpy as np
from math import sqrt
import psycopg2
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import datetime
import operator
from functions_CA import create_view_file_dim_STARTINGPOINT, create_view_file_fact_STARTINGPOINT, create_view_course_dim_STARTINGPOINT, create_view_join_fileFact_fileDim, create_view_course_nFiles_size, create_view_course_contentType_count, create_view_course_nFileTypes, create_view_course_code_nFiles_sizeAll, create_view_course_code_nFiles_sizeAll_nFileTypes, create_dic_course_fileTypes, get_course_contentType_count_as_DF, get_course_code_nFiles_sizeAll_nFileTypes_as_DF, create_dic_fileTypes_nFiles
from mime_types import get_type_from_MIME
from compare_date import compare_date
from cleaning_sis import clean_sis_course_id
from count_course_with_type import count_course_with_type
import traceback

# Get list of Canvas course IDs from AN:
courses = pd.read_csv('/Users/e35596/RMITStudios/Canvas_metrics/Canvas_IDs_in_SAMS.csv', usecols = ['id'])
#print courses.head(10)
course_list = courses['id'].tolist()
#print course_list, type(course_list)

# Connect to database
folder = '/Users/e35596/RMITStudios/Canvas_metrics/'
fig_dir = folder + 'figs/'
dbfile = 'test.sqlite'

# Sarah's database (will break as the table names may not be the same)
#conn = psycopg2.connect(database = "Canvas_TEST", STUFF)

# Connect to the database
conn = sq.connect(folder+dbfile)

# Make any user-defined functions accessible through sqlite
conn.create_function("set_file_type", 1, get_type_from_MIME)
conn.create_function("compare_date", 1, compare_date)
conn.create_function("clean_sis", 1, clean_sis_course_id)

# Create the cursor
cur = conn.cursor()

# The list of live courses that we're working with, obtained by PR
live_courses_from_PR = ('95950000000000628', '95950000000008932', '95950000000001212', '95950000000001479', '95950000000001534', '95950000000001587', '95950000000001629', '95950000000001810', '95950000000000416', '95950000000010440', '95950000000000391', '95950000000000393', '95950000000010380', '95950000000002289', '95950000000002663', '95950000000002670', '95950000000002678', '95950000000009379', '95950000000003039', '95950000000003061', '95950000000009119', '95950000000003186', '95950000000003266', '95950000000010866', '95950000000009322', '95950000000000407', '95950000000000409', '95950000000004505', '95950000000004554', '95950000000009214', '95950000000000367', '95950000000000379', '95950000000004822', '95950000000000400', '95950000000010485', '95950000000010352', '95950000000009402', '95950000000010853', '95950000000010487', '95950000000000495', '95950000000000555', '95950000000006912', '95950000000007232', '95950000000007516', '95950000000007526', '95950000000000348', '95950000000000351', '95950000000008069', '95950000000008212', '95950000000010488', '95950000000008602')

# OLD: for testing
#live_courses_from_PR = ('95950000000000126', '95950000000000132', '95950000000000153', '95950000000000156', '95950000000000163', '95950000000000165', '95950000000000170', '95950000000000174', '95950000000000175', '95950000000000178', '95950000000000185', '95950000000000191', '95950000000000192', '95950000000000193', '95950000000000194', '95950000000000209', '95950000000000214', '95950000000000215', '95950000000000220', '95950000000000224', '95950000000000225', '95950000000000226', '95950000000000228', '95950000000000234', '95950000000000259', '95950000000000262', '95950000000000271', '95950000000000272', '95950000000000273', '95950000000000275', '95950000000000276', '95950000000000278', '95950000000000279', '95950000000000281', '95950000000000282', '95950000000000283', '95950000000000285', '95950000000000287', '95950000000000288', '95950000000000289', '95950000000000290', '95950000000000297', '95950000000000298', '95950000000000318', '95950000000000348', '95950000000000351', '95950000000000367', '95950000000000370', '95950000000000379', '95950000000000391', '95950000000000393', '95950000000000400', '95950000000000406', '95950000000000407', '95950000000000409', '95950000000000414', '95950000000000416', '95950000000000426', '95950000000000493', '95950000000000495', '95950000000000549', '95950000000000555', '95950000000000611', '95950000000000614', '95950000000000616', '95950000000000618', '95950000000000628', '95950000000001212', '95950000000001245', '95950000000001479', '95950000000001534', '95950000000001535', '95950000000001587', '95950000000001629', '95950000000001810', '95950000000002289', '95950000000002663', '95950000000002670', '95950000000002678', '95950000000002736', '95950000000003039', '95950000000003061', '95950000000003186', '95950000000003266', '95950000000004501', '95950000000004504', '95950000000004505', '95950000000004554', '95950000000004822', '95950000000004943', '95950000000005177', '95950000000005788', '95950000000005830', '95950000000005993', '95950000000006764', '95950000000006912', '95950000000006918', '95950000000006919', '95950000000007232', '95950000000007452', '95950000000007516', '95950000000007526', '95950000000007577', '95950000000008069', '95950000000008212', '95950000000008394', '95950000000008602', '95950000000008826', '95950000000008932', '95950000000009119', '95950000000009205', '95950000000009206', '95950000000009214', '95950000000009322', '95950000000009379', '95950000000009402', '95950000000010352', '95950000000010380', '95950000000010440', '95950000000010485', '95950000000010487', '95950000000010488', '95950000000010643', '95950000000010853', '95950000000010866', '95950000000011375')


#########################  Extracting the file types by course and plotting the frequencies of courses containing each file type  #########################

# Get the dataframe containing the file types and frequencies
dataframe1 = get_course_contentType_count_as_DF(cur, cv_course_id=live_courses_from_PR, new_file_types=True)
#print dataframe1

# Turn this into a dictionary of course ids with all filetypes they contain
file_types_dic = create_dic_course_fileTypes(dataframe1)
print file_types_dic

# Turn this into another dictionary of file types and number of courses in which they appear
freq_dic = count_course_with_type(file_types_dic)
#print freq_dic

# Create dictionary of file types with the total number of times they appear in any course, and another of file types with list of number of files
type_nFiles_dic, type_nFiles_list_dic = create_dic_fileTypes_nFiles(dataframe1)
#print type_nFiles_dic
#print type_nFiles_list_dic



# Divide the totals by the number of courses containing at least one of these file types to work out the average number of times a file type is used by a course
x_num_courses = []
y_mean_files = []
type_labels = []
for key in freq_dic:
    num_courses = freq_dic[key]
    try:
        num_files = type_nFiles_dic[key]
        x_num_courses.append(num_courses)
        mean = float(num_files)/num_courses
        y_mean_files.append(mean)
        type_labels.append(key)
    except:
        print 'Problem!'
        pass

print x_num_courses
print y_mean_files
print type_labels

plt.figure(figsize=(20,13))
plt.scatter(x_num_courses,y_mean_files)
for i, txt in enumerate(type_labels):
    plt.annotate(txt, (x_num_courses[i],y_mean_files[i]), xytext=(5, 5), textcoords='offset points')
plt.xlabel('Number of courses containing file type')
plt.ylabel('Average number of files by type')
plt.xlim(0,60)
plt.ylim(0,120)
plt.grid()
#plt.show()
plt.savefig(fig_dir + 'mean_nFiles_vs_nCourses_byType.png')
plt.close()



# sort the dictionary in descending order of frequency
sorted_freq_dic = sorted(freq_dic.items(), key=operator.itemgetter(1), reverse=True)
#print sorted_freq_dic

# Pull this apart for plotting
#print zip(*sorted_freq_dic)
x_tick_labels = zip(*sorted_freq_dic)[0]
x = np.arange(len(x_tick_labels))
y = zip(*sorted_freq_dic)[1]

plt.figure(figsize=(20,15))
ax = plt.subplot(1, 1, 1)
#plt.ylim(0,110)
#plt.xlim(-1,len(name))
plt.xticks(x, x_tick_labels,rotation=70)
plt.bar(x,y, align='center')
ax.set_xlabel('File types')
ax.set_ylabel('Number of courses')
#plt.show()
plt.savefig(fig_dir + 'fileType_vs_numCourses.png')
plt.close()



for key in type_nFiles_list_dic:
    print key + ': ' + str(type_nFiles_list_dic[key])
    plt.hist(type_nFiles_list_dic[key])
    plt.xlabel('Number of {0} files'.format(key))
    plt.ylabel('Number of courses')
    #plt.show()
    plt.savefig(fig_dir + 'hist_by_type/hist_' + key + '.png')
    plt.close()


#########################  Extracting the numbers of files, size, etc and plotting these  #########################

# Get the dataframe containing files, size, types
dataframe2 = get_course_code_nFiles_sizeAll_nFileTypes_as_DF(cur, cv_course_id=live_courses_from_PR, new_file_types=True, ignore_web_types=True, broken_files=False)
print dataframe2#.head(10)

# Plot
x_labs_dic = {'file_count': 'Total number of files', 'size_all_files': 'Total size of all files (MB)', 'num_filetypes': 'Number of file types'}

for var in ['file_count', 'size_all_files', 'num_filetypes']:
    dataframe2.hist(column=var, bins=6)
    plt.xlabel(x_labs_dic[var])
    plt.ylabel('Number of courses')
    #plt.show()
    plt.savefig(fig_dir + var + '.png')
    plt.close()
