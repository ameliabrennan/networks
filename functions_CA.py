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

def create_view_file_dim_STARTINGPOINT(cur, cv_course_id='', broken_files=False, errored_files=False, deleted_files=False):
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
        if broken_files:
            qry += ' WHERE (file_state = "broken")'
            print 'WARNING: YOU HAVE SELECTED BROKEN FILES'
        elif errored_files:
            qry += ' WHERE (file_state = "errored")'
            print 'WARNING: YOU HAVE SELECTED ERRORED FILES'
        elif deleted_files:
            qry += ' WHERE (file_state = "deleted")'
            print 'WARNING: YOU HAVE SELECTED DELETED FILES'
        else:
            qry += ' WHERE (file_state = "available" OR file_state = "hidden")'
        if len(cv_course_id) > 0:
            qry += ' AND course_id IN {0}'.format(str(cv_course_id))
        qry += ' GROUP BY course_id, file_ID, display_name, content_type, new_type, owner_entity_type, file_state'
        qry += ' ORDER BY Count(*) DESC'
        qry += ';'
        #print(qry)
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
        #print(qry)
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
        #print(qry)
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
        #print(qry)
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
        #print(qry)
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
        #print(qry)
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
        #print(qry)
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
        #print(qry)
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
        #print(qry)
        cur.execute(qry)

        return(view_name)
    except:
        traceback.print_exc()
        return(result)


def get_course_contentType_count_as_DF(cur, cv_course_id='', new_file_types=True):
    '''
    Runs create_view_file_dim_STARTINGPOINT and create_view_course_contentType_count to create a view with course_id, type of files and counts of files within those types.
    Pulls this into a Pandas dataframe which is then returned.
    '''
    result = create_view_file_dim_STARTINGPOINT(cur, cv_course_id=cv_course_id)
    print result
    if (result != False):
        print("Successfully created view %s!" %result)
        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_contentType_count(cur, new_file_types=new_file_types)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchall()
        #print(tabulate(result, headers=zip(*cur.description)[0]))
        course_contentType_count_pd = DataFrame(result)
        course_contentType_count_pd.columns = [i[0] for i in cur.description]
        #print course_contentType_count_pd#.head(10)

    return course_contentType_count_pd

def get_course_code_nFiles_sizeAll_nFileTypes_as_DF(cur, cv_course_id='', new_file_types=True, ignore_web_types=False, broken_files=False, errored_files=False, deleted_files=False):
    '''
    Runs a bunch of view-creation functions, returns a pandas dataframe with course_id, course_code, num files, total size and num file types.
    '''
    result = create_view_file_dim_STARTINGPOINT(cur, cv_course_id=cv_course_id, broken_files=broken_files, errored_files=errored_files, deleted_files=deleted_files)
    print result
    if (result != False):
        print("Successfully created view %s!" %result)
        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))

    result = create_view_course_contentType_count(cur, new_file_types=new_file_types)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))

    result = create_view_file_fact_STARTINGPOINT(cur, cv_course_id=cv_course_id)
    if (result != False):
        print("Successfully created view %s!" %result)

        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_dim_STARTINGPOINT(cur, cv_course_id=cv_course_id)
    if (result != False):
        print("Successfully created view %s!" %result)

        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_join_fileFact_fileDim(cur)
    if (result != False):
        print("Successfully created view %s!" %result)

        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_nFiles_size(cur, ignore_web_types=ignore_web_types)
    if (result != False):
        print("Successfully created view %s!" %result)

        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_code_nFiles_sizeAll(cur)
    if (result != False):
        print("Successfully created view %s!" %result)

        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_nFileTypes(cur, ignore_web_types=ignore_web_types)
    if (result != False):
        print("Successfully created view %s!" %result)

        #sql = "SELECT * FROM {0};".format(result)
        #cur.execute(sql)
        #result = cur.fetchmany(10)
        #print(tabulate(result, headers=zip(*cur.description)[0]))


    result = create_view_course_code_nFiles_sizeAll_nFileTypes(cur)
    if (result != False):
        print("Successfully created view %s!" %result)
        sql = "SELECT * FROM {0};".format(result)
        cur.execute(sql)
        result = cur.fetchall()
        #print(tabulate(result, headers=zip(*cur.description)[0]))

        course_code_nFiles_sizeAll_nFileTypes_pd = DataFrame(result)
        course_code_nFiles_sizeAll_nFileTypes_pd.columns = [i[0] for i in cur.description]
        #print course_code_nFiles_sizeAll_nFileTypes_pd#.head(10)

    return course_code_nFiles_sizeAll_nFileTypes_pd

def create_dic_course_fileTypes(dataframe):
    '''
    Reads in a dataframe containing course_id, type and count (created by get_course_contentType_count_as_DF function), creates a dictionary of form (course_id : [list of file types])
    '''
    course_types_dic = {}
    for index, row in dataframe.iterrows():
        #print row
        course_id = str(row['course_id'])
        #print course_id
        file_type = str(row['type'])
        if course_id not in course_types_dic:
            course_types_dic[course_id] = [file_type]
        else:
            course_types_dic[course_id].append(file_type)
    return course_types_dic

def create_dic_fileTypes_nFiles(dataframe):
    '''
    Reads in a dataframe containing course_id, type and count (created by get_course_contentType_count_as_DF function), creates a dictionary of form (type : total number of files of that type])
    Also creates a second dictionary of form (type: [list of file counts by course])
    '''
    type_nFiles_dic = {}
    type_nFiles_list_dic = {}
    for index, row in dataframe.iterrows():
        #print row
        file_type = str(row['type'])
        #print file_type
        num = int(row['count'])
        #print num
        if file_type not in type_nFiles_dic:
            type_nFiles_dic[file_type] = num
            type_nFiles_list_dic[file_type] = [num]
        else:
            type_nFiles_dic[file_type] += num
            type_nFiles_list_dic[file_type].append(num)
    return type_nFiles_dic, type_nFiles_list_dic
