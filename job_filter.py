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
    pass

def get_experience():
    """ Filter by experience level."""
    exp_list = ['Entry level', 'Mid level', 'Senior level']
    pass

def get_developer_skill():
    """ Filter by developer skills."""
    skill_list = ['python', 'java', 'javascript', 'django', 'sql', 'react']
    pass

def get_date_posted():
    """ Filter by date posted."""
    date_list = [1, 3, 7, 14]
    pass