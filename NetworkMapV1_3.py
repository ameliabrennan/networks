import datetime as dt
import os
import gc
import matplotlib.pyplot as plt
import sys
import sqlite3
import numpy as np
#import plotly.plotly as py
import csv
from operator import attrgetter


# Connect to database
folder = 'C:\\Peter\\Data\\Network Map\\SQLite\\'
dbfile = 'CourseNetwork.db'

conn = sqlite3.connect(folder+dbfile)
cur = conn.cursor()

###----------------StudentClass------------------###
class StudentClass(object):
    obList = []
    """ Student object with class key from SAMS"""
    def __init__(self, dataList, dataOrder=0):
        #dataList contains the data from CES

        self.classkey = dataList[0].strip()
        self.std_id = dataList[2].strip()
        self.program_code = dataList[3].strip()
        self.grade = dataList[4].strip()

        x = self.classkey.split('-')
        self.term_code = x[0]
        self.class_nb = int(x[1])
        self.course_code = x[2]
        self.osi = None
        StudentClass.obList.append(self)

    def __eq__(self, other):
        return (self.classkey==other.classkey
                and self.std_id==other.std_id)

    def __str__(self):
        return("Student:\t{0}\t{1}\t{2}\t{3}\t{4}"
               .format(self.std_id, self.program_code, self.classkey, self.grade, self.osi))

    def program_college(self):
        cur.execute(create_get_program_details_qry([self.program_code]))
        row = cur.fetchone()
        return row[0]

    def program_school(self):
        cur.execute(create_get_program_details_qry([self.program_code]))
        row = cur.fetchone()
        return row[1]

    def program_acad_career(self):
        cur.execute(create_get_program_details_qry([self.program_code]))
        row = cur.fetchone()
        return row[2]

    def program_desc(self):
        cur.execute(create_get_program_details_qry([self.program_code]))
        row = cur.fetchone()
        return row[5]

    def std_gender(self):
        cur.execute(create_get_student_details_qry([self.std_id]))
        row = cur.fetchone()
        return row[2]

    def std_acad_load(self):
        cur.execute(create_get_student_details_qry([self.std_id]))
        row = cur.fetchone()
        return row[3]

    def std_cit_code(self):
        cur.execute(create_get_student_details_qry([self.std_id]))
        row = cur.fetchone()
        return row[4]

    def std_country(self):
        cur.execute(create_get_student_details_qry([self.std_id]))
        row = cur.fetchone()
        return row[6]

    def std_lote(self):
        cur.execute(create_get_student_details_qry([self.std_id]))
        row = cur.fetchone()
        return row[7]

    def course_name(self):
        cur.execute(create_get_class_details_qry([self.classkey]))
        row = cur.fetchone()
        return row[3]

    def course_acad_career(self):
        cur.execute(create_get_class_details_qry([self.classkey]))
        row = cur.fetchone()
        return row[4]

    def course_college(self):
        cur.execute(create_get_class_details_qry([self.classkey]))
        row = cur.fetchone()
        return row[5]

    def course_school(self):
        cur.execute(create_get_class_details_qry([self.classkey]))
        row = cur.fetchone()
        return row[6]

    def course_campus(self):
        cur.execute(create_get_class_details_qry([self.classkey]))
        row = cur.fetchone()
        return row[7]

    def course_foe(self):
        cur.execute(create_get_class_details_qry([self.classkey]))
        row = cur.fetchone()
        return row[8]

def create_get_Grade_qry(classkeys=[], term_codes = [], course_codes=[], std_ids=[], prg_codes=[], grades=[]):
    qry = 'SELECT * ' \
          'FROM Grades '

    # Add WHERE statements if necessary
    if (len(classkeys) > 0
        or len(term_codes) > 0
        or len(course_codes) > 0
        or len(std_ids) > 0
        or len(prg_codes) > 0
        or len(grades) > 0):

        qry += 'WHERE ( '
        if len(classkeys) > 0:
            qry += ' ( '
            # Add each program
            for clkey in classkeys:
                qry += 'classkey = "%s" OR ' % clkey
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(term_codes) > 0:
            qry += ' ( '
            # Add each program
            for term in term_codes:
                qry += 'classkey LIKE "%s%%" OR ' % term
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(course_codes) > 0:
            qry += ' ( '
            # Add each program
            for crse in course_codes:
                qry += 'course_code = "%s" OR ' % crse
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(std_ids) > 0:
            qry += ' ( '
            # Add each program
            for std in std_ids:
                qry += 'NDS_EMPID = "%s" OR ' % std
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(prg_codes) > 0:
            qry += ' ( '
            # Add each program
            for prg in prg_codes:
                qry += 'acad_prog = "%s" OR ' % prg
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(grades) > 0:
            qry += ' ( '
            # Add each program
            for g in grades:
                qry += 'CRSE_GRADE_OFF = "%s" OR ' % g
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        # remove last 'AND '
        qry = qry[:-4]
        qry += ' ) '

    qry += 'ORDER BY course_code, nds_emplid'
    return qry

