"""
Filter job posts based on different parameters
"""

import sys


def get_position():
    """ Filter by postion."""

    position = input("What postion you want to apply?\n")
    if position == '':
        print('Please specify the position you want to work on.')
        get_location()
    return position

def get_location():
    """ Filter by location."""
    location = input("Where do you want to work?\n")    
    if location == '':
        print('Please specify the location you want to work on.')
        get_location()
    return location

def get_job_type():
    """ Filter by job type."""
    type_list = ['fulltime', 'contract', 'parttime', 'internship', 'temporary']
    print("Select the type of job you want to work.")
    for i, job in enumerate(type_list):
        print(f'{i+1} -> {job}')
    ch = input('Your choice: ')
    valid_choices = [i+1 for i in  range(len(type_list))]
    if ch in valid_choices:
        return type_list[ch - 1]
    else:
        get_job_type()

def get_experience():
    """ Filter by experience level."""
    exp_list = ['Entry level', 'Mid level', 'Senior level']
    print("Select the level of experience you have.")
    for i, expr in enumerate(exp_list):
        print(f'{i+1} -> {expr}')
    ch = input('Your choice: ')
    valid_choices = [i+1 for i in  range(len(exp_list))]
    if ch in valid_choices:
        return exp_list[ch - 1]
    else:
        get_experience()
        
def get_developer_skill():
    """ Filter by developer skills."""
    skill_list = ['python', 'java', 'javascript', 'django', 'sql', 'react']
    pass

def get_date_posted():
    """ Filter by date posted."""
    date_list = [1, 3, 7, 14]
    pass