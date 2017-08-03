#!/usr/bin/python

from datetime import datetime

now = datetime.now()

#print now

def compare_date(date_string):
    '''
    Stuff
    '''
    space = date_string.find(' ')
    status = 'live' # if date_end is \N, assume course is still live
    if space > -1:
        date_string = date_string[0:space]
        fixed_date = datetime.strptime(date_string, "%Y-%m-%d")
        if fixed_date <= now:
            status = 'completed'
        else:
            status = 'live'
    return status

#print compare_date('\N')
