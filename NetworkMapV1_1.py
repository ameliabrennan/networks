import datetime as dt
import os
import gc
import matplotlib.pyplot as plt
import numpy as np
#import plotly.plotly as py
import csv

class Course:
    """ Course Object"""
    # Contains information relating to Courses, with enorolled students.
    obList = []
    countUnique = 0
    def __init__(self, course_code, term_code, school_code, school_name, college_code, college_name):

        self.course_code = course_code
        self.school_code = school_code
        self.school_name = school_name
        self.college_code = college_code
        self.college_name = college_name
        self.term_code = term_code
        self.year = int(term_code/100)+2000
        self.stdList = []
        self.stdobList = []

        # Add Course to Course.obList
        Course.obList.append(self)

    # returns header text string with Course variables with tab seperators
    def header(self):
        txt = 'year\tterm_code\tcourse_code\tschool_code\tcollege\tstd_pop\tprg_code\tprg_pop'
        return txt

    # returns text string with Course variables with tab seperators
    def info(self):
        txt = ''
        txt += '%i\t%i\t' % (self.year,
                             self.term_code)
        txt += '%s\t%s\t%s\t' % (self.course_code,
                                 self.school_code,
                                 self.college_code)
        txt += '%i\t' % self.std_pop()
        for prg in self.prg_list():
            txt += '%s\t%i\t' % (prg[0], prg[1])
        return txt[:-1]

    # returns text string with Course variables headers with comma seperators
    def headerCSV(self):
        txt = 'year,term_code,course_code,school_code,college_code,std_pop'
        return txt

    # returns text string with Course variables with comma seperators
    def CSV(self):
        txt = ''
        txt += '%i,%i,' % (self.year,
                           self.term_code)
        txt += '%s,%s,%s,' % (self.course_code,
                              self.school_code,
                              self.college_code)
        txt += '%i,' % self.std_pop()
        return txt

    def std_pop(self):
        return len(self.stdList)

    def prg_list(self):
        prg_list = []
        prg_pop_list = []
        for std in self.stdList:
            if std[1] not in prg_list:
                prg_list.append(std[1])
                prg_pop_list.append(1)
            else:
                i = prg_list.index(std[1])
                prg_pop_list[i] += 1
        temp = []
        for i in range(len(prg_list)):
            temp.append([prg_list[i], prg_pop_list[i]])
        temp.sort(key=lambda x: x[1], reverse=True) # this sorts the temp list according to prg_pop_list I think
        return temp

class CourseConnections:
    """ Course Object"""
    # Contains information relating to Courses, broken down by Programs.
    obList = []

    def __init__(self, course1, course2):

        self.course1 = course1
        self.course2 = course2
        self.stdList = []

        for std in course1.stdList:
            if std in course2.stdList:
                self.stdList.append(std)

        CourseConnections.obList.append(self)

    # returns header text string with Course variables with tab seperators
    def header(self):
        txt = 'term_code1\tcourse_code1\t'
        txt += 'term_code2\tcourse_code2\t'
        txt += 'std_pop\tprg_code\tprg_pop'
        return txt

    # returns text string with CourseConnections variables with tab seperators
    def info(self):
        txt = ''
        txt += '%i\t%s\t' % (self.course1.term_code,
                             self.course1.course_code)
        txt += '%i\t%s\t' % (self.course2.term_code,
                             self.course2.course_code)
        txt += '%i\t' % self.std_pop()
        for prg in self.prg_list():
            txt += '%s\t%i\t' % (prg[0], prg[1])
        return txt[:-1]

    # returns text string with Course variables headers with comma seperators
    def headerCSV(self):
        txt = 'term_code1,course_code1,'
        txt += 'term_code2,course_code2,'
        txt += 'std_pop'
        return txt

    # returns text string with Course variables with comma seperators
    def CSV(self):
        txt = ''
        txt += '%i,%s,' % (self.course1.term_code,
                           self.course1.course_code)
        txt += '%i,%s,' % (self.course2.term_code,
                           self.course2.course_code)
        txt += '%i,' % self.std_pop()
        return txt

    def std_pop(self):
        return len(self.stdList)

    def prg_list(self):
        prg_list = []
        prg_pop_list = []
        for std in self.stdList:
            if std[1] not in prg_list:
                prg_list.append(std[1])
                prg_pop_list.append(1)
            else:
                i = prg_list.index(std[1])
                prg_pop_list[i] += 1
        temp = []
        for i in range(len(prg_list)):
            temp.append([prg_list[i], prg_pop_list[i]])
        temp.sort(key=lambda x: x[1], reverse=True)
        return temp