# Get Class data
def GradesDBtoObject(cursor, classkeys=[], term_codes = [], course_codes=[], std_ids=[],
                     prg_codes=[], grades=[], batch_size=1000):
    cur.execute(create_get_Grade_qry(classkeys, term_codes, course_codes, std_ids, prg_codes, grades))
    while True:
        rows = cur.fetchmany(batch_size)
        if not rows: break
        for row in rows:
            StudentClass(row)

###----------------Program Details-----------------------###
class ProgramDetails(object):
    obList = []
    """ Program details from SAMS"""
    def __init__(self, dataList):

        # dataList contains the data
        # dataType indicates the ordering of the data
        self.college_code = dataList[0].strip()
        if self.college_code == 'SET':
            self.college_code = 'SEH'
        self.school_code = dataList[1].strip()
        self.acad_career = dataList[2].strip()
        self.program_status = dataList[3].strip()
        self.program_code = dataList[4].strip()
        self.program_description = dataList[5].strip()
        ProgramDetails.obList.append(self)

    def __eq__(self, other):
        return (self.program_code==other.program_code)

    def __str__(self):
        return("Program:\t{0}\t{1}\t{2}\t{3}"
               .format(self.program_code, self.acad_career, self.school_code, self.college_code))

def create_get_program_details_qry(prg_code=[], school=None, college=None, acad_career=None):
    qry = 'SELECT * ' \
          'FROM Program_details '

    # Add WHERE statements if necessary
    if (len(prg_code) > 0
        or school != None
        or college != None
        or acad_career != None):
        qry += 'WHERE ( '

        if len(prg_code) > 0:
            qry += ' ( '
            # Add each program
            for prg in prg_code:
                qry += 'program_code = "%s" OR ' % prg
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if school != None:
            qry += ' program_school = "%s" AND ' % school

        if college != None:
            qry += ' program_college = "%s" AND ' % college

        if acad_career != None:
            qry += ' program_acad_career = "%s" AND ' % acad_career

        # remove last 'AND '
        qry = qry[:-4]
        qry += ' ) '

    qry += 'ORDER BY program_code '
    return qry

# Get Programs data
def ProgramDBtoObject(cursor, prg_code=[], school=None, college=None, acad_career=None, batch_size=1000):
    cur.execute(create_get_program_details_qry(prg_code, school, college, acad_career))
    while True:
        rows = cur.fetchmany(batch_size)
        if not rows: break
        for row in rows:
            ProgramDetails(row)

# Get all
#ProgramDBtoObject(cur)

###----------------Class Details-----------------------###
class ClassDetails(object):
    obList = []
    """ Class object from SAMS"""
    def __init__(self, dataList):
        # dataList contains the data
        # dataType indicates the ordering of the data
        self.classkey = dataList[0].strip()
        self.term_code = int(dataList[1].strip())
        self.course_code = dataList[2].strip()
        self.course_name = dataList[3].strip()
        self.acad_career = dataList[4].strip()
        self.college_code = dataList[5].strip()
        self.school_code = dataList[6].strip()
        self.campus = dataList[7].strip()
        self.foe_description = dataList[8].strip()
        self.class_instructor1_id = dataList[9].strip()
        self.class_instructor2_id = dataList[10].strip()
        self.term_desc = dataList[11].strip()
        ClassDetails.obList.append(self)

    def year(self):
        return(int(self.term_code/100) + 2000)

    def __eq__(self, other):
        return (self.classkey == other.classkey)

    def __str__(self):
        return("Class:\n"
               "  classkey = {0}\n"
               "  course_code = {1}\n"
               "  course_name = {2}\n"
               "  term_code = {3}\n"             
               "  acad_career = {4} \n"
               "  school_code = {5} \n"
               "  college_code = {6} \n"
               "  campus = {7} \n"
               "  foe_description = {8} \n"
               .format(self.classkey, self.course_code, self.course_name, self.term_code,
                       self.acad_career,  self.school_code, self.college_code, self.campus,
                       self.foe_description))

