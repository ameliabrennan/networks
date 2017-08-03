#!/usr/bin/python

def clean_sis_course_id(input_string):
    '''
    Looks for _ in a sis_source_id, if found it removes it and everything following.
    '''
    position = input_string.find('_')
    if position > -1:
        input_string = input_string[0:position]
    return input_string

#print clean_sis_course_id('nothing_here')