class Program:
    """ Course Object"""
    # Contains information relating to Programs, broken down by Courses.
    obList = []
    countUnique = 0
    def __init__(self, course_name, course_code, course_career_level, course_start_date,
                 college_code, college_name, sch_code, sch_name,
                 prg_descrip, prg_code, prg_career_level,
                 campus_code, campus_descrip, campus_loc, campus_loc_descrip,
                 course_delivery_mode, course_delivery_mode_descrip,
                 term_code, term_year):

        self.course_name = course_name
        self.course_code = course_code
        self.course_career_level = course_career_level
        self.course_start_date = course_start_date

        self.college_code = college_code
        self.college_name = college_name
        self.sch_code = sch_code
        self.sch_name = sch_name

        self.prg_descrip = prg_descrip
        self.prg_code = prg_code
        self.prg_career_level = prg_career_level

        self.campus_code = campus_code
        self.campus_descrip = campus_descrip
        self.campus_loc = campus_loc
        self.campus_loc_descrip = campus_loc_descrip

        self.course_delivery_mode = course_delivery_mode
        self.course_delivery_mode_descrip = course_delivery_mode_descrip

        self.term_code = term_code
        self.year = term_year

        # Student population will be counted in
        self.std_count_enrol = 0

        # Total student in Course and Total programs in Course is calculated by calcCourseTotalProgramandStudentsCount
        self.total_std_prg_count_enrol = 0
        self.total_course_prg_count = 0

        #Count the number of unique courses
        try:
            #Check to see if Course/Program already exists
            if (self.prg_descrip != Program.obList[-1].prg_descrip and
                self.prg_code != Program.obList[-1].prg_code):
                Program.countUnique += 1
        except:
            Program.countUnique = 1

        # Add Course to Course.obList
        Program.obList.append(self)


    # returns text string with Course variables with tab seperators
    def printProgram(self):
        txt = ''
        txt += '%s\t%i\t%i\t%i\t' % (self.year,
                                     self.std_count_enrol,
                                     self.total_std_prg_count_enrol,
                                     self.total_course_prg_count)

        txt += '%s\t%s\t%s\t%s\t%s\t' % (self.course_name,
                                         self.course_code,
                                         self.term_code,
                                         self.course_career_level,
                                         self.course_start_date)

        txt += '%s\t%s\t%s\t%s\t' % (self.college_code,
                                     self.college_name,
                                     self.sch_code,
                                     self.sch_name)
        txt += '%s\t%s\t%s\t' % (self.prg_descrip,
                                 self.prg_code,
                                 self.prg_career_level)

        txt += '%s\t' % (self.campus_code)

        txt += '%s' % (self.course_delivery_mode_descrip)

        return txt

    # returns text string with Course variables headers with comma seperators
    def printHeaderCSV(self):
        txt = ''
        txt += 'Program_name,Program_code,Term_code,Program_sector,Course_duplicate,'
        txt += 'Program_no_of_courses,Program_no_of_students,'
        txt += 'Course_date_start,Course_date_first_start,'
        txt += 'College_name,College_code,School_name,School_code,'
        txt += 'Course_name,Course_code,Course_sector,Course_student_no,Course_student_percentage,'
        txt += 'Course_Campus,Course_Country,Course_Delivery,'
        txt += 'LMS_Champion,Complexity,'
        return txt

    # returns text string with Course variables with comma seperators
    def printProgramCSV(self):
        txt = ''
        if self.std_count_enrol != 0:
            txt += '"%s",%s,%s,%s,,%i,%i,' % (self.prg_descrip,
                                              self.prg_code,
                                              self.term_code,
                                              self.prg_career_level,
                                              self.total_course_prg_count,
                                              self.total_std_prg_count_enrol)

            txt += '%s,,' % (self.course_start_date)

            txt += '"%s",%s,"%s",%s,' % (self.college_name, self.college_code,
                                     self.sch_name, self.sch_code)

            txt += '"%s",%s,%s,%i,%.1f,' % (self.course_name,
                                          self.course_code,
                                          self.course_career_level,
                                          self.std_count_enrol,
                                          (100*self.std_count_enrol/(1.0*self.total_std_prg_count_enrol)))

            txt += '%s,,%s,' % (self.campus_code, self.course_delivery_mode_descrip)
            txt += ',,'
        return txt