def create_get_class_details_qry(classkeys=[],  term_codes=[], course_codes=[],
                                  acad_career=None, school=None, college=None,
                                  campus=None, foe_description=None):

    qry = 'SELECT * ' \
          'FROM Class_details '

    # Add WHERE statements if necessary
    if (len(classkeys) > 0
        or len(term_codes) > 0
        or len(course_codes) > 0
        or acad_career != None
        or school != None
        or college != None
        or campus != None
        or foe_description != None):

        qry += 'WHERE ( '

        if len(classkeys) > 0:
            qry += ' ( '
            # Add each program
            for classkey in classkeys:
                qry += 'classkey = "%s" OR ' % classkey
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(term_codes) > 0:
            qry += ' ( '
            # Add each program
            for term_code in term_codes:
                qry += 'term_code = "%s" OR ' % term_code
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if len(course_codes) > 0:
            qry += ' ( '
            # Add each program
            for course_code in course_codes:
                qry += 'course_code = "%s" OR ' % course_code
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '


        if acad_career != None:
            qry += ' course_acad_career = "%s" AND ' % acad_career

        if school != None:
            qry += ' course_school = "%s" AND ' % school

        if college != None:
            qry += ' course_college = "%s" AND ' % college

        if campus != None:
            qry += ' course_campus = "%s" AND ' % campus

        if foe_description != None:
            qry += ' course_foe = "%s" AND ' % foe_description

        # remove last 'AND '
        qry = qry[:-4]
        qry += ' ) '

    qry += 'ORDER BY classkey '
    return qry

# Get Class data
def ClassDBtoObject(cursor, classkeys=[],  term_codes=[], course_codes=[],
                                  acad_career=None, school=None, college=None,
                                  campus=None, foe_description=None, batch_size=1000):
    cur.execute(create_get_student_details_qry(classkeys,  term_codes, course_codes,
                                             acad_career, school, college,
                                             campus, foe_description))
    while True:
        rows = cur.fetchmany(batch_size)
        if not rows: break
        for row in rows:
            ClassDetails(row)

# Get all Class details
#ClassDBtoObject(cur)

###----------------Student Details-----------------------###
class StudentDetails(object):
    obList = []
    """ StudentDetails object from SAMS"""
    def __init__(self, dataList):
        # dataList contains the data
        # dataType indicates the ordering of the data

        self.std_id = dataList[0].strip()
        self.dob = dataList[2].strip()
        self.gender = dataList[5].strip()
        self.acad_load = dataList[8].strip()
        self.ftpt = dataList[8].strip()
        self.citizenship_code = dataList[10].strip()
        self.citizen_cat = dataList[11].strip()
        self.country = dataList[12].strip()
        self.lote = dataList[13].strip()
        StudentDetails.obList.append(self)

    def __eq__(self, other):
        return (self.std_id==other.std_id)

    def __str__(self):
        return("Student:\t{0}\n".format(self.std_id))

def create_get_student_details_qry(std_ids=[],  gender=None, acad_load=None, citizenship_code=None,
                                   country=None, lote=None):
    qry = 'SELECT * ' \
          'FROM Student_details '

    # Add WHERE statements if necessary
    if (len(std_ids) > 0
        or gender != None
        or acad_load != None
        or citizenship_code != None
        or country != None
        or lote != None):
        qry += 'WHERE ( '

        if len(std_ids) > 0:
            qry += ' ( '
            # Add each program
            for std in std_ids:
                qry += 'std_id = "%s" OR ' % std
            # remove last 'OR '
            qry = qry[:-3]
            qry += ' ) AND '

        if gender != None:
            qry += ' gender = "%s" AND ' % gender

        if acad_load != None:
            qry += ' acad_load = "%s" AND ' % acad_load

        if citizenship_code != None:
            qry += ' citizenship_code = "%s" AND ' % citizenship_code

        if country != None:
            qry += ' country = "%s" AND ' % country

        if lote != None:
            qry += ' lote = "%s" AND ' % lote

        # remove last 'AND '
        qry = qry[:-4]
        qry += ' ) '

    qry += 'ORDER BY std_id '
    return qry

# Get Student data
def StudentDBtoObject(cursor, std_ids=[], gender=None, acad_load=None, citizenship_code=None,
                      country=None, lote=None, batch_size=1000):
    cur.execute(create_get_student_details_qry(std_ids, gender, acad_load, citizenship_code,
                                             country, lote))
    while True:
        rows = cur.fetchmany(batch_size)
        if not rows: break
        for row in rows:
            StudentDetails(row)

# Get all Student details
#StudentDBtoObject(cur)


GradesDBtoObject(cur, term_codes=['1710'])

stdcl = StudentClass.obList[0]





