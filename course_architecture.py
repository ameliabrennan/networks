import sqlite3 as sq
import numpy as np
from math import sqrt
import psycopg2
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import datetime
from mime_types import get_type_from_MIME
from compare_date import compare_date
from cleaning_sis import clean_sis_course_id
import traceback

i = datetime.datetime.now()

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
#conn = psycopg2.connect(database = "Canvas_TEST", FILL IN HERE)

# Connect to the database
conn = sq.connect(folder+dbfile)

# Make any user-defined functions accessible through sqlite
conn.create_function("set_file_type", 1, get_type_from_MIME)
conn.create_function("compare_date", 1, compare_date)
conn.create_function("clean_sis", 1, clean_sis_course_id)

# Create the cursor
cur = conn.cursor()

def create_view_file_dim_STARTINGPOINT(cur, cv_course_id=''):
    '''
    Pulls out the useful pieces from file_dim table. Note that files must be 'available' or 'hidden'.
    Includes an extra column that converts the content_type to a more general type.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_file_dim_STARTINGPOINT'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT course_id, id AS file_ID, display_name, content_type, set_file_type(content_type) AS new_type, owner_entity_type, file_state, Count(*)'
        qry += ' FROM file_dim'
        qry += ' WHERE (file_state = "available" OR file_state = "hidden")'
        if len(cv_course_id) > 0:
            qry += ' AND course_id IN {0}'.format(str(cv_course_id))
        qry += ' GROUP BY course_id, file_ID, display_name, content_type, new_type, owner_entity_type, file_state'
        qry += ' ORDER BY Count(*) DESC'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_file_fact_STARTINGPOINT(cur, cv_course_id=''):
    '''
    Pulls out the useful pieces from file_fact table.
    Puts them into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_file_fact_STARTINGPOINT'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT course_id, file_id AS file_ID, user_id, size, Count(*)'
        qry += ' FROM file_fact'
        if len(cv_course_id) > 0:
            qry += ' WHERE course_id IN {0}'.format(cv_course_id)

        qry += ' GROUP BY course_id, file_ID, user_id, size'
        qry += ' ORDER BY Count(*) DESC'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_course_dim_STARTINGPOINT(cur, cv_course_id=''):
    '''
    Pulls out the useful pieces from course_dim table.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_course_dim_STARTINGPOINT'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT id AS course_id, code AS course_code, sis_source_id AS course_code_term, workflow_state, Count(*)'
        qry += ' FROM course_dim'
        qry += ' WHERE (workflow_state = "available" OR workflow_state = "completed")'
        if len(cv_course_id) > 0:
            qry += ' AND course_id IN {0}'.format(cv_course_id)
        qry += ' GROUP BY course_id, code, sis_source_id, workflow_state'
        qry += ' ORDER BY Count(*) DESC'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)


def create_view_join_fileFact_fileDim(cur):
    '''
    Joins together the file tables (fact and dim) on the file_id variable.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_join_fileFact_fileDim'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        tab_fileFact = 'view_file_fact_STARTINGPOINT'
        tab_fileDim = 'view_file_dim_STARTINGPOINT'
        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT tab_fileFact.course_id AS course_id'
        qry += ', tab_fileFact.file_ID AS file_ID'
        qry += ', display_name, content_type, new_type, owner_entity_type, file_state'
        qry += ', user_id, size, Count(*)'
        qry += ' FROM ({0}) tab_fileDim LEFT JOIN ({1}) tab_fileFact ON tab_fileDim.file_id = tab_fileFact.file_id'.format(tab_fileDim, tab_fileFact)
        qry += ' GROUP BY tab_fileDim.course_id, tab_fileDim.file_ID, display_name, content_type, new_type, owner_entity_type, file_state, user_id, size'
        qry += ' ORDER BY Count(*) DESC'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_course_nFiles_size(cur, ignore_web_types=False):
    '''
    Counts the number of files for a course and sums the file sizes together.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_course_nFiles_size'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        tab_fileFactDim = 'view_join_fileFact_fileDim'
        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT course_id, Count(*) AS file_count, Sum(size) AS size_all_files'
        qry += ' FROM ({0})'.format(tab_fileFactDim)
        qry += ' WHERE (new_type != "unknown")'
        if ignore_web_types:
            qry += ' AND (new_type != "web_content")'
        qry += ' GROUP BY course_id'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_course_contentType_count(cur, new_file_types=True):
    '''
    Groups the files together by type, and counts the number of files within each type.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_course_contentType_count'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        tab_fileDim = 'view_file_dim_STARTINGPOINT'
        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT course_id,'
        if new_file_types:
            qry += ' new_type AS type,'
        else:
            qry += ' content_type AS type,'
        qry += ' Count(*) AS count'
        qry += ' FROM ({0})'.format(tab_fileDim)
        qry += ' GROUP BY course_id, type'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_course_nFileTypes(cur, ignore_web_types=True):
    '''
    Counts the number of file types. new_file_types is a flag determining whether to use the new file type definitions from mime_types.py (default) or the MIME types provided by content_type.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_course_nFileTypes'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        tab_course_contentType_count = 'view_course_contentType_count'
        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT course_id, Count(*) AS num_filetypes'
        qry += ' FROM ({0})'.format(tab_course_contentType_count)
        qry += ' WHERE type != "unknown"'
        if ignore_web_types:
            qry += ' AND type != "web_content"'
        qry += ' GROUP BY course_id'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_course_code_nFiles_sizeAll(cur):
    '''
    Joins the reduced course_dim table to the table that counts the number of files, joined on the course_id.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_course_code_nFiles_sizeAll'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        tab_courseDim = 'view_course_dim_STARTINGPOINT'
        tab_2 = 'view_course_nFiles_size'
        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT tab_fileDim.course_id, course_code, file_count, size_all_files'
        qry += ' FROM ({0}) tab_fileDim LEFT JOIN ({1}) tab_2 ON tab_fileDim.course_id = tab_2.course_id'.format(tab_courseDim, tab_2)
        qry += ' GROUP BY tab_fileDim.course_id, course_code, file_count, size_all_files'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