class All:
    """ Students object with programs and associated courses"""
    obList = []

    def __init__(self, dataList):

        self.classkey = dataList[0].strip()
        x = self.classkey.split('-')
        self.course_term_code = int(x[0])
        self.course_code = x[2]
        self.std_nds_empid = dataList[1].strip()
        self.std_prg_code = dataList[2].strip()
        self.course_school_code = dataList[3].strip()
        self.course_school_name = dataList[4].strip()
        self.course_college_code = dataList[5].strip()
        self.course_college_name = dataList[6].strip()
        All.obList.append(self)

class StudentProgram:
    """ StudentProgram Object"""
    # Contains Student information including program.
    obList = []

    def __init__(self, nds_empid, prg_code):
        self.nds_empid = nds_empid
        self.prg_code = prg_code
        self.courseList = []
        StudentProgram.obList.append(self)

    # returns text string with Student ivariables with tab seperators
    def info(self):
        txt = ''
        txt += '%s\t%s\t' % (self.nds_empid,
                             self.prg_code)
        return txt[:-1]

def readAllFile(f1, maxread=None):
    csv_reader = csv.reader(f1)
    header = next(csv_reader)
    count = 0
    while (count < maxread or maxread == None):
        try:
            count += 1
            All(next(csv_reader))
        except Exception as e:
            print e
            break
    f1.close()

def createStudentPrograms(term_code_list=[], prg_list = [], maxstd = None):
    # Sort All_Info object by student and program
    All.obList.sort(key=lambda x: (x.std_nds_empid, x.std_prg_code))

    # Initialise the codes
    std_nds_empid = 'df'
    std_prg_code = 'df'
    if (maxstd == None
        or maxstd > len(All.obList)):
        maxstd = len(All.obList)

    # Loop through All_Info objects
    ## maxstudents sets a limit on the number of object in the loop
    for x in All.obList[:maxstd]:
        if ((x.course_term_code in term_code_list
             or term_code_list == [])
            and
            (x.std_prg_code in prg_list
             or prg_list == [])):
            #print x.course_term_code, x.std_prg_code
        # If course changes create a new Course object
        # The course object include the student count
            if (std_nds_empid != x.std_nds_empid
                or std_prg_code != x.std_prg_code):
                std = StudentProgram(x.std_nds_empid, x.std_prg_code)

                # Change codes to new codes
                std_nds_empid = x.std_nds_empid
                std_prg_code = x.std_prg_code

# Loops through All objects to create course objects
## Course objects are unique, each student in the course is added to the course object.
def createCourses(term_code_list=[], prg_list=[], maxstd = None):
    # Sort All_Info object by course, term, campus and program
    All.obList.sort(key=lambda x: (x.course_code, x.course_term_code, x.std_prg_code))

    # Initialise the codes
    course_code = 'df'
    term_code = 'df'
    if (maxstd == None
        or maxstd > len(All.obList)):
        maxstd = len(All.obList)

    # Loop through All_Info objects
    ## maxstudents sets a limit on the number of object in the loop
    for x in All.obList[:maxstd]:
        if ((x.course_term_code in term_code_list
             or term_code_list == [])
            and
            (x.std_prg_code in prg_list
             or prg_list == [])):
            #print x.course_term_code, x.std_prg_code
        # If course changes create a new Course object
        # The course object include the student count
            if (course_code != x.course_code
                or term_code != x.course_term_code):
                c = Course(x.course_code, x.course_term_code, x.course_school_code,
                           x.course_school_name, x.course_college_code, x.course_college_name)

                # Change codes to new codes
                course_code = x.course_code
                term_code = x.course_term_code
            #std1 = [std for std in StudentProgram.obList if (std.nds_empid == x.std_nds_empid
            #                                                 and std.prg_code == x.std_prg_code)]

            #if len(std1) == 1:  c.stdobList.append(std1[0])

            c.stdList.append([x.std_nds_empid, x.std_prg_code])

