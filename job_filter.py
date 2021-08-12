"""
Filter job posts based on different parameters
"""

import sys


def get_positions():
    """ Filter by postion."""
    print("\nWhat postion you want to apply for?\n")
    print('Enter one position per line. (type "END" when finished)\n')

    positions = []

    answer = input()
    while answer != "END":            
        if answer != '':
            positions.append(answer)
        answer = input()

    return positions


def get_locations():
    """ Filter by location."""
    print("\nWhere would you like to work?\n")
    print('Enter one position per line. (type "END" when finished)\n') 

    locations = []

    answer = input()
    while answer != "END":            
        if answer != '':
            locations.append(answer)
        answer = input()

    return locations

def get_job_types():
    """ Filter by job type."""
    # fulltime, contract, parttime
    type_list = ['fulltime', 'contract', 'parttime', 'internship']
    print("Select the type of job you want to work.")
    for i, job in enumerate(type_list):
        print(f'{i+1} -> {job}')
    ch = input('Your choice: ')
    valid_choices = [i+1 for i in  range(len(type_list))]
    if ch in valid_choices:
        return type_list[ch - 1]
    else:
        get_job_type()

def get_experiences():
    """ Filter by experience level."""
    # entry_level, mid_level, senior_level
    exp_list = ['Entry level', 'Mid level', 'Senior level']
    print("Select the level of experience you have.")
    for i, expr in enumerate(exp_list):
        print(f'{i+1} -> {expr}')
    ch = input('Your choice: ')
    valid_choices = [i+1 for i in  range(len(exp_list))]
    if ch in valid_choices:
        return exp_list[ch - 1]
    else:
        get_experiences()

def get_developer_skill():
    """ Filter by developer skills."""
    skill_list = ['python', 'java', 'javascript', 'django', 'sql', 'react']
    pass