def create_view_course_code_nFiles_sizeAll_nFileTypes(cur):
    '''
    Joins the table with actual course code and number of files to the table with number of file types, joined on the course_id.
    Puts this into a VIEW.
    Returns view name if successful in doing so.
    Returns False if an error encountered.
    '''
    result = False
    try:
        view_name = 'view_course_code_nFiles_sizeAll_nFileTypes'
        qry = 'DROP VIEW IF EXISTS {0};'.format(view_name)
        cur.execute(qry)

        tab_1 = 'view_course_code_nFiles_sizeAll'
        tab_2 = 'view_course_nFileTypes'
        qry = 'CREATE VIEW {0} AS'.format(view_name)
        qry += ' SELECT tab_1.course_id, course_code, file_count, size_all_files, num_filetypes'
        qry += ' FROM ({0}) tab_1 LEFT JOIN ({1}) tab_2 ON tab_1.course_id = tab_2.course_id'.format(tab_1, tab_2)
        qry += ' GROUP BY tab_1.course_id, course_code, file_count, size_all_files, num_filetypes'
        qry += ';'
        print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)

# build all other functions as above
# build a function to update all of the views (which may be necessary if I change my code for them, not because underlying data will change) - will need to do this actually, every time I change course ID set
# build function to call something and output into a pandas DataFrame
# put in my loop or whatever to re-create my plots - how to extract useful stuff from the dataframe regarding content types?


def run_all(cur, cv_course_id='', ignore_web_types=True, new_file_types=True):

    result = create_view_file_dim_STARTINGPOINT(cur, cv_course_id=cv_course_id)
    print result
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_contentType_count(cur, new_file_types=new_file_types)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchall()
        print(tabulate(result, headers=zip(*cur.description)[0]))
        course_contentType_count_pd = DataFrame(result)
        course_contentType_count_pd.columns = [i[0] for i in cur.description]
        print course_contentType_count_pd.head(10)


    result = create_view_file_fact_STARTINGPOINT(cur, cv_course_id=cv_course_id)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_dim_STARTINGPOINT(cur, cv_course_id=cv_course_id)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_join_fileFact_fileDim(cur)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_nFiles_size(cur, ignore_web_types=ignore_web_types)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_code_nFiles_sizeAll(cur)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_nFileTypes(cur, ignore_web_types=ignore_web_types)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_code_nFiles_sizeAll_nFileTypes(cur)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchmany(10)
        print(tabulate(result, headers=zip(*cur.description)[0]))

        course_code_nFiles_sizeAll_nFileTypes_pd = DataFrame(result)
        course_code_nFiles_sizeAll_nFileTypes_pd.columns = [i[0] for i in cur.description]
        print course_code_nFiles_sizeAll_nFileTypes_pd.head(10)


run_all(cur, cv_course_id=('95950000000008895', '95950000000000153'))


'''
result = create_view_file_dim_STARTINGPOINT(cur, '95950000000008895')
if (result != False):
    print("Successfully created view %s!" %result)
    sql = 'SELECT * FROM view_file_dim_STARTINGPOINT;'
    cur.execute(sql)
    result = cur.fetchmany(10)
    print(tabulate(result))
#  print result.keys()
    df = DataFrame(cur.fetchall())
#  df.columns = cur.keys()
    num_fields = len(cur.description)
    df.columns = [i[0] for i in cur.description]
    print df.head(10)
'''
#NEXT: pull into Pandas dataframe

#result = cur.fetchone()
#result = cur.fetchmany(100)
#result = cur.fetchall()
#print result
#print tabulate(result)
#print cur.rowcount
#print len(result)
#print result[0][1]