def createCourseConnections(term_code_list=[], college=None):
    # record courses in network map
    usedcourseList = []
    # record used courses to avoid double counting of edges
    usediList = []
    for i in range(len(Course.obList)): # this is the number of courses
        c1 = Course.obList[i]
        if i%100 ==0:
            print i
        if (college == None
            or c1.college_code == college):
            usedcourseList.append(c1)   # Add used course
            usediList.append(i)         # Add used index
            for j in range(len(Course.obList)):
                if j not in usediList:
                    c2 = Course.obList[j]
                    if (((c1.term_code in term_code_list
                          and c2.term_code in term_code_list)
                         or term_code_list == [])
                        ):
                        CourseConnections(c1, c2)

    print 'Total CourseConnections:\t%i' % len(CourseConnections.obList)

    # Remove CourseConnection with zero students
    # and add Target courses to usedcourseList
    temp = []
    NullCount = 0
    for cc in CourseConnections.obList:
        if cc.std_pop() > 0:
            temp.append(cc)
            if cc.course2 not in usedcourseList:
                usedcourseList.append(cc.course2)
        else:
            NullCount += 1
    CourseConnections.obList = temp
    Course.obList = usedcourseList
    print 'Null CourseConnections:\t%i' % NullCount
    print 'NonZero CourseConnections:\t%i' % len(CourseConnections.obList)

def saveedges(savefilename, ccList):
    # Order edges by first course_code
    ccList.sort(key=lambda x: (x.course1.term_code,
                               x.course1.college_code,
                               x.course1.school_code,
                               x.course1.course_code))

    print "Save File: %s" % savefilename

    f1 = open(savefilename, "w")
    txt = 'Source,Target,Weight,'
    print "Header line: %s" % txt
    txt += '\n'
    f1.write(txt)
    for cc in ccList:
        try:
            txt = '%s,%s,%i,\n' % (cc.course1.course_code,
                                   cc.course2.course_code,
                                   cc.std_pop())
            f1.write(txt)
        except Exception as e:
            print txt
            print e
    f1.close()

def savenodes(savefilename, cList):
    # Order edges by first course_code
    cList.sort(key=lambda x: (x.term_code,
                              x.college_code,
                              x.school_code,
                              x.course_code))

    print "Save File: %s" % savefilename

    f1 = open(savefilename, "w")
    txt = 'ID,student_pop,school_code,school_name,college_code,year,term_code,'
    print "Header line: %s" % txt
    txt += '\n'
    f1.write(txt)
    for c in cList:
        try:
            txt = '%s,%i,' % (c.course_code,
                              c.std_pop())

            txt += '"%s","%s",%s,' % (c.school_code,
                                      c.school_name,
                                      c.college_code)
            txt += '%i,%i,\n' % (c.year,
                                 c.term_code)
            f1.write(txt)
        except Exception as e:
            print txt
            print e
    f1.close()

def graphNetwork(edgesfile, nodesfile, layout='spring', graphfile='network_grpah.png',
                 title="",
                 show_labels=False,
                 constant_node_size=False):
    import networkx as nx
    import matplotlib.pyplot as plt
    import pandas as pd
    # Declare graph object
    G = nx.Graph()
    # Read network data
    inputedges = pd.read_csv(edgesfile)
    inputnodes = pd.read_csv(nodesfile)
    node_sizes = []
    node_colours = []
    node_labels = []
    for i, r in inputnodes.iterrows():
        if r['college_code'] == "DSC":
            G.add_node(r['ID'], color = 'red', size=r['student_pop'], label='DSC')
        elif r['college_code'] == "BUS":
            G.add_node(r['ID'], color= 'blue', size=r['student_pop'], label='BUS')
        elif r['college_code'] == "SEH":
            G.add_node(r['ID'], color= 'green', size=r['student_pop'], label='SEH')
        else:
            G.add_node(r['ID'], color='black', size=r['student_pop'], label='NA')

        node_labels.append(r['ID'])

    for i, r in inputedges.iterrows():
        #if r['Weight'] > 300:
        #    G.add_edge(r['Source'], r['Target'], weight=int(300))
        #else:
        G.add_edge(r['Source'], r['Target'], weight=int(r['Weight']))

    # assign layout
    if layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    else:
        pos = nx.spring_layout(G, iterations=200, scale=5000)

    # set nodes to positions
    nx.set_node_attributes(G, 'pos', pos)

    try:
        color_map = []
        size_map = []
        edge_colors = []
        for n in G.nodes():
            color_map.append(G.node[n]['color'])
            size_map.append(G.node[n]['size'])

        for e in G.edges(data=True):
            edge_colors.append(e[2]['weight'])


        labels = {k: k for k in node_labels}
        plt.figure(figsize=(12.0, 9.0))
        plt.title(title)
        if constant_node_size:
            nodes = nx.draw_networkx_nodes(G, pos=pos, labels=labels, node_size=8, node_color=color_map)
        else:
            nodes = nx.draw_networkx_nodes(G, pos=pos, labels=labels, node_size=size_map, node_color=color_map)
        edges = nx.draw_networkx_edges(G, pos=pos, edge_color=edge_colors, edge_cmap=plt.cm.copper_r)
        plt.colorbar(edges)
        plt.axis('off')
        if show_labels:
            nx.draw_networkx_labels(G, pos, labels, font_size=12)

        print "Nodes:\t%i" % G.number_of_nodes()
        print "Edges:\t%i" % G.number_of_edges()

        plt.savefig(graphfile, dpi=500)
        plt.clf()
        plt.close()

    except Exception as e:
        print e
        pass

def rankCourseAdundance(courseList, title=''):
    # sort courseList by student population
    courseRankList = []

    for std_pop in range(max([c.std_pop() for c in courseList])+1):
        courseCount = len([c for c in courseList if (c.std_pop() == std_pop)])
        courseRankList.append([std_pop, courseCount])

    try:
        x = [r[0] for r in courseRankList]
        y = [r[1] for r in courseRankList]

        ax.plot(x, y, '-', linewidth=2, label=title)

        ax.legend(loc='upper right')
        ax.set_xlabel('No of Students in course')
        ax.set_ylabel('Frequeny')
        plt.show()

    except Exception as e:
        print e
        pass

term_list = [1605, 1710, 1750, 1705, 1701, 1745]
#term_list = [1710]
#term_list = []
college_list = [None]
#prg_list = ['AD023']
prg_list = []

print dt.datetime.now()
# Read in all data------------------------------------------------------------------
#sourcefilename = "H:\Data\LMS_Schedule\Useful\JamesData\Student_class_program_school_college_20170522_jt.csv"
sourcefilename = "/Users/e35596/RMITStudios/tests/Pete_code/Student_class_program_school_college_20170522_jt.csv"
f1 = open(sourcefilename, "r")

print sourcefilename
readAllFile(f1)
print dt.datetime.now()
print "All_Info objects: %i" % len(All.obList)
AllobList = []
for a in All.obList:
    AllobList.append(a)

for college in college_list:
    Course.obList=[]
    CourseConnections.obList=[]
    # Limit to selected term_code and prg_codes
    temp = []
    for x in AllobList:
        if ((x.course_term_code in term_list
             or term_list == [])
            and
            (x.std_prg_code in prg_list
             or prg_list == [])):
            temp.append(x)
    All.obList = temp
    print dt.datetime.now()
    print "Limit to terms", term_list
    print "Limit to program", prg_list
    print "All_Info objects: %i" % len(All.obList)

    # Create Students
    createStudentPrograms(term_list, prg_list)
    print dt.datetime.now()
    print "Students: %i" % len(StudentProgram.obList)
    # Create Course
    createCourses(term_list, prg_list)
    print dt.datetime.now()
    print 'Courses:\t%i' % len(Course.obList)
    temp = []
    for c in Course.obList:
        if (c.college_code == college
            or
            college == None):
            temp.append(c)
    Course.obList = temp

    # Build filename
    savefilename = ''

    # Add college
    try:
        if college != None:
            savefilename += '%s_' % college
    except: pass

    # Add terms
    for term in term_list:
        savefilename += '%i_' % term

    # Add programs
    for prg in prg_list:
        savefilename += '%s_' % prg

    # Title
    title = savefilename[:-1]

    fig, ax = plt.subplots()
    '''
    for col_code in ['DSC', 'BUS', 'SEH']:
        courseRankList = []
        courseList = [c for c in Course.obList if c.college_code == col_code]
        print col_code, len(courseList)
        for std_pop in range(max([c.std_pop() for c in courseList]) + 1):
            courseCount = len([c for c in courseList if (c.std_pop() == std_pop)])
            courseRankList.append([std_pop, courseCount])
        x = [r[0] for r in courseRankList]
        y = [r[1] for r in courseRankList]
        if col_code == 'DSC': col = 'r'
        if col_code == 'BUS': col = 'b'
        if col_code == 'SEH': col = 'g'
        ax.plot(x, y, '-', linewidth=1, label=col_code, color=col)
    ax.legend(loc='upper right')
    ax.set_xlabel('No of Students in course')
    ax.set_ylabel('Frequency')
    plt.show()
    '''
    '''
    for college in ['DSC', 'BUS', 'SEH']:
        courseRankList = []
        courseList = [c for c in Course.obList if c.college_code == college]
        print college, len(courseList)
        for std_pop in range(max([c.std_pop() for c in courseList]) + 1):
            courseCount = len([c for c in courseList if (c.std_pop() == std_pop)])
            courseRankList.append([std_pop, courseCount])
        x = [r[0] for r in courseRankList]
        y = [r[1] for r in courseRankList]
        if college == 'DSC': col = 'r'
        if college == 'BUS': col = 'b'
        if college == 'SEH': col = 'g'
        ax.plot(x, y, '-', linewidth=1, label=college, color=col)
    ax.legend(loc='upper right')
    ax.set_xlabel('No of Students in course')
    ax.set_ylabel('Frequency')
    plt.show()
    '''
    #Creat CourseConnections
    createCourseConnections(term_list, college)
    CourseConnections.obList.sort(key=lambda x: (x.course1.course_code, x.course2.course_code))


    #savefolder = 'H:\Data\Student Network Map\JamesData\\'
    savefolder = '/Users/e35596/RMITStudios/tests/Pete_code/'
    #prgsavefolder = savefolder + 'Programs\\%s\\' % prg

    #if not os.path.exists(prgsavefolder):
    #    os.makedirs(prgsavefolder)

    # Bulid filename
    savefilename = ''

    # Add college
    try:
        if college != None:
            savefilename += '%s_' % college
    except: pass

    # Add terms
    for term in term_list:
        savefilename += '%i_' % term

    # Add programs
    for prg in prg_list:
        savefilename += '%s_' % prg

    # Title
    title = savefilename[:-1]

    # Save files
    edgesfile = '%s%sedges.csv' % (savefolder, savefilename)
    nodesfile = '%s%snodes.csv' % (savefolder, savefilename)

    pngfile = '%sGraphs\\%s_network_graph_copper.png' % (savefolder, savefilename)
    pdffile = '%sGraphs\\%s_network_graph_copper.pdf' % (savefolder, savefilename)

    saveedges(edgesfile, CourseConnections.obList)
    savenodes(nodesfile, Course.obList)

    if len(Course.obList)>0:
        if len(Course.obList)<50:
            graphNetwork(edgesfile, nodesfile,
                         graphfile=pngfile, title=title,
                         show_labels=True, constant_node_size=False)
        else:
            graphNetwork(edgesfile, nodesfile,
                         graphfile=pngfile, title=title,
                         show_labels=False, constant_node_size=True)

    gc.collect()

    print dt.datetime.now()

#nodesfile= "H:\Data\Student Network Map\JamesData\\nodes_BP254_1710.csv"
#edgesfile = "H:\Data\Student Network Map\JamesData\\edges_BP254_1710.csv"
#graphNetwork(edgesfile, nodesfile, layout='shell')
#graphNetwork(edgesfile, nodesfile, layout='spring')


'''
class CourseConnections2:
    """ Course Object"""
    # Contains information relating to Courses, broken down by Programs.
    obList = []
    def __init__(self, course1, course2, stdList):

        self.course1 = next((x for x in Course.obList if x.course_code == course1[0] and x.term_code ==course1[1]),
                            None)
        self.course2 = next((x for x in Course.obList if x.course_code == course2[0] and x.term_code == course2[1]),
                            None)

        self.stdList = stdList
        print self.info()
        CourseConnections2.obList.append(self)

    # returns header text string with Course variables with tab seperators
    def header(self):
        txt = 'term_code1\tcourse_code1\t'
        txt += 'term_code2\tcourse_code2\t'
        txt += 'std_pop\tprg_code\tprg_pop'
        return txt

    # returns text string with CourseConnections2 variables with tab seperators
    def info(self):
        txt = ''
        txt += '%i\t%s\t' % (self.course1.term_code,
                             self.course1.course_code)
        txt += '%i\t%s\t' % (self.course2.term_code,
                             self.course2.course_code)
        txt += '%i\t' % self.std_pop()
        for prg in self.prg_list():
            txt += '%s\t%i\t' % (prg[0], prg[1])
        return txt[:-1]

    # returns text string with Course variables headers with comma seperators
    def headerCSV(self):
        txt = 'term_code1,course_code1,'
        txt += 'term_code2,course_code2,'
        txt += 'std_pop'
        return txt

    # returns text string with Course variables with comma seperators
    def CSV(self):
        txt = ''
        txt += '%i,%s,' % (self.course1.term_code,
                             self.course1.course_code)
        txt += '%i,%s,' % (self.course2.term_code,
                             self.course2.course_code)
        txt += '%i,' % self.std_pop()
        return txt

    def std_pop(self):
        return len(self.stdList)

    def prg_list(self):
        prg_list = []
        prg_pop_list = []
        for std in self.stdList:
            if std[1] not in prg_list:
                prg_list.append(std[1])
                prg_pop_list.append(1)
            else:
                i = prg_list.index(std[1])
                prg_pop_list[i] += 1
        temp = []
        for i in range(len(prg_list)):
            temp.append([prg_list[i], prg_pop_list[i]])
        temp.sort(key=lambda x: x[1], reverse=True)
        return temp

def createEdges(term_code_list, maxstd=None):
    # restrict to course in term_code
    All_short = [x for x in All.obList if x.course_term_code in term_code_list]
    All_short.sort(key=lambda x: (x.std_nds_empid, x.course_term_code, x.course_code))

    students = 0
    course_connections = []
    course_connections_stdList = []

    if (maxstd == None
        or maxstd > len(All_short)):
        maxstd = len(All_short)

    for i in range(1, maxstd):
        std1 = All_short[i - 1]
        std2 = All_short[i]
        if (std1.std_nds_empid == std2.std_nds_empid):
            if ([[std1.course_code, std1.course_term_code],
                 [std2.course_code, std2.course_term_code]] not in course_connections):
                course_connections.append([[std1.course_code, std1.course_term_code],
                                           [std2.course_code, std2.course_term_code]])
                course_connections_stdList.append([std1.std_nds_empid, std1.std_prg_code])
                print [[std1.course_code, std1.course_term_code],[std2.course_code, std2.course_term_code]], [std1.std_nds_empid, std1.std_prg_code]
            else:
                j = course_connections.index([[std1.course_code, std1.course_term_code],
                                              [std2.course_code, std2.course_term_code]])
                course_connections_stdList[j].append([std1.std_nds_empid, std1.std_prg_code])
        else:
            students += 1
    temp = []
    for i in range(len(course_connections)):
        CourseConnections2(course_connections[i][0], course_connections[i][1], course_connections_stdList[i])
        temp.append([course_connections[i][0], course_connections[i][1], course_connections_stdList[i]])
    return temp

edges = createEdges(term_list)

print 'Edges:\t%i' % len(edges)
print 'CC:\t%i' % len(CourseConnections2.obList)
print dt.datetime.now()
'''
